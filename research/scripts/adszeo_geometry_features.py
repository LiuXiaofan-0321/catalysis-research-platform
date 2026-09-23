"""Precompute leakage-safe pore-geometry descriptors for AdsZeo structures.

Everything is derived from pre-adsorption framework coordinates only
(structures + framework_atoms tables; positions/cycle_stats never touched).

Topology-level quantities (identical for all structures of a framework_code
because cell and framework positions are shared) are computed once per code:
  - smallest-ring size distribution over T sites (T = Si/Al, bonded via O)
  - mean/max smallest ring, ring entropy
  - coordination sequence means (graph distance 1/2/3)
  - T-T bond length mean/std, O-T-O angle mean/std
Structure-level quantities (depend on Al placement):
  - fraction of Al sites with another Al within two T-O-T hops
  - mean local O-Al-O angle deviation from the framework O-T-O mean

Output: CSV keyed by structure_id + sha256 sidecar.
"""
import hashlib
import math
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path

import duckdb
import numpy as np

DB = "/public/home/xiaohe/lxf/catalysis-rag/benchmarks/adszeo-v1/AdsZeo_data.duckdb"
OUT = Path("/public/home/xiaohe/lxf/catalysis-rag/benchmarks/adszeo-v1/geometry-features-v1.csv")
T_ELEMENTS = {"Si", "Al"}
TO_CUTOFF = 2.2  # angstrom, T-O bond assignment
RING_CAP = 12    # max graph distance searched for the far side of a ring

RING_BUCKETS = (4, 5, 6, 7, 8, 10, 12)  # smallest-ring sizes tracked separately


def cell_matrix(record):
    a, b, c = (float(record[f"cell_{axis}"]) for axis in "abc")
    alpha, beta, gamma = np.deg2rad(
        [float(record["cell_alpha"]), float(record["cell_beta"]), float(record["cell_gamma"])]
    )
    sin_gamma = math.sin(gamma)
    va = np.array([a, 0.0, 0.0])
    vb = np.array([b * math.cos(gamma), b * math.sin(gamma), 0.0])
    cx = c * math.cos(beta)
    cy = c * (math.cos(alpha) - math.cos(beta) * math.cos(gamma)) / sin_gamma
    cz = math.sqrt(max(c * c - cx * cx - cy * cy, 0.0))
    return np.vstack([va, vb, [cx, cy, cz]])


def mic_delta(frac_i, frac_j):
    delta = frac_j[None, :, :] - frac_i[:, None, :]
    delta -= np.rint(delta)
    return delta


def build_topology(frac_T, frac_O, M):
    """Return per-T graph adjacency, bond vectors, and geometry stats."""
    delta = mic_delta(frac_T, frac_O)          # (nT, nO, 3)
    dist = np.linalg.norm(delta @ M, axis=2)   # (nT, nO)
    nT = frac_T.shape[0]
    bonds = [[] for _ in range(nT)]            # T -> list of (O, vector)
    o_count = defaultdict(int)
    for o in range(frac_O.shape[0]):
        nearest = np.argsort(dist[:, o])[:2]
        t1, t2 = int(nearest[0]), int(nearest[1])
        if dist[t1, o] > TO_CUTOFF or dist[t2, o] > TO_CUTOFF or t1 == t2:
            continue
        bonds[t1].append((o, delta[t1, o] @ M))
        bonds[t2].append((o, delta[t2, o] @ M))
        o_count[t1] += 1
        o_count[t2] += 1
    adj = [[] for _ in range(nT)]
    for o in range(frac_O.shape[0]):
        order = np.argsort(dist[:, o])[:2]
        t1, t2 = int(order[0]), int(order[1])
        if dist[t1, o] > TO_CUTOFF or dist[t2, o] > TO_CUTOFF or t1 == t2:
            continue
        adj[t1].append(t2)
        adj[t2].append(t1)
    # O-T-O angles from bond vectors; T-T bond lengths via minimum-image distances
    angles = []
    for t in range(nT):
        vecs = [v for _, v in bonds[t]]
        for i in range(len(vecs)):
            for j in range(i + 1, len(vecs)):
                cosang = float(np.dot(vecs[i], vecs[j])
                               / (np.linalg.norm(vecs[i]) * np.linalg.norm(vecs[j])))
                angles.append(math.degrees(math.acos(max(-1.0, min(1.0, cosang)))))
    dTT = np.linalg.norm(mic_delta(frac_T, frac_T) @ M, axis=2)
    np.fill_diagonal(dTT, np.inf)
    bond_lengths = [dTT[t, u] for t in range(nT) for u in adj[t] if u > t]
    angle_arr = np.asarray(angles)
    return {
        "adj": adj,
        "tt_bond_mean": float(np.mean(bond_lengths)) if bond_lengths else np.nan,
        "tt_bond_std": float(np.std(bond_lengths)) if bond_lengths else np.nan,
        "otot_angle_mean": float(np.mean(angle_arr)) if angle_arr.size else np.nan,
        "otot_angle_std": float(np.std(angle_arr)) if angle_arr.size else np.nan,
        "t_degree_mean": float(np.mean([len(a) for a in adj])),
        "o_degree_mean": float(np.mean(list(o_count.values()))) if o_count else np.nan,
    }


def coordination_sequence(adj, start, depth):
    seen = {start}
    frontier = [start]
    counts = []
    for _ in range(depth):
        nxt = []
        for u in frontier:
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    nxt.append(w)
        counts.append(len(nxt))
        frontier = nxt
    return counts


def smallest_ring_size(adj, v):
    best = None
    nbrs = adj[v]
    for i in range(len(nbrs)):
        for j in range(i + 1, len(nbrs)):
            a, b = nbrs[i], nbrs[j]
            dist = {a: 0}
            dq = deque([a])
            found = -1
            while dq and found < 0:
                u = dq.popleft()
                du = dist[u]
                if du >= RING_CAP:
                    continue
                for w in adj[u]:
                    if w == v or w in dist:
                        continue
                    dist[w] = du + 1
                    if w == b:
                        found = du + 1
                        break
                    dq.append(w)
            if found >= 0:
                cand = found + 2
                if best is None or cand < best:
                    best = cand
    return best


def ring_entropy(counts, total):
    ent = 0.0
    for c in counts.values():
        if c > 0:
            p = c / total
            ent -= p * math.log(p)
    return ent


def main():
    t0 = time.time()
    con = duckdb.connect(DB, read_only=True)
    structures = con.execute(
        "SELECT structure_id, framework_code, cell_a, cell_b, cell_c, cell_alpha,"
        " cell_beta, cell_gamma FROM structures ORDER BY structure_id"
    ).fetchall()
    atoms = con.execute(
        "SELECT structure_id, element, frac_x, frac_y, frac_z FROM framework_atoms"
    ).fetchall()
    con.close()
    by_struct = defaultdict(list)
    for sid, el, x, y, z in atoms:
        by_struct[sid].append((el, float(x), float(y), float(z)))
    del atoms
    print(f"loaded {len(structures)} structures, {sum(len(v) for v in by_struct.values())} atoms "
          f"in {time.time() - t0:.0f}s", flush=True)

    topo_cache = {}
    rows = []
    warnings = []
    for si, (sid, code, a, b, c, al, be, ga) in enumerate(structures):
        rec = {"cell_a": a, "cell_b": b, "cell_c": c,
               "cell_alpha": al, "cell_beta": be, "cell_gamma": ga}
        M = cell_matrix(rec)
        els = by_struct.get(sid, [])
        is_T = np.array([el in T_ELEMENTS for el, *_ in els])
        T_all = [i for i, flag in enumerate(is_T) if flag]
        O_all = [i for i, flag in enumerate(is_T) if not flag]
        frac_T_all = np.array([[els[i][1], els[i][2], els[i][3]] for i in T_all])
        frac_O = np.array([[els[i][1], els[i][2], els[i][3]] for i in O_all])
        elements_T = [els[i][0] for i in T_all]

        topo = topo_cache.get(code)
        if topo is None:
            topo = build_topology(frac_T_all, frac_O, M)
            adj = topo["adj"]
            nT = len(adj)
            ring_sizes = [smallest_ring_size(adj, v) for v in range(nT)]
            ring_counter = Counter(r for r in ring_sizes if r and r <= 14)
            total = sum(ring_counter.values())
            bucket_fracs = {}
            for bucket in RING_BUCKETS:
                bucket_fracs[f"ring{bucket}_frac"] = ring_counter.get(bucket, 0) / total
            big = sum(c for r, c in ring_counter.items() if r > 12)
            bucket_fracs["ring13p_frac"] = big / total
            cs = np.asarray([coordination_sequence(adj, v, 3) for v in range(nT)], dtype=float)
            topo.update({
                **bucket_fracs,
                "ring_mean": float(np.mean([r for r in ring_sizes if r and r <= 14])),
                "ring_entropy": ring_entropy(ring_counter, total),
                "cs2_mean": float(np.mean(cs[:, 1])),
                "cs3_mean": float(np.mean(cs[:, 2])),
                "n_T": nT,
            })
            topo_cache[code] = topo
            if si % 40 == 0:
                print(f"  topology {code}: nT={nT} degree={topo['t_degree_mean']:.2f} "
                      f"o_deg={topo['o_degree_mean']:.2f} ring_mean={topo['ring_mean']:.2f} "
                      f"({time.time() - t0:.0f}s)", flush=True)
            if abs(topo["t_degree_mean"] - 4.0) > 0.2 or abs(topo["o_degree_mean"] - 2.0) > 0.2:
                warnings.append(f"{code}: degrees {topo['t_degree_mean']:.2f}/{topo['o_degree_mean']:.2f}")

        # per-structure Al features
        adj = topo["adj"]
        al_nodes = [i for i, el in enumerate(elements_T) if el == "Al"]
        second_shell_hits = 0
        for v in al_nodes:
            two_hop = set()
            for u in adj[v]:
                two_hop.update(adj[u])
            two_hop.discard(v)
            if any(elements_T[w] == "Al" for w in two_hop):
                second_shell_hits += 1
        al_second = second_shell_hits / len(al_nodes) if al_nodes else np.nan

        row = {"structure_id": sid, "framework_code": code, "al_count": len(al_nodes),
               "n_T": topo["n_T"], "al_second_shell_al_frac": al_second}
        for key in RING_BUCKETS:
            row[f"ring{key}_frac"] = topo[f"ring{key}_frac"]
        row["ring13p_frac"] = topo["ring13p_frac"]
        row["ring_mean"] = topo["ring_mean"]
        row["ring_entropy"] = topo["ring_entropy"]
        row["cs2_mean"] = topo["cs2_mean"]
        row["cs3_mean"] = topo["cs3_mean"]
        row["tt_bond_mean"] = topo["tt_bond_mean"]
        row["tt_bond_std"] = topo["tt_bond_std"]
        row["otot_angle_mean"] = topo["otot_angle_mean"]
        row["otot_angle_std"] = topo["otot_angle_std"]
        rows.append(row)
        if si % 500 == 0:
            print(f"  structure {si + 1}/{len(structures)} ({time.time() - t0:.0f}s)", flush=True)

    import pandas as pd
    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    (OUT.parent / (OUT.name + ".sha256")).write_text(digest + "\n")
    print(f"wrote {OUT} rows={len(df)} cols={len(df.columns)} sha256={digest}", flush=True)
    if warnings:
        print("degree warnings:", warnings[:10], flush=True)
    print("GEOMETRY_DONE", flush=True)


if __name__ == "__main__":
    sys.exit(main())

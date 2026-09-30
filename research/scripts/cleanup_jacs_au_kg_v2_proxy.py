"""Stop this run's dedicated cluster proxy after every queued stage terminates."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time


TERMINAL = {'COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT', 'OUT_OF_MEMORY',
            'NODE_FAIL', 'PREEMPTED', 'BOOT_FAIL', 'DEADLINE', 'REVOKED'}


def all_jobs_terminated(job_ids):
    result = subprocess.run(['sacct', '-n', '-X', '-j', ','.join(job_ids),
        '--format=JobID%32,State%32', '--parsable2'], capture_output=True, text=True, check=True)
    states = {}
    for line in result.stdout.splitlines():
        if not line.strip(): continue
        job_id, state = line.strip().split('|')[:2]
        base = job_id.split('_')[0]
        if base in job_ids:
            states.setdefault(base, []).append(state.split()[0].rstrip('+'))
    return all(states.get(j) and all(s in TERMINAL for s in states[j]) for j in job_ids)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--jobs', nargs='+', help='Watch these Slurm jobs on login2 before stopping its proxy')
    args = parser.parse_args()
    if args.jobs:
        while not all_jobs_terminated(args.jobs): time.sleep(60)
    pid = int((args.run/'proxy.pid').read_text().strip())
    process = Path('/proc')/str(pid)
    expected_name = args.run.name
    if not process.exists():
        status = 'already_stopped'
    else:
        command = (process/'cmdline').read_bytes().split(b'\0')
        if process.stat().st_uid != os.getuid() or (
                not any(arg.endswith((b'/api_proxy_300s.py', b'/api_proxy_1800s.py')) for arg in command)
                or b'--name' not in command
                or command[command.index(b'--name')+1].decode() != expected_name):
            raise RuntimeError('Recorded PID does not belong to this run proxy; refuse to signal')
        os.kill(pid, signal.SIGTERM)
        status = 'termination_requested'
        for _ in range(20):
            if not process.exists():
                status = 'stopped'; break
            time.sleep(.25)
    report = {'pid': pid, 'status': status, 'proxy_name': expected_name}
    (args.run/'proxy-cleanup.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__': main()

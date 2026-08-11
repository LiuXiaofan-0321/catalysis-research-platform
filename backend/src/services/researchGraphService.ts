import fs from 'fs/promises';
import path from 'path';
import prisma from '../config/db';
import { stableHash } from '../utils/hash';

type JsonObject = Record<string, any>;

export interface StageOneArtifact {
  source?: JsonObject;
  extraction: {
    schema_version?: string;
    paper: JsonObject;
    abstract?: JsonObject;
    summary?: JsonObject;
    keywords?: { author_keywords?: unknown[]; extracted?: JsonObject[] };
    entities?: JsonObject[];
    experiments?: JsonObject[];
    observations?: JsonObject[];
    claims?: JsonObject[];
    visual_review_items?: JsonObject[];
    quality?: JsonObject;
    extraction_metadata?: JsonObject;
  };
}

export interface ResearchAdvicePayload {
  answer: string;
  candidateDirections: Array<{
    title: string;
    hypothesis: string;
    rationale: string;
    novelty: string;
    systemDesign: {
      molecularSieveRole: string;
      activePhaseRole: string;
      interfaceStrategy: string;
      proposedPathway: string;
      selectivityTarget: string;
      evidenceBoundary: string;
    };
    supportingEvidence: Array<{
      nodeId: string;
      paperId?: string | null;
      quote?: string | null;
      role: string;
    }>;
    feasibility: 'high' | 'medium' | 'low';
    confidence: number;
    risks: string[];
    nextExperiment: {
      objective: string;
      materials: string[];
      procedure: string[];
      variables: string[];
      controls: string[];
      measurements: string[];
      decisionRules: string[];
      stoppingCriteria: string[];
    };
  }>;
  contradictions: string[];
  dataGaps: string[];
  safetyNotes: string[];
}

const stringify = (value: unknown, fallback: unknown = {}) => {
  try { return JSON.stringify(value ?? fallback); } catch { return JSON.stringify(fallback); }
};

const parse = <T>(value: string | null | undefined, fallback: T): T => {
  try { return value ? JSON.parse(value) as T : fallback; } catch { return fallback; }
};

const text = (value: unknown, max = 1200) => {
  const normalized = String(value ?? '').replace(/\s+/g, ' ').trim();
  return normalized.length > max ? `${normalized.slice(0, max)}…` : normalized;
};

const normalizeKey = (value: unknown) =>
  String(value ?? '').normalize('NFKC').toLowerCase().replace(/[\s\-_/\\()[\]{}:;,.，。；：]+/g, '').trim();

const clamp01 = (value: unknown, fallback = 0.75) => {
  const number = Number(value);
  return Number.isFinite(number) ? Math.max(0, Math.min(1, number)) : fallback;
};

const evidenceFor = (record: JsonObject | undefined) =>
  Array.isArray(record?.evidence) ? record.evidence.filter((item: unknown) => item && typeof item === 'object') : [];

const confidenceFor = (record: JsonObject | undefined) => {
  const validations = evidenceFor(record).map((item: JsonObject) => item.evidence_validation);
  let fallback = validations.includes('unverified')
    ? 0.42
    : validations.includes('locally_recovered')
      ? 0.72
      : validations.includes('exact')
        ? 0.96
        : 0.7;
  if (record?.needs_visual_review) fallback = Math.min(fallback, 0.58);
  return clamp01(record?.confidence, fallback);
};

const reviewStatusFor = (record: JsonObject | undefined) =>
  record?.review_status === 'needs_review' || record?.needs_visual_review ? 'needs_review' : 'extracted';

const asArtifact = (value: unknown): StageOneArtifact => {
  const artifact = value as StageOneArtifact;
  if (!artifact?.extraction?.paper) throw new Error('JSON 缺少 extraction.paper');
  return artifact;
};

const documentKeyFor = (paper: JsonObject, source?: JsonObject) => {
  if (text(paper.id, 400)) return text(paper.id, 400);
  if (text(paper.doi, 400)) return `doi:${text(paper.doi, 400).toLowerCase().replace(/^doi:/, '')}`;
  const sha = text(paper.source_pdf_sha256 || source?.source_pdf_sha256, 128);
  return sha ? `sha256:${sha}` : `paper:${stableHash([paper.title, paper.year, paper.source_path]).slice(0, 32)}`;
};

const idFor = (prefix: string, workspaceId: string, key: string) =>
  `${prefix}-${stableHash([workspaceId, key]).slice(0, 32)}`;

const globalNodeKey = (kind: string, category: unknown, canonical: unknown, fallback: unknown) =>
  `${kind}:${text(category, 80) || 'other'}:${stableHash(normalizeKey(canonical) || normalizeKey(fallback)).slice(0, 24)}`;

const paperNodeKey = (type: string, documentKey: string, localId: unknown) =>
  `${type}:${stableHash([documentKey, text(localId, 160)]).slice(0, 28)}`;

const deserializeDocument = (row: any) => ({
  id: row.id,
  title: row.title,
  doi: row.doi,
  year: row.year,
  journal: row.journal,
  paperType: row.paperType,
  catalysisSystem: row.catalysisSystem,
  reactionCategories: parse(row.reactionCategoriesJson, []),
  summary: parse(row.summaryJson, {}),
  quality: parse(row.qualityJson, {})
});

const deserializeNode = (row: any) => ({
  id: row.id,
  key: row.nodeKey,
  type: row.nodeType,
  label: row.label,
  canonicalName: row.canonicalName,
  zhName: row.zhName,
  localId: row.localId,
  sourceDocumentId: row.sourceDocumentId,
  data: parse(row.dataJson, {}),
  evidence: parse(row.evidenceJson, []),
  confidence: row.confidence,
  reviewStatus: row.reviewStatus
});

const deserializeEdge = (row: any) => ({
  id: row.id,
  key: row.edgeKey,
  type: row.edgeType,
  from: row.fromNodeId,
  to: row.toNodeId,
  sourceDocumentId: row.sourceDocumentId,
  sourceRecordType: row.sourceRecordType,
  sourceRecordId: row.sourceRecordId,
  evidence: parse(row.evidenceJson, []),
  confidence: row.confidence,
  reviewStatus: row.reviewStatus
});

const queryTokens = (value: unknown) => {
  const input = text(value, 1800).toLowerCase();
  const tokens = new Set<string>();
  for (const token of input.match(/[a-z0-9][a-z0-9+._-]{1,}/gi) || []) tokens.add(token);
  for (const chunk of input.match(/[\p{Script=Han}]{2,}/gu) || []) {
    if (chunk.length <= 16) tokens.add(chunk);
    for (const size of [4, 3, 2]) {
      for (let index = 0; index <= chunk.length - size; index += 1) {
        tokens.add(chunk.slice(index, index + size));
      }
    }
  }
  return Array.from(tokens).sort((a, b) => b.length - a.length).slice(0, 60);
};

export class ResearchGraphService {
  async readArtifactsFromDirectory(directory: string) {
    const entries = (await fs.readdir(directory, { withFileTypes: true }))
      .filter((entry) => entry.isFile() && entry.name.toLowerCase().endsWith('.json'))
      .sort((a, b) => a.name.localeCompare(b.name));
    const artifacts: StageOneArtifact[] = [];
    const errors: Array<{ file: string; error: string }> = [];
    for (const entry of entries) {
      const file = path.join(directory, entry.name);
      try {
        artifacts.push(asArtifact(JSON.parse(await fs.readFile(file, 'utf8'))));
      } catch (error) {
        errors.push({ file, error: error instanceof Error ? error.message : String(error) });
      }
    }
    return { artifacts, errors };
  }

  async importArtifacts(
    workspaceId: string,
    values: unknown[],
    options: { allowedSystems?: string[]; replaceWorkspace?: boolean; researchArticlesOnly?: boolean } = {}
  ) {
    const allowed = new Set((options.allowedSystems || ['photocatalysis', 'both']).map((item) => item.toLowerCase()));
    const artifacts = values.map(asArtifact);
    const accepted = artifacts.filter((artifact) => {
      const paper = artifact.extraction.paper;
      if (!allowed.has(text(paper.catalysis_system, 80).toLowerCase())) return false;
      return !options.researchArticlesOnly || paper.paper_type === 'research_article';
    });

    const attempted = { documents: 0, nodes: 0, edges: 0 };
    await prisma.$transaction(async (tx: any) => {
      if (options.replaceWorkspace) {
        await tx.$executeRawUnsafe('DELETE FROM "ResearchGraphEdge" WHERE "workspaceId" = ?', workspaceId);
        await tx.$executeRawUnsafe('DELETE FROM "ResearchGraphNode" WHERE "workspaceId" = ?', workspaceId);
        await tx.$executeRawUnsafe('DELETE FROM "ResearchCorpusDocument" WHERE "workspaceId" = ?', workspaceId);
      }

      const insertNode = async (input: {
        nodeKey: string; nodeType: string; label: string; canonicalName?: string; zhName?: string;
        localId?: string | null; data?: JsonObject; evidence?: JsonObject[]; confidence?: number;
        reviewStatus?: string; sourceDocumentId?: string | null;
      }) => {
        const id = idFor('research-node', workspaceId, input.nodeKey);
        await tx.$executeRawUnsafe(
          `INSERT INTO "ResearchGraphNode" (
            "id","nodeKey","nodeType","label","canonicalName","zhName","localId","dataJson","evidenceJson",
            "confidence","reviewStatus","workspaceId","sourceDocumentId","updatedAt"
          ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
          ON CONFLICT("workspaceId","nodeKey") DO UPDATE SET
            "label"=excluded."label","canonicalName"=excluded."canonicalName","zhName"=excluded."zhName",
            "dataJson"=excluded."dataJson","evidenceJson"=excluded."evidenceJson",
            "confidence"=MAX("ResearchGraphNode"."confidence",excluded."confidence"),
            "reviewStatus"=CASE WHEN excluded."reviewStatus"='needs_review' THEN 'needs_review' ELSE "ResearchGraphNode"."reviewStatus" END,
            "updatedAt"=CURRENT_TIMESTAMP`,
          id, input.nodeKey, input.nodeType, input.label, input.canonicalName || '', input.zhName || '',
          input.localId || null, stringify(input.data || {}), stringify(input.evidence || [], []),
          clamp01(input.confidence, 0.75), input.reviewStatus || 'extracted', workspaceId,
          input.sourceDocumentId || null
        );
        attempted.nodes += 1;
        return id;
      };

      const insertEdge = async (input: {
        edgeType: string; fromNodeId: string; toNodeId: string; sourceDocumentId: string;
        sourceRecordType: string; sourceRecordId?: string | null; evidence?: JsonObject[];
        confidence?: number; reviewStatus?: string;
      }) => {
        if (!input.fromNodeId || !input.toNodeId || input.fromNodeId === input.toNodeId) return;
        const edgeKey = stableHash([
          input.edgeType, input.fromNodeId, input.toNodeId, input.sourceDocumentId,
          input.sourceRecordType, input.sourceRecordId || ''
        ]).slice(0, 36);
        await tx.$executeRawUnsafe(
          `INSERT INTO "ResearchGraphEdge" (
            "id","edgeKey","edgeType","fromNodeId","toNodeId","sourceRecordType","sourceRecordId",
            "evidenceJson","confidence","reviewStatus","workspaceId","sourceDocumentId","updatedAt"
          ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
          ON CONFLICT("workspaceId","edgeKey") DO UPDATE SET
            "evidenceJson"=excluded."evidenceJson","confidence"=excluded."confidence",
            "reviewStatus"=excluded."reviewStatus","status"='active',"updatedAt"=CURRENT_TIMESTAMP`,
          idFor('research-edge', workspaceId, edgeKey), edgeKey, input.edgeType, input.fromNodeId,
          input.toNodeId, input.sourceRecordType, input.sourceRecordId || null,
          stringify(input.evidence || [], []), clamp01(input.confidence, 0.75),
          input.reviewStatus || 'extracted', workspaceId, input.sourceDocumentId
        );
        attempted.edges += 1;
      };

      for (const artifact of accepted) {
        const extraction = artifact.extraction;
        const paper = extraction.paper;
        const documentKey = documentKeyFor(paper, artifact.source);
        const documentId = idFor('research-document', workspaceId, documentKey);
        await tx.$executeRawUnsafe(
          `INSERT INTO "ResearchCorpusDocument" (
            "id","documentKey","title","doi","year","journal","paperType","catalysisSystem",
            "reactionCategoriesJson","sourcePath","sourceSha256","pageCount","abstractJson","summaryJson",
            "qualityJson","metadataJson","workspaceId","updatedAt"
          ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
          ON CONFLICT("workspaceId","documentKey") DO UPDATE SET
            "title"=excluded."title","doi"=excluded."doi","year"=excluded."year","journal"=excluded."journal",
            "paperType"=excluded."paperType","catalysisSystem"=excluded."catalysisSystem",
            "reactionCategoriesJson"=excluded."reactionCategoriesJson","sourcePath"=excluded."sourcePath",
            "sourceSha256"=excluded."sourceSha256","pageCount"=excluded."pageCount",
            "abstractJson"=excluded."abstractJson","summaryJson"=excluded."summaryJson",
            "qualityJson"=excluded."qualityJson","metadataJson"=excluded."metadataJson",
            "status"='active',"updatedAt"=CURRENT_TIMESTAMP`,
          documentId, documentKey, text(paper.title, 600) || documentKey, text(paper.doi, 240) || null,
          Number.isFinite(Number(paper.year)) ? Number(paper.year) : null, text(paper.journal, 300) || null,
          text(paper.paper_type, 80) || null, text(paper.catalysis_system, 80) || 'unclear',
          stringify(paper.reaction_categories || [], []), text(paper.source_path || artifact.source?.path, 900),
          text(paper.source_pdf_sha256 || artifact.source?.source_pdf_sha256, 128),
          Number.isFinite(Number(paper.page_count || artifact.source?.page_count))
            ? Number(paper.page_count || artifact.source?.page_count) : null,
          stringify(extraction.abstract || {}), stringify(extraction.summary || {}),
          stringify(extraction.quality || {}),
          stringify({
            schemaVersion: extraction.schema_version,
            extractionMetadata: extraction.extraction_metadata || {},
            visualReviewItems: extraction.visual_review_items || []
          }),
          workspaceId
        );
        await tx.$executeRawUnsafe(
          'DELETE FROM "ResearchGraphEdge" WHERE "workspaceId"=? AND "sourceDocumentId"=?',
          workspaceId, documentId
        );
        await tx.$executeRawUnsafe(
          'DELETE FROM "ResearchGraphNode" WHERE "workspaceId"=? AND "sourceDocumentId"=?',
          workspaceId, documentId
        );
        attempted.documents += 1;

        const paperId = await insertNode({
          nodeKey: `paper:${stableHash(documentKey).slice(0, 28)}`,
          nodeType: 'paper',
          label: text(paper.title, 600) || documentKey,
          canonicalName: text(paper.title, 600),
          localId: documentKey,
          data: paper,
          confidence: 1,
          sourceDocumentId: documentId
        });

        const entityIds = new Map<string, string>();
        for (const entity of extraction.entities || []) {
          const canonical = text(entity.canonical_name || entity.raw_term || entity.zh_name, 300);
          const zhName = text(entity.zh_name || entity.normalized_term, 300);
          if (!canonical && !zhName) continue;
          const nodeId = await insertNode({
            nodeKey: globalNodeKey('entity', entity.type, canonical, zhName),
            nodeType: 'entity',
            label: zhName || canonical,
            canonicalName: canonical,
            zhName,
            localId: text(entity.id, 160) || null,
            data: entity,
            evidence: evidenceFor(entity),
            confidence: confidenceFor(entity),
            reviewStatus: reviewStatusFor(entity)
          });
          if (entity.id) entityIds.set(String(entity.id), nodeId);
          await insertEdge({
            edgeType: 'PAPER_MENTIONS_ENTITY', fromNodeId: paperId, toNodeId: nodeId,
            sourceDocumentId: documentId, sourceRecordType: 'entity', sourceRecordId: entity.id,
            evidence: evidenceFor(entity), confidence: confidenceFor(entity), reviewStatus: reviewStatusFor(entity)
          });
        }

        for (const keyword of extraction.keywords?.extracted || []) {
          const normalized = text(keyword.normalized_term || keyword.raw_term, 300);
          const raw = text(keyword.raw_term, 300);
          if (!normalized && !raw) continue;
          const nodeId = await insertNode({
            nodeKey: globalNodeKey('keyword', keyword.category, normalized, raw),
            nodeType: 'keyword',
            label: normalized || raw,
            canonicalName: raw,
            zhName: normalized,
            localId: text(keyword.id, 160) || null,
            data: keyword,
            evidence: evidenceFor(keyword),
            confidence: confidenceFor(keyword),
            reviewStatus: reviewStatusFor(keyword)
          });
          await insertEdge({
            edgeType: 'PAPER_HAS_KEYWORD', fromNodeId: paperId, toNodeId: nodeId,
            sourceDocumentId: documentId, sourceRecordType: 'keyword', sourceRecordId: keyword.id,
            evidence: evidenceFor(keyword), confidence: confidenceFor(keyword), reviewStatus: reviewStatusFor(keyword)
          });
        }

        const experimentIds = new Map<string, string>();
        for (const experiment of extraction.experiments || []) {
          if (!experiment.id) continue;
          const nodeId = await insertNode({
            nodeKey: paperNodeKey('experiment', documentKey, experiment.id),
            nodeType: 'experiment',
            label: text(experiment.objective, 360) || `${text(experiment.experiment_type, 80) || '实验'} ${experiment.id}`,
            canonicalName: text(experiment.experiment_type, 120),
            localId: text(experiment.id, 160),
            data: experiment,
            evidence: evidenceFor(experiment),
            confidence: confidenceFor(experiment),
            reviewStatus: reviewStatusFor(experiment),
            sourceDocumentId: documentId
          });
          experimentIds.set(String(experiment.id), nodeId);
          await insertEdge({
            edgeType: 'PAPER_REPORTS_EXPERIMENT', fromNodeId: paperId, toNodeId: nodeId,
            sourceDocumentId: documentId, sourceRecordType: 'experiment', sourceRecordId: experiment.id,
            evidence: evidenceFor(experiment), confidence: confidenceFor(experiment), reviewStatus: reviewStatusFor(experiment)
          });
          for (const [field, edgeType] of [
            ['sample_entity_ids', 'EXPERIMENT_USES_SAMPLE'],
            ['material_entity_ids', 'EXPERIMENT_USES_MATERIAL'],
            ['method_entity_ids', 'EXPERIMENT_USES_METHOD']
          ] as const) {
            for (const localId of Array.isArray(experiment[field]) ? experiment[field] : []) {
              const target = entityIds.get(String(localId));
              if (target) await insertEdge({
                edgeType, fromNodeId: nodeId, toNodeId: target, sourceDocumentId: documentId,
                sourceRecordType: 'experiment', sourceRecordId: experiment.id,
                evidence: evidenceFor(experiment), confidence: confidenceFor(experiment),
                reviewStatus: reviewStatusFor(experiment)
              });
            }
          }
        }

        for (const observation of extraction.observations || []) {
          if (!observation.id) continue;
          const nodeId = await insertNode({
            nodeKey: paperNodeKey('observation', documentKey, observation.id),
            nodeType: 'observation',
            label: text(observation.metric_name, 240) || String(observation.id),
            canonicalName: text(observation.metric_name, 240),
            localId: text(observation.id, 160),
            data: observation,
            evidence: evidenceFor(observation),
            confidence: confidenceFor(observation),
            reviewStatus: reviewStatusFor(observation),
            sourceDocumentId: documentId
          });
          const experimentId = experimentIds.get(String(observation.experiment_id || ''));
          await insertEdge({
            edgeType: experimentId ? 'EXPERIMENT_PRODUCES_OBSERVATION' : 'PAPER_REPORTS_OBSERVATION',
            fromNodeId: experimentId || paperId, toNodeId: nodeId, sourceDocumentId: documentId,
            sourceRecordType: 'observation', sourceRecordId: observation.id,
            evidence: evidenceFor(observation), confidence: confidenceFor(observation),
            reviewStatus: reviewStatusFor(observation)
          });
          for (const [field, edgeType] of [
            ['sample_entity_id', 'OBSERVATION_OF_SAMPLE'],
            ['property_entity_id', 'OBSERVATION_MEASURES_PROPERTY'],
            ['method_entity_id', 'OBSERVATION_MEASURED_BY']
          ] as const) {
            const target = entityIds.get(String(observation[field] || ''));
            if (target) await insertEdge({
              edgeType, fromNodeId: nodeId, toNodeId: target, sourceDocumentId: documentId,
              sourceRecordType: 'observation', sourceRecordId: observation.id,
              evidence: evidenceFor(observation), confidence: confidenceFor(observation),
              reviewStatus: reviewStatusFor(observation)
            });
          }
        }

        for (const claim of extraction.claims || []) {
          if (!claim.id) continue;
          const nodeId = await insertNode({
            nodeKey: paperNodeKey('claim', documentKey, claim.id),
            nodeType: 'claim',
            label: text(claim.statement, 600) || String(claim.id),
            canonicalName: text(claim.claim_type, 120),
            localId: text(claim.id, 160),
            data: claim,
            evidence: evidenceFor(claim),
            confidence: confidenceFor(claim),
            reviewStatus: reviewStatusFor(claim),
            sourceDocumentId: documentId
          });
          await insertEdge({
            edgeType: 'PAPER_ASSERTS_CLAIM', fromNodeId: paperId, toNodeId: nodeId,
            sourceDocumentId: documentId, sourceRecordType: 'claim', sourceRecordId: claim.id,
            evidence: evidenceFor(claim), confidence: confidenceFor(claim), reviewStatus: reviewStatusFor(claim)
          });
        }
      }

      await tx.$executeRawUnsafe(
        `DELETE FROM "ResearchGraphNode"
         WHERE "workspaceId"=? AND "sourceDocumentId" IS NULL
           AND NOT EXISTS (
             SELECT 1 FROM "ResearchGraphEdge" e
             WHERE e."fromNodeId"="ResearchGraphNode"."id" OR e."toNodeId"="ResearchGraphNode"."id"
           )`,
        workspaceId
      );
    }, { maxWait: 30000, timeout: 900000 });

    return {
      inputDocuments: artifacts.length,
      acceptedDocuments: accepted.length,
      skippedDocuments: artifacts.length - accepted.length,
      attempted,
      graph: await this.getStats(workspaceId)
    };
  }

  async getStats(workspaceId: string) {
    const documents = await prisma.$queryRawUnsafe<Array<any>>(
      `SELECT "catalysisSystem","paperType",COUNT(*) AS count
       FROM "ResearchCorpusDocument" WHERE "workspaceId"=? AND "status"='active'
       GROUP BY "catalysisSystem","paperType"`,
      workspaceId
    );
    const nodes = await prisma.$queryRawUnsafe<Array<any>>(
      `SELECT "nodeType",COUNT(*) AS count FROM "ResearchGraphNode"
       WHERE "workspaceId"=? GROUP BY "nodeType"`,
      workspaceId
    );
    const edges = await prisma.$queryRawUnsafe<Array<any>>(
      `SELECT "edgeType",COUNT(*) AS count FROM "ResearchGraphEdge"
       WHERE "workspaceId"=? AND "status"='active' GROUP BY "edgeType"`,
      workspaceId
    );
    return {
      documents: documents.reduce((sum, row) => sum + Number(row.count), 0),
      documentBreakdown: documents.map((row) => ({ ...row, count: Number(row.count) })),
      nodes: Object.fromEntries(nodes.map((row) => [row.nodeType, Number(row.count)])),
      edges: Object.fromEntries(edges.map((row) => [row.edgeType, Number(row.count)])),
      nodeCount: nodes.reduce((sum, row) => sum + Number(row.count), 0),
      edgeCount: edges.reduce((sum, row) => sum + Number(row.count), 0)
    };
  }

  async getGraph(input: { workspaceId: string; search?: string; nodeTypes?: string[]; limit?: number }) {
    const where = ['"workspaceId"=?'];
    const params: unknown[] = [input.workspaceId];
    if (input.nodeTypes?.length) {
      where.push(`"nodeType" IN (${input.nodeTypes.map(() => '?').join(',')})`);
      params.push(...input.nodeTypes);
    }
    if (text(input.search, 300)) {
      const needle = `%${text(input.search, 300).toLowerCase()}%`;
      where.push('(LOWER("label") LIKE ? OR LOWER("canonicalName") LIKE ? OR LOWER("zhName") LIKE ? OR LOWER("dataJson") LIKE ?)');
      params.push(needle, needle, needle, needle);
    }
    params.push(Math.max(20, Math.min(600, Number(input.limit || 320))));
    const nodeRows = await prisma.$queryRawUnsafe<Array<any>>(
      `SELECT * FROM "ResearchGraphNode" WHERE ${where.join(' AND ')}
       ORDER BY "confidence" DESC,"updatedAt" DESC LIMIT ?`,
      ...params
    );
    const ids = nodeRows.map((row) => row.id);
    const edgeRows = ids.length
      ? await prisma.$queryRawUnsafe<Array<any>>(
          `SELECT * FROM "ResearchGraphEdge"
           WHERE "workspaceId"=? AND "status"='active'
             AND "fromNodeId" IN (${ids.map(() => '?').join(',')})
             AND "toNodeId" IN (${ids.map(() => '?').join(',')})
           ORDER BY "confidence" DESC`,
          input.workspaceId, ...ids, ...ids
        )
      : [];
    const documentIds = Array.from(new Set([
      ...nodeRows.map((row) => row.sourceDocumentId),
      ...edgeRows.map((row) => row.sourceDocumentId)
    ].filter(Boolean)));
    const documents = documentIds.length
      ? await prisma.$queryRawUnsafe<Array<any>>(
          `SELECT * FROM "ResearchCorpusDocument" WHERE "workspaceId"=?
           AND "id" IN (${documentIds.map(() => '?').join(',')})`,
          input.workspaceId, ...documentIds
        )
      : [];
    return {
      nodes: nodeRows.map(deserializeNode),
      edges: edgeRows.map(deserializeEdge),
      documents: documents.map(deserializeDocument)
    };
  }

  async buildEvidenceContext(input: {
    workspaceId: string;
    corpusWorkspaceId?: string;
    query: string;
    experimentId?: string | null;
    limit?: number;
  }) {
    const experiment = input.experimentId ? await this.getExperiment(input.workspaceId, input.experimentId) : null;
    const corpusWorkspaceId = input.corpusWorkspaceId || input.workspaceId;
    const tokens = queryTokens(`${input.query} ${experiment ? stringify(experiment) : ''}`);
    const params: unknown[] = [corpusWorkspaceId];
    const where = ['"workspaceId"=?', `"nodeType" IN ('claim','observation','experiment','entity','keyword')`];
    if (tokens.length) {
      where.push(`(${tokens.map(() => '(LOWER("label") LIKE ? OR LOWER("dataJson") LIKE ?)').join(' OR ')})`);
      for (const token of tokens) params.push(`%${token}%`, `%${token}%`);
    }
    const limit = Math.max(20, Math.min(120, Number(input.limit || 36)));
    params.push(Math.min(480, limit * 4));
    let rows = await prisma.$queryRawUnsafe<Array<any>>(
      `SELECT * FROM "ResearchGraphNode" WHERE ${where.join(' AND ')}
       ORDER BY "confidence" DESC LIMIT ?`,
      ...params
    );
    if (!rows.length) {
      rows = await prisma.$queryRawUnsafe<Array<any>>(
        `SELECT * FROM "ResearchGraphNode" WHERE "workspaceId"=?
         AND "nodeType" IN ('claim','observation','experiment')
         ORDER BY "confidence" DESC,"updatedAt" DESC LIMIT ?`,
        corpusWorkspaceId, limit
      );
    } else {
      rows = rows.map((row) => {
        const haystack = `${row.label} ${row.canonicalName} ${row.zhName} ${row.dataJson}`.toLowerCase();
        const relevance = tokens.reduce((score, token) => score + (haystack.includes(token) ? token.length ** 2 : 0), 0);
        return { row, relevance };
      }).sort((a, b) => b.relevance - a.relevance || Number(b.row.confidence) - Number(a.row.confidence))
        .slice(0, limit).map((item) => item.row);
    }
    const documentIds = Array.from(new Set(rows.map((row) => row.sourceDocumentId).filter(Boolean)));
    const documents = documentIds.length
      ? await prisma.$queryRawUnsafe<Array<any>>(
          `SELECT * FROM "ResearchCorpusDocument" WHERE "workspaceId"=?
           AND "id" IN (${documentIds.map(() => '?').join(',')})`,
          corpusWorkspaceId, ...documentIds
        )
      : [];
    const previousAdvice = experiment
      ? await prisma.$queryRawUnsafe<Array<any>>(
          `SELECT "id","responseJson","createdAt" FROM "ResearchAdviceRun"
           WHERE "workspaceId"=? AND "experimentLogId"=? AND "status"='completed'
           ORDER BY "createdAt" DESC LIMIT 4`,
          input.workspaceId, input.experimentId
        )
      : [];
    return {
      nodes: rows.map(deserializeNode),
      documents: documents.map(deserializeDocument),
      currentExperiment: experiment,
      previousAdviceRuns: previousAdvice.map((row) => ({
        id: row.id,
        response: parse(row.responseJson, {}),
        createdAt: row.createdAt
      }))
    };
  }

  async saveExperiment(workspaceId: string, input: JsonObject) {
    const existingId = text(input.id, 160);
    const id = existingId || `research-experiment-${stableHash([workspaceId, Date.now(), input.title]).slice(0, 28)}`;
    const title = text(input.title, 400);
    if (!title) throw new Error('实验标题不能为空');
    await prisma.$executeRawUnsafe(
      `INSERT INTO "ResearchExperimentLog" (
        "id","title","objective","status","materialsJson","procedureJson","conditionsJson",
        "observationsJson","outcomeJson","constraintsJson","source","workspaceId","updatedAt"
      ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
      ON CONFLICT("id") DO UPDATE SET
        "title"=excluded."title","objective"=excluded."objective","status"=excluded."status",
        "materialsJson"=excluded."materialsJson","procedureJson"=excluded."procedureJson",
        "conditionsJson"=excluded."conditionsJson","observationsJson"=excluded."observationsJson",
        "outcomeJson"=excluded."outcomeJson","constraintsJson"=excluded."constraintsJson",
        "source"=excluded."source","updatedAt"=CURRENT_TIMESTAMP`,
      id, title, text(input.objective, 1600), text(input.status, 80) || 'planned',
      stringify(input.materials || [], []), stringify(input.procedure || [], []),
      stringify(input.conditions || {}), stringify(input.observations || [], []),
      stringify(input.outcome || {}), stringify(input.constraints || {}),
      text(input.source, 80) || 'user', workspaceId
    );
    return this.getExperiment(workspaceId, id);
  }

  async getExperiment(workspaceId: string, id: string) {
    const row = (await prisma.$queryRawUnsafe<Array<any>>(
      'SELECT * FROM "ResearchExperimentLog" WHERE "workspaceId"=? AND "id"=? LIMIT 1',
      workspaceId, id
    ))[0];
    return row ? {
      id: row.id,
      title: row.title,
      objective: row.objective,
      status: row.status,
      materials: parse(row.materialsJson, []),
      procedure: parse(row.procedureJson, []),
      conditions: parse(row.conditionsJson, {}),
      observations: parse(row.observationsJson, []),
      outcome: parse(row.outcomeJson, {}),
      constraints: parse(row.constraintsJson, {}),
      source: row.source,
      createdAt: row.createdAt,
      updatedAt: row.updatedAt
    } : null;
  }

  async listExperiments(workspaceId: string, limit = 50) {
    const rows = await prisma.$queryRawUnsafe<Array<any>>(
      'SELECT "id" FROM "ResearchExperimentLog" WHERE "workspaceId"=? ORDER BY "updatedAt" DESC LIMIT ?',
      workspaceId, Math.max(1, Math.min(200, limit))
    );
    return Promise.all(rows.map((row) => this.getExperiment(workspaceId, row.id)));
  }

  async createAdviceRun(workspaceId: string, experimentId: string | null, request: JsonObject, context: JsonObject) {
    const id = `research-advice-${stableHash([workspaceId, Date.now(), request]).slice(0, 28)}`;
    await prisma.$executeRawUnsafe(
      `INSERT INTO "ResearchAdviceRun"
       ("id","status","requestJson","contextJson","workspaceId","experimentLogId","updatedAt")
       VALUES (?,'running',?,?,?,?,CURRENT_TIMESTAMP)`,
      id, stringify(request), stringify(context), workspaceId, experimentId
    );
    return id;
  }

  async completeAdviceRun(id: string, response: ResearchAdvicePayload, metadata: JsonObject) {
    await prisma.$executeRawUnsafe(
      `UPDATE "ResearchAdviceRun" SET "status"='completed',"responseJson"=?,
       "provider"=?,"model"=?,"usageJson"=?,"error"=NULL,"updatedAt"=CURRENT_TIMESTAMP WHERE "id"=?`,
      stringify(response), text(metadata.provider, 80), text(metadata.model, 160),
      stringify(metadata.usage || {}), id
    );
  }

  async failAdviceRun(id: string, error: unknown) {
    await prisma.$executeRawUnsafe(
      `UPDATE "ResearchAdviceRun" SET "status"='failed',"error"=?,"updatedAt"=CURRENT_TIMESTAMP WHERE "id"=?`,
      error instanceof Error ? error.message : String(error), id
    );
  }

  async getAdviceRun(workspaceId: string, id: string) {
    const row = (await prisma.$queryRawUnsafe<Array<any>>(
      'SELECT * FROM "ResearchAdviceRun" WHERE "workspaceId"=? AND "id"=? LIMIT 1',
      workspaceId, id
    ))[0];
    return row ? {
      id: row.id,
      status: row.status,
      request: parse(row.requestJson, {}),
      context: parse(row.contextJson, {}),
      response: parse(row.responseJson, {}),
      provider: row.provider,
      model: row.model,
      usage: parse(row.usageJson, {}),
      error: row.error,
      experimentId: row.experimentLogId,
      createdAt: row.createdAt,
      updatedAt: row.updatedAt
    } : null;
  }

  async updateAdviceResponse(id: string, response: ResearchAdvicePayload) {
    await prisma.$executeRawUnsafe(
      `UPDATE "ResearchAdviceRun" SET "responseJson"=?,"updatedAt"=CURRENT_TIMESTAMP WHERE "id"=?`,
      stringify(response), id
    );
  }
}

export const researchGraphService = new ResearchGraphService();

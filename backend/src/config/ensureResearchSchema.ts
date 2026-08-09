import prisma from './db';

const statements = [
  `CREATE TABLE IF NOT EXISTS "ResearchCorpusDocument" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "documentKey" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "doi" TEXT,
    "year" INTEGER,
    "journal" TEXT,
    "paperType" TEXT,
    "catalysisSystem" TEXT NOT NULL DEFAULT 'unclear',
    "reactionCategoriesJson" TEXT NOT NULL DEFAULT '[]',
    "sourcePath" TEXT NOT NULL DEFAULT '',
    "sourceSha256" TEXT NOT NULL DEFAULT '',
    "pageCount" INTEGER,
    "abstractJson" TEXT NOT NULL DEFAULT '{}',
    "summaryJson" TEXT NOT NULL DEFAULT '{}',
    "qualityJson" TEXT NOT NULL DEFAULT '{}',
    "metadataJson" TEXT NOT NULL DEFAULT '{}',
    "status" TEXT NOT NULL DEFAULT 'active',
    "importedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "workspaceId" TEXT NOT NULL,
    FOREIGN KEY ("workspaceId") REFERENCES "Workspace" ("id") ON DELETE CASCADE
  )`,
  `CREATE UNIQUE INDEX IF NOT EXISTS "ResearchCorpusDocument_workspace_document_key"
    ON "ResearchCorpusDocument"("workspaceId", "documentKey")`,
  `CREATE INDEX IF NOT EXISTS "ResearchCorpusDocument_workspace_system_idx"
    ON "ResearchCorpusDocument"("workspaceId", "catalysisSystem")`,
  `CREATE TABLE IF NOT EXISTS "ResearchGraphNode" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "nodeKey" TEXT NOT NULL,
    "nodeType" TEXT NOT NULL,
    "label" TEXT NOT NULL,
    "canonicalName" TEXT NOT NULL DEFAULT '',
    "zhName" TEXT NOT NULL DEFAULT '',
    "localId" TEXT,
    "dataJson" TEXT NOT NULL DEFAULT '{}',
    "evidenceJson" TEXT NOT NULL DEFAULT '[]',
    "confidence" REAL NOT NULL DEFAULT 0.75,
    "reviewStatus" TEXT NOT NULL DEFAULT 'extracted',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "workspaceId" TEXT NOT NULL,
    "sourceDocumentId" TEXT,
    FOREIGN KEY ("workspaceId") REFERENCES "Workspace" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("sourceDocumentId") REFERENCES "ResearchCorpusDocument" ("id") ON DELETE CASCADE
  )`,
  `CREATE UNIQUE INDEX IF NOT EXISTS "ResearchGraphNode_workspace_node_key"
    ON "ResearchGraphNode"("workspaceId", "nodeKey")`,
  `CREATE INDEX IF NOT EXISTS "ResearchGraphNode_workspace_type_label_idx"
    ON "ResearchGraphNode"("workspaceId", "nodeType", "label")`,
  `CREATE TABLE IF NOT EXISTS "ResearchGraphEdge" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "edgeKey" TEXT NOT NULL,
    "edgeType" TEXT NOT NULL,
    "fromNodeId" TEXT NOT NULL,
    "toNodeId" TEXT NOT NULL,
    "sourceRecordType" TEXT NOT NULL DEFAULT '',
    "sourceRecordId" TEXT,
    "evidenceJson" TEXT NOT NULL DEFAULT '[]',
    "confidence" REAL NOT NULL DEFAULT 0.75,
    "reviewStatus" TEXT NOT NULL DEFAULT 'extracted',
    "status" TEXT NOT NULL DEFAULT 'active',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "workspaceId" TEXT NOT NULL,
    "sourceDocumentId" TEXT,
    FOREIGN KEY ("workspaceId") REFERENCES "Workspace" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("fromNodeId") REFERENCES "ResearchGraphNode" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("toNodeId") REFERENCES "ResearchGraphNode" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("sourceDocumentId") REFERENCES "ResearchCorpusDocument" ("id") ON DELETE CASCADE
  )`,
  `CREATE UNIQUE INDEX IF NOT EXISTS "ResearchGraphEdge_workspace_edge_key"
    ON "ResearchGraphEdge"("workspaceId", "edgeKey")`,
  `CREATE INDEX IF NOT EXISTS "ResearchGraphEdge_workspace_type_idx"
    ON "ResearchGraphEdge"("workspaceId", "edgeType")`,
  `CREATE TABLE IF NOT EXISTS "ResearchExperimentLog" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "objective" TEXT NOT NULL DEFAULT '',
    "status" TEXT NOT NULL DEFAULT 'planned',
    "materialsJson" TEXT NOT NULL DEFAULT '[]',
    "procedureJson" TEXT NOT NULL DEFAULT '[]',
    "conditionsJson" TEXT NOT NULL DEFAULT '{}',
    "observationsJson" TEXT NOT NULL DEFAULT '[]',
    "outcomeJson" TEXT NOT NULL DEFAULT '{}',
    "constraintsJson" TEXT NOT NULL DEFAULT '{}',
    "source" TEXT NOT NULL DEFAULT 'user',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "workspaceId" TEXT NOT NULL,
    FOREIGN KEY ("workspaceId") REFERENCES "Workspace" ("id") ON DELETE CASCADE
  )`,
  `CREATE INDEX IF NOT EXISTS "ResearchExperimentLog_workspace_status_idx"
    ON "ResearchExperimentLog"("workspaceId", "status", "updatedAt")`,
  `CREATE TABLE IF NOT EXISTS "ResearchAdviceRun" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "status" TEXT NOT NULL DEFAULT 'running',
    "requestJson" TEXT NOT NULL DEFAULT '{}',
    "contextJson" TEXT NOT NULL DEFAULT '{}',
    "responseJson" TEXT NOT NULL DEFAULT '{}',
    "provider" TEXT,
    "model" TEXT,
    "usageJson" TEXT NOT NULL DEFAULT '{}',
    "error" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "workspaceId" TEXT NOT NULL,
    "experimentLogId" TEXT,
    FOREIGN KEY ("workspaceId") REFERENCES "Workspace" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("experimentLogId") REFERENCES "ResearchExperimentLog" ("id") ON DELETE SET NULL
  )`,
  `CREATE INDEX IF NOT EXISTS "ResearchAdviceRun_workspace_status_idx"
    ON "ResearchAdviceRun"("workspaceId", "status", "createdAt")`
];

export const ensureResearchSchema = async () => {
  for (const statement of statements) {
    await prisma.$executeRawUnsafe(statement);
  }
};

import '../config/env';
import prisma, { configureDatabase } from '../config/db';
import { ensureResearchSchema } from '../config/ensureResearchSchema';
import { researchGraphService } from '../services/researchGraphService';

const main = async () => {
  await configureDatabase();
  await ensureResearchSchema();
  const workspaces = await prisma.workspace.findMany({ orderBy: { catalysisSystem: 'asc' } });
  const results = [];
  for (const workspace of workspaces) {
    const corpusWorkspaceId = workspace.corpusWorkspaceId || workspace.id;
    const stats = await researchGraphService.getStats(corpusWorkspaceId);
    const checks = await prisma.$queryRawUnsafe<Array<{ checkName: string; count: number }>>(
      `SELECT 'dangling_from' AS checkName, COUNT(*) AS count
       FROM "ResearchGraphEdge" e LEFT JOIN "ResearchGraphNode" n ON n."id"=e."fromNodeId"
       WHERE e."workspaceId"=? AND n."id" IS NULL
       UNION ALL
       SELECT 'dangling_to', COUNT(*)
       FROM "ResearchGraphEdge" e LEFT JOIN "ResearchGraphNode" n ON n."id"=e."toNodeId"
       WHERE e."workspaceId"=? AND n."id" IS NULL
       UNION ALL
       SELECT 'self_loops', COUNT(*) FROM "ResearchGraphEdge"
       WHERE "workspaceId"=? AND "fromNodeId"="toNodeId"`,
      corpusWorkspaceId, corpusWorkspaceId, corpusWorkspaceId
    );
    results.push({
      workspace,
      corpusWorkspaceId,
      stats,
      checks: checks.map((item) => ({ ...item, count: Number(item.count) }))
    });
  }
  const quickCheck = await prisma.$queryRawUnsafe<Array<{ quick_check: string }>>('PRAGMA quick_check');
  console.log(JSON.stringify({ ok: true, quickCheck, results }, null, 2));
};

main()
  .catch((error) => {
    console.error(error instanceof Error ? error.message : error);
    process.exitCode = 1;
  })
  .finally(async () => prisma.$disconnect());

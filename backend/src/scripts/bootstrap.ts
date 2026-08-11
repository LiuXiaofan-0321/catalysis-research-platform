import '../config/env';
import { CATALYSIS_PLATFORMS } from '../config/catalysisPlatforms';
import prisma, { configureDatabase } from '../config/db';
import { ensureResearchSchema } from '../config/ensureResearchSchema';
import { hashPassword } from '../utils/hash';

const main = async () => {
  await configureDatabase();
  await ensureResearchSchema();
  const username = process.env.INITIAL_ADMIN_USERNAME?.trim() || 'admin';
  const email = process.env.INITIAL_ADMIN_EMAIL?.trim().toLowerCase() || 'admin@example.com';
  const password = process.env.INITIAL_ADMIN_PASSWORD || '';
  let user = await prisma.user.findFirst({ where: { OR: [{ username }, { email }] } });
  if (!user) {
    if (password.length < 8) {
      throw new Error('首次初始化请设置至少8位的 INITIAL_ADMIN_PASSWORD');
    }
    user = await prisma.user.create({
      data: {
        username,
        email,
        displayName: username,
        password: hashPassword(password)
      }
    });
  }
  await prisma.researcherProfile.upsert({
    where: { userId: user.id },
    update: {},
    create: {
      userId: user.id,
      primaryCatalysis: 'both',
      researchInterestsJson: JSON.stringify(['分子筛催化', '催化机理', '实验闭环']),
      catalystSystemsJson: JSON.stringify(['photocatalysis', 'thermal_catalysis']),
      onboardingCompletedAt: new Date()
    }
  });
  for (const workspace of CATALYSIS_PLATFORMS) {
    await prisma.workspace.upsert({
      where: { id: workspace.id },
      update: {
        name: workspace.name,
        description: workspace.description,
        catalysisSystem: workspace.catalysisSystem,
        corpusWorkspaceId: workspace.id,
        userId: user.id
      },
      create: {
        ...workspace,
        corpusWorkspaceId: workspace.id,
        userId: user.id
      }
    });
  }
  console.log(JSON.stringify({
    ok: true,
    username: user.username,
    workspaces: await prisma.workspace.findMany({
      where: { userId: user.id },
      select: { id: true, name: true, catalysisSystem: true }
    })
  }, null, 2));
};

main()
  .catch((error) => {
    console.error(error instanceof Error ? error.message : error);
    process.exitCode = 1;
  })
  .finally(async () => prisma.$disconnect());

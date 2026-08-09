import { Router } from 'express';
import prisma from '../config/db';
import { requireAuth, requireWorkspaceAccess } from '../middleware/auth';

const router = Router();
router.use(requireAuth);

router.get('/', async (req, res) => {
  const workspaces = await prisma.workspace.findMany({
    where: { userId: req.authUser!.id },
    orderBy: { createdAt: 'asc' }
  });
  res.json({ workspaces });
});

router.post('/', async (req, res) => {
  const name = String(req.body?.name || '').trim();
  const catalysisSystem = String(req.body?.catalysisSystem || '').trim();
  if (!name || !['photocatalysis', 'thermal_catalysis'].includes(catalysisSystem)) {
    return res.status(400).json({ error: '请填写名称并选择有效催化体系' });
  }
  const workspace = await prisma.workspace.create({
    data: {
      name,
      catalysisSystem,
      description: String(req.body?.description || '').trim(),
      userId: req.authUser!.id
    }
  });
  res.status(201).json({ workspace });
});

router.get('/:id', requireWorkspaceAccess, async (req, res) => {
  const workspace = await prisma.workspace.findUniqueOrThrow({ where: { id: String(req.params.id) } });
  res.json({ workspace });
});

export default router;

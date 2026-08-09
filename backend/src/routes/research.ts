import { Router } from 'express';
import { requireAuth, requireWorkspaceAccess } from '../middleware/auth';
import { researchAssistantService } from '../services/researchAssistantService';
import { researchGraphService } from '../services/researchGraphService';

const router = Router();
router.use(requireAuth);
router.use('/workspaces/:workspaceId', requireWorkspaceAccess);

const message = (error: unknown) => error instanceof Error ? error.message : String(error);

router.get('/workspaces/:workspaceId/stats', async (req, res) => {
  res.json(await researchGraphService.getStats(String(req.params.workspaceId)));
});

router.get('/workspaces/:workspaceId/graph', async (req, res) => {
  const nodeTypes = String(req.query.nodeTypes || '').split(',').map((item) => item.trim()).filter(Boolean);
  res.json(await researchGraphService.getGraph({
    workspaceId: String(req.params.workspaceId),
    search: typeof req.query.search === 'string' ? req.query.search : undefined,
    nodeTypes: nodeTypes.length ? nodeTypes : undefined,
    limit: Number(req.query.limit || 320)
  }));
});

router.get('/workspaces/:workspaceId/experiments', async (req, res) => {
  res.json({
    experiments: await researchGraphService.listExperiments(
      String(req.params.workspaceId),
      Number(req.query.limit || 50)
    )
  });
});

router.post('/workspaces/:workspaceId/experiments', async (req, res) => {
  try {
    const experiment = await researchGraphService.saveExperiment(String(req.params.workspaceId), req.body || {});
    res.status(req.body?.id ? 200 : 201).json({ experiment });
  } catch (error) {
    res.status(400).json({ error: message(error) });
  }
});

router.post('/workspaces/:workspaceId/advice', async (req, res) => {
  try {
    res.json(await researchAssistantService.advise({
      workspaceId: String(req.params.workspaceId),
      userId: req.authUser!.id,
      goal: String(req.body?.goal || ''),
      question: typeof req.body?.question === 'string' ? req.body.question : undefined,
      experimentId: typeof req.body?.experimentId === 'string' ? req.body.experimentId : null,
      constraints: req.body?.constraints && typeof req.body.constraints === 'object' ? req.body.constraints : {},
      preferredDirectionCount: Number(req.body?.preferredDirectionCount || 1),
      focus: ['performance', 'engineering', 'gap'].includes(req.body?.focus) ? req.body.focus : undefined
    }));
  } catch (error) {
    res.status(400).json({ error: message(error) });
  }
});

router.get('/workspaces/:workspaceId/advice/:runId', async (req, res) => {
  const run = await researchGraphService.getAdviceRun(
    String(req.params.workspaceId),
    String(req.params.runId)
  );
  if (!run) return res.status(404).json({ error: '建议记录不存在' });
  res.json({ run });
});

router.post('/workspaces/:workspaceId/advice/:runId/experiment-plan', async (req, res) => {
  try {
    res.json(await researchAssistantService.planExperiment({
      workspaceId: String(req.params.workspaceId),
      userId: req.authUser!.id,
      runId: String(req.params.runId),
      directionIndex: Math.max(0, Number(req.body?.directionIndex || 0))
    }));
  } catch (error) {
    res.status(400).json({ error: message(error) });
  }
});

export default router;

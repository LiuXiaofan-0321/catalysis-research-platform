import { Router } from 'express';
import prisma from '../config/db';
import { requireAuth } from '../middleware/auth';

const router = Router();
router.use(requireAuth);

const parse = <T>(value: string, fallback: T): T => {
  try { return JSON.parse(value) as T; } catch { return fallback; }
};

const serialize = (profile: any) => ({
  id: profile.id,
  institution: profile.institution || '',
  role: profile.role || '',
  researchInterests: parse(profile.researchInterestsJson, []),
  catalystSystems: parse(profile.catalystSystemsJson, []),
  techniques: parse(profile.techniquesJson, []),
  currentGoals: parse(profile.currentGoalsJson, []),
  experimentalConstraints: parse(profile.experimentalConstraintsJson, {}),
  preferredOutputStyle: profile.preferredOutputStyle,
  notes: profile.notes,
  updatedAt: profile.updatedAt
});

router.get('/', async (req, res) => {
  const profile = await prisma.researcherProfile.upsert({
    where: { userId: req.authUser!.id },
    update: {},
    create: { userId: req.authUser!.id }
  });
  res.json({ profile: serialize(profile) });
});

router.put('/', async (req, res) => {
  const array = (value: unknown) =>
    Array.isArray(value) ? value.map(String).map((item) => item.trim()).filter(Boolean).slice(0, 50) : [];
  const profile = await prisma.researcherProfile.upsert({
    where: { userId: req.authUser!.id },
    create: {
      userId: req.authUser!.id,
      institution: String(req.body?.institution || '').trim(),
      role: String(req.body?.role || '').trim(),
      researchInterestsJson: JSON.stringify(array(req.body?.researchInterests)),
      catalystSystemsJson: JSON.stringify(array(req.body?.catalystSystems)),
      techniquesJson: JSON.stringify(array(req.body?.techniques)),
      currentGoalsJson: JSON.stringify(array(req.body?.currentGoals)),
      experimentalConstraintsJson: JSON.stringify(req.body?.experimentalConstraints || {}),
      preferredOutputStyle: String(req.body?.preferredOutputStyle || 'evidence_first'),
      notes: String(req.body?.notes || '').trim()
    },
    update: {
      institution: String(req.body?.institution || '').trim(),
      role: String(req.body?.role || '').trim(),
      researchInterestsJson: JSON.stringify(array(req.body?.researchInterests)),
      catalystSystemsJson: JSON.stringify(array(req.body?.catalystSystems)),
      techniquesJson: JSON.stringify(array(req.body?.techniques)),
      currentGoalsJson: JSON.stringify(array(req.body?.currentGoals)),
      experimentalConstraintsJson: JSON.stringify(req.body?.experimentalConstraints || {}),
      preferredOutputStyle: String(req.body?.preferredOutputStyle || 'evidence_first'),
      notes: String(req.body?.notes || '').trim()
    }
  });
  res.json({ profile: serialize(profile) });
});

export default router;

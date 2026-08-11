import { Router } from 'express';
import prisma from '../config/db';
import { requireAuth } from '../middleware/auth';
import {
  getOrCreateResearcherProfile,
  mergeConversationLearning,
  profileCreateData,
  profileUpdateData,
  serializeResearcherProfile
} from '../services/researcherProfileService';

const router = Router();
router.use(requireAuth);

router.get('/', async (req, res) => {
  const profile = await getOrCreateResearcherProfile(req.authUser!.id);
  res.json({ profile: serializeResearcherProfile(profile) });
});

const interviewQuestions = [
  {
    id: 'research_interests',
    title: '具体研究对象',
    prompt: '你当前最想解决的反应、材料或科学问题是什么？',
    hint: '例如：甲烷温和氧化、塑料升级回收、抗生素降解、分子筛限域效应。',
    type: 'text'
  },
  {
    id: 'current_goals',
    title: '近期阶段目标',
    prompt: '未来 3–6 个月，你最希望完成什么科研结果？',
    hint: '可以是论文结果、关键机理验证、性能指标或工程可行性证明。',
    type: 'text'
  },
  {
    id: 'research_priorities',
    title: '决策优先级',
    prompt: '当多个方向都可行时，你希望 AI 优先考虑哪些因素？',
    type: 'multiple',
    options: [
      { value: 'performance', label: '性能提升' },
      { value: 'mechanism', label: '机理清晰' },
      { value: 'engineering', label: '工程可行' },
      { value: 'novelty', label: '研究新颖性' },
      { value: 'cost', label: '成本控制' },
      { value: 'sustainability', label: '绿色与安全' }
    ]
  },
  {
    id: 'techniques',
    title: '已掌握技术',
    prompt: '哪些实验或表征技术是你能够独立完成的？',
    hint: '例如：XRD、BET、GC-MS、原位红外、EPR、光电化学测试。',
    type: 'text'
  },
  {
    id: 'available_resources',
    title: '可调用资源',
    prompt: '除了个人技能，你还能调用哪些设备、材料或合作资源？',
    hint: '可以填写课题组设备、公共平台、合作团队或稳定可获得的特殊材料。',
    type: 'text'
  },
  {
    id: 'experimental_constraints',
    title: '硬性边界',
    prompt: '实验在温度、压力、预算、周期、安全或样品量上有哪些硬限制？',
    hint: '这些条件会作为 AI 方案排序时的硬约束。',
    type: 'text'
  },
  {
    id: 'risk_tolerance',
    title: '探索风险偏好',
    prompt: '你希望 AI 推荐多大风险的新方向？',
    type: 'single',
    options: [
      { value: 'conservative', label: '稳健优先', description: '优先证据充分、短周期可验证的方向' },
      { value: 'balanced', label: '平衡探索', description: '兼顾可行性与适度的新颖性' },
      { value: 'exploratory', label: '高风险探索', description: '接受更大不确定性以寻找潜在突破' }
    ]
  },
  {
    id: 'avoidances',
    title: '不希望出现的建议',
    prompt: '除了前面提到的异质结偏好，还有哪些路线或表达方式应避免？',
    hint: '例如：不使用贵金属、不做高压、不接受缺少对照的复杂体系。',
    type: 'text'
  },
  {
    id: 'success_definition',
    title: '成功标准',
    prompt: '什么样的 AI 建议会让你觉得真正有用？',
    hint: '可以描述希望看到的证据深度、实验颗粒度、创新边界或输出格式。',
    type: 'text'
  }
] as const;

const answerFor = (profile: any, id: string) => {
  if (id === 'research_interests') return profile.researchInterests;
  if (id === 'current_goals') return profile.currentGoals;
  if (id === 'research_priorities') return profile.researchPriorities;
  if (id === 'techniques') return profile.techniques;
  if (id === 'available_resources') return profile.availableResources;
  if (id === 'experimental_constraints') return profile.experimentalConstraints?.other || '';
  if (id === 'risk_tolerance') return profile.riskTolerance;
  if (id === 'avoidances') return profile.avoidances;
  if (id === 'success_definition') return profile.openResearchContext;
  return '';
};

router.get('/questions', async (req, res) => {
  const row = await getOrCreateResearcherProfile(req.authUser!.id);
  const profile = serializeResearcherProfile(row);
  const answeredCount = interviewQuestions.filter((question) => profile.interviewAnswers[question.id]).length;
  res.json({
    questions: interviewQuestions.map((question) => ({
      ...question,
      answer: answerFor(profile, question.id),
      answered: Boolean(profile.interviewAnswers[question.id])
    })),
    progress: {
      answered: answeredCount,
      total: interviewQuestions.length,
      completed: Boolean(profile.onboardingCompletedAt)
    }
  });
});

router.put('/questions/:questionId', async (req, res) => {
  const questionId = String(req.params.questionId);
  const question = interviewQuestions.find((item) => item.id === questionId);
  if (!question) return res.status(404).json({ error: '画像问题不存在' });
  const row = await getOrCreateResearcherProfile(req.authUser!.id);
  const profile = serializeResearcherProfile(row);
  const list = (value: unknown) =>
    Array.isArray(value)
      ? value.map(String).map((item) => item.trim()).filter(Boolean).slice(0, 30)
      : String(value || '').split(/[,，;\n]/).map((item) => item.trim()).filter(Boolean).slice(0, 30);
  const text = String(req.body?.answer || '').trim().slice(0, 4000);
  const answer = question.type === 'multiple' ? list(req.body?.answer) : text;
  const data: Record<string, unknown> = {
    interviewAnswersJson: JSON.stringify({
      ...profile.interviewAnswers,
      [questionId]: { answer, answeredAt: new Date().toISOString() }
    })
  };
  if (questionId === 'research_interests') data.researchInterestsJson = JSON.stringify(list(answer));
  if (questionId === 'current_goals') data.currentGoalsJson = JSON.stringify(list(answer));
  if (questionId === 'research_priorities') data.researchPrioritiesJson = JSON.stringify(list(answer));
  if (questionId === 'techniques') data.techniquesJson = JSON.stringify(list(answer));
  if (questionId === 'available_resources') data.availableResourcesJson = JSON.stringify(list(answer));
  if (questionId === 'experimental_constraints') {
    data.experimentalConstraintsJson = JSON.stringify({ ...profile.experimentalConstraints, other: text });
  }
  if (questionId === 'risk_tolerance') {
    data.riskTolerance = ['conservative', 'balanced', 'exploratory'].includes(text) ? text : 'balanced';
  }
  if (questionId === 'avoidances') data.avoidancesJson = JSON.stringify(list(answer));
  if (questionId === 'success_definition') data.openResearchContext = text;
  const updated = await prisma.researcherProfile.update({
    where: { userId: req.authUser!.id },
    data
  });
  res.json({ profile: serializeResearcherProfile(updated) });
});

router.post('/questions/complete', async (req, res) => {
  const updated = await prisma.researcherProfile.update({
    where: { userId: req.authUser!.id },
    data: { onboardingCompletedAt: new Date() }
  });
  res.json({ profile: serializeResearcherProfile(updated) });
});

router.post('/learn', async (req, res) => {
  const value = String(req.body?.value || '').trim();
  const category = String(req.body?.category || '').trim();
  if (!value) return res.status(400).json({ error: '请填写回答内容' });
  const learning = await mergeConversationLearning(
    req.authUser!.id,
    [{ category, value, confidence: 1 }],
    String(req.body?.evidence || value)
  );
  res.json({ learning });
});

router.put('/', async (req, res) => {
  const profile = await prisma.researcherProfile.upsert({
    where: { userId: req.authUser!.id },
    create: profileCreateData(req.authUser!.id, req.body, true),
    update: profileUpdateData(req.body, true)
  });
  res.json({ profile: serializeResearcherProfile(profile) });
});

export default router;

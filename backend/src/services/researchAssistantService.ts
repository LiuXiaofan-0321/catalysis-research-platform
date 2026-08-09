import prisma from '../config/db';
import { deepseekClient } from './deepseekClient';
import { ResearchAdvicePayload, researchGraphService } from './researchGraphService';

type AdviceInput = {
  workspaceId: string;
  userId: string;
  goal: string;
  question?: string;
  experimentId?: string | null;
  constraints?: Record<string, unknown>;
  preferredDirectionCount?: number;
  focus?: 'performance' | 'engineering' | 'gap';
};

const clip = (value: unknown, max = 1200) => {
  const normalized = String(value ?? '').replace(/\s+/g, ' ').trim();
  return normalized.length > max ? `${normalized.slice(0, max)}…` : normalized;
};

const strings = (value: unknown, max = 12) =>
  Array.isArray(value)
    ? Array.from(new Set(value.map((item) => clip(item, 500)).filter(Boolean))).slice(0, max)
    : [];

const parse = <T>(value: string | null | undefined, fallback: T): T => {
  try { return value ? JSON.parse(value) as T : fallback; } catch { return fallback; }
};

const profileContext = async (userId: string) => {
  const row = await prisma.researcherProfile.findUnique({ where: { userId } });
  if (!row) return null;
  return {
    institution: row.institution,
    role: row.role,
    researchInterests: parse(row.researchInterestsJson, []),
    catalystSystems: parse(row.catalystSystemsJson, []),
    techniques: parse(row.techniquesJson, []),
    currentGoals: parse(row.currentGoalsJson, []),
    experimentalConstraints: parse(row.experimentalConstraintsJson, {}),
    preferredOutputStyle: row.preferredOutputStyle,
    notes: row.notes
  };
};

const compactEvidence = (node: any, alias: string) => ({
  id: alias,
  sourceNodeId: node.id,
  type: node.type,
  label: node.label,
  sourceDocumentId: node.sourceDocumentId,
  confidence: node.confidence,
  reviewStatus: node.reviewStatus,
  data: {
    statement: clip(node.data?.statement, 560) || undefined,
    objective: clip(node.data?.objective, 480) || undefined,
    metricName: clip(node.data?.metric_name, 220) || undefined,
    numericValue: node.data?.numeric_value ?? undefined,
    textValue: clip(node.data?.text_value, 320) || undefined,
    unit: clip(node.data?.unit, 80) || undefined,
    rawValue: clip(node.data?.raw_value, 240) || undefined,
    conditions: Array.isArray(node.data?.conditions) ? node.data.conditions.slice(0, 8) : undefined,
    entityType: clip(node.data?.type, 120) || undefined,
    canonicalName: clip(node.data?.canonical_name, 260) || undefined,
    zhName: clip(node.data?.zh_name, 260) || undefined
  },
  evidence: (Array.isArray(node.evidence) ? node.evidence : []).slice(0, 2).map((item: any) => ({
    page: item.pdf_page_index ?? item.page ?? null,
    section: clip(item.section, 160) || null,
    quote: clip(item.quote, 420) || null,
    validation: item.evidence_validation || null
  }))
});

const emptyExperiment = () => ({
  objective: '',
  materials: [] as string[],
  procedure: [] as string[],
  variables: [] as string[],
  controls: [] as string[],
  measurements: [] as string[],
  decisionRules: [] as string[],
  stoppingCriteria: [] as string[]
});

const normalizeAdvice = (
  raw: any,
  aliasToNode: Map<string, string>,
  directionCount: number
): ResearchAdvicePayload => ({
  answer: clip(raw?.answer, 4000) || '当前证据不足以形成可靠建议。',
  candidateDirections: (Array.isArray(raw?.candidateDirections) ? raw.candidateDirections : [])
    .slice(0, directionCount)
    .map((item: any) => {
      const plan = item?.nextExperiment || {};
      const evidence = (Array.isArray(item?.supportingEvidence) ? item.supportingEvidence : [])
        .map((entry: any) => {
          const alias = clip(entry?.nodeId, 20).toUpperCase().match(/E\d{2}/)?.[0] || '';
          const nodeId = aliasToNode.get(alias);
          return nodeId ? {
            nodeId,
            paperId: clip(entry?.paperId, 180) || null,
            quote: clip(entry?.quote, 560) || null,
            role: clip(entry?.role, 240) || 'supports'
          } : null;
        })
        .filter(Boolean)
        .slice(0, 10) as ResearchAdvicePayload['candidateDirections'][number]['supportingEvidence'];
      return {
        title: clip(item?.title, 260),
        hypothesis: clip(item?.hypothesis, 1200),
        rationale: clip(item?.rationale, 2000),
        novelty: clip(item?.novelty, 1000),
        systemDesign: {
          molecularSieveRole: clip(item?.systemDesign?.molecularSieveRole, 800),
          activePhaseRole: clip(item?.systemDesign?.activePhaseRole, 800),
          interfaceStrategy: clip(item?.systemDesign?.interfaceStrategy, 800),
          proposedPathway: clip(item?.systemDesign?.proposedPathway, 1200),
          selectivityTarget: clip(item?.systemDesign?.selectivityTarget, 700),
          evidenceBoundary: clip(item?.systemDesign?.evidenceBoundary, 1000)
        },
        supportingEvidence: evidence,
        feasibility: item?.feasibility === 'high' || item?.feasibility === 'low' ? item.feasibility : 'medium',
        confidence: evidence.length ? Math.max(0, Math.min(1, Number(item?.confidence) || 0.55)) : 0.3,
        risks: strings(item?.risks, 12),
        nextExperiment: {
          ...emptyExperiment(),
          objective: clip(plan.objective, 1000),
          materials: strings(plan.materials, 16),
          procedure: strings(plan.procedure, 18),
          variables: strings(plan.variables, 14),
          controls: strings(plan.controls, 14),
          measurements: strings(plan.measurements, 16),
          decisionRules: strings(plan.decisionRules, 12),
          stoppingCriteria: strings(plan.stoppingCriteria, 12)
        }
      };
    })
    .filter((item: any) => item.title && item.hypothesis),
  contradictions: strings(raw?.contradictions, 14),
  dataGaps: strings(raw?.dataGaps, 14),
  safetyNotes: strings(raw?.safetyNotes, 14)
});

const responseSchema = {
  answer: '完整说明证据范围、推理逻辑与建议边界',
  candidateDirections: [{
    title: '候选方向名称',
    hypothesis: '可证伪的研究假设',
    rationale: '由证据到假设的推理链',
    novelty: '相对现有研究的明确增量',
    systemDesign: {
      molecularSieveRole: '孔道、酸性、限域、吸附、形选、载体或稳定作用',
      activePhaseRole: '热催化或光催化活性相承担的功能',
      interfaceStrategy: '两类组分的界面与空间构型',
      proposedPathway: '底物到目标产物的拟议路径及竞争路径',
      selectivityTarget: '目标产物或降解目标与应避免的副反应',
      evidenceBoundary: '论文直接证据、跨论文归纳、待验证假设的边界'
    },
    supportingEvidence: [{
      nodeId: '只能使用 E01、E02 等输入中的短编号',
      paperId: '来源文档ID或null',
      quote: '输入中已有的原文证据或null',
      role: '该证据在推理中的作用'
    }],
    feasibility: 'high|medium|low',
    confidence: 0.7,
    risks: ['材料、机理、工程、安全等风险'],
    nextExperiment: {
      objective: '最小判别实验目标',
      materials: ['材料与试剂'],
      procedure: ['步骤'],
      variables: ['变量'],
      controls: ['对照组'],
      measurements: ['表征和检测'],
      decisionRules: ['结果如何支持、修正或否定假设'],
      stoppingCriteria: ['停止或转向条件']
    }
  }],
  contradictions: ['证据冲突'],
  dataGaps: ['仍缺少的数据'],
  safetyNotes: ['安全注意事项']
};

export class ResearchAssistantService {
  async advise(input: AdviceInput) {
    const goal = clip(input.goal, 1800);
    if (!goal) throw new Error('研究目标不能为空');
    if (!deepseekClient.isConfigured()) throw new Error('DEEPSEEK_API_KEY 未配置');
    const workspace = await prisma.workspace.findFirstOrThrow({
      where: { id: input.workspaceId, userId: input.userId }
    });
    const profile = await profileContext(input.userId);
    const systemTerms = workspace.catalysisSystem === 'thermal_catalysis'
      ? 'thermal catalysis zeolite molecular sieve acid site metal site reaction pathway selectivity coke stability'
      : 'photocatalysis visible light charge separation active species heterojunction zeolite adsorption confinement stability';
    const evidenceContext = await researchGraphService.buildEvidenceContext({
      workspaceId: input.workspaceId,
      experimentId: input.experimentId,
      query: `${goal} ${input.question || ''} ${systemTerms} ${JSON.stringify(input.constraints || {})}`,
      limit: 30
    });
    const evidenceNodes = evidenceContext.nodes.slice(0, 18).map((node, index) =>
      compactEvidence(node, `E${String(index + 1).padStart(2, '0')}`)
    );
    const aliasToNode = new Map(evidenceNodes.map((node) => [node.id, node.sourceNodeId]));
    const directionCount = Math.max(1, Math.min(3, Number(input.preferredDirectionCount || 1)));
    const context = {
      workspace: {
        id: workspace.id,
        name: workspace.name,
        catalysisSystem: workspace.catalysisSystem
      },
      mode: evidenceContext.currentExperiment ? 'experiment_feedback' : 'initial_direction',
      goal,
      question: clip(input.question, 1400) || null,
      focus: input.focus || 'performance',
      constraints: input.constraints || {},
      researcherProfile: profile,
      currentExperiment: evidenceContext.currentExperiment,
      previousAdviceRuns: evidenceContext.previousAdviceRuns,
      papers: evidenceContext.documents,
      evidenceNodes,
      requestedDirectionCount: directionCount
    };
    const runId = await researchGraphService.createAdviceRun(
      input.workspaceId,
      input.experimentId || null,
      { goal, question: input.question || null, constraints: input.constraints || {}, focus: input.focus || null },
      context
    );

    const systemMode = workspace.catalysisSystem === 'thermal_catalysis'
      ? [
          '当前语料库是分子筛热催化证据图谱。',
          '候选方向应以热催化机理、酸碱位、金属位、限域、扩散、形选、积碳和稳定性为主。',
          '除非用户明确要求，不要擅自改成光催化体系。'
        ]
      : [
          '当前语料库是光催化证据图谱。',
          '当课题涉及分子筛时，应明确分子筛与光催化活性相的分工、界面和协同机制。',
          '不得把单纯吸附或单纯热催化伪装成光催化结论。'
        ];
    try {
      const result = await deepseekClient.json<any>({
        system: [
          '你是催化科研多智能体平台的 Orchestrator，负责整合检索、机理、实验规划和证据审查结果。',
          ...systemMode,
          '只能引用 input.evidenceNodes 中真实存在的 E 编号，不得编造论文、DOI、引文或实验结果。',
          '必须区分论文直接证据、跨论文归纳、AI 候选假设和用户实验记录。',
          '相关性不等于因果性；低质量、needs_review、综述证据应降低权重。',
          '输出候选方向必须可证伪，并给出最小判别实验、对照、测量指标和停止条件。',
          '研究者画像只用于调整可行性、设备条件和表达方式，不得覆盖论文事实。',
          '如果已有实验结果与旧建议冲突，应明确保留、修正或停止旧假设。',
          '涉及高温、高压、易燃气体、强氧化剂、毒性或环境风险时给出安全提示。',
          '使用简体中文，只返回符合 schema 的 JSON。'
        ].join('\n'),
        schema: responseSchema,
        input: context
      });
      const advice = normalizeAdvice(result.data, aliasToNode, directionCount);
      await researchGraphService.completeAdviceRun(runId, advice, result);
      return {
        runId,
        status: 'completed',
        provider: result.provider,
        model: result.model,
        evidenceNodeCount: evidenceNodes.length,
        paperCount: evidenceContext.documents.length,
        advice
      };
    } catch (error) {
      await researchGraphService.failAdviceRun(runId, error);
      throw error;
    }
  }

  async planExperiment(input: { workspaceId: string; userId: string; runId: string; directionIndex: number }) {
    const workspace = await prisma.workspace.findFirstOrThrow({
      where: { id: input.workspaceId, userId: input.userId }
    });
    const run = await researchGraphService.getAdviceRun(input.workspaceId, input.runId);
    if (!run || run.status !== 'completed') throw new Error('建议记录不存在或尚未完成');
    const advice = run.response as ResearchAdvicePayload;
    const direction = advice.candidateDirections[input.directionIndex];
    if (!direction) throw new Error('候选方向不存在');
    const result = await deepseekClient.json<any>({
      system: [
        '你是催化实验 Planning Agent。',
        '在不改变候选假设和证据边界的前提下，把首轮实验展开成可执行、可判别、可回流的方案。',
        '不得补造具体性能数据或论文结论。',
        '必须包含变量、对照、表征、判定规则、停止条件和安全边界。',
        '使用简体中文，只返回 JSON。'
      ].join('\n'),
      schema: responseSchema.candidateDirections[0].nextExperiment,
      input: {
        catalysisSystem: workspace.catalysisSystem,
        direction,
        researcherProfile: await profileContext(input.userId)
      },
      maxTokens: 20000
    });
    const plan = result.data || {};
    direction.nextExperiment = {
      objective: clip(plan.objective, 1000),
      materials: strings(plan.materials, 20),
      procedure: strings(plan.procedure, 24),
      variables: strings(plan.variables, 18),
      controls: strings(plan.controls, 18),
      measurements: strings(plan.measurements, 20),
      decisionRules: strings(plan.decisionRules, 16),
      stoppingCriteria: strings(plan.stoppingCriteria, 16)
    };
    await researchGraphService.updateAdviceResponse(input.runId, advice);
    return {
      runId: input.runId,
      directionIndex: input.directionIndex,
      provider: result.provider,
      model: result.model,
      direction,
      safetyNotes: advice.safetyNotes,
      dataGaps: advice.dataGaps
    };
  }
}

export const researchAssistantService = new ResearchAssistantService();

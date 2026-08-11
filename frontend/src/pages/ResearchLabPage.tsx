import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import {
  ArrowLeft,
  Beaker,
  BookOpen,
  ChevronRight,
  ClipboardCheck,
  FlaskConical,
  Lightbulb,
  Loader2,
  Network,
  RefreshCw,
  Save,
  Search,
  ShieldAlert,
  Sparkles,
  UserRoundCog,
  Workflow
} from 'lucide-react';
import { api, ProfileFollowUpQuestion, Workspace } from '../api';
import { researchApi, ResearchAdvice, ResearchExperimentLog, ResearchGraphNode } from '../services/researchApi';

const focusOptions = [
  { id: 'performance', label: '性能与机理' },
  { id: 'engineering', label: '工程可用性' },
  { id: 'gap', label: '证据空白' }
] as const;

const supplementalQuestionPrompts = [
  '我现有的设备和表征能力是：',
  '我明确不希望采用的材料或路线是：',
  '请重点回答这个具体问题：',
  '我希望最终方案优先满足的指标是：'
];

const topicTemplates = {
  photocatalysis: [
    {
      id: 'methane',
      label: '甲烷转化',
      goal: '设计分子筛-光催化耦合体系用于甲烷温和转化，利用分子筛的限域、吸附或形选作用与光催化活性位协同，优先探索甲醇等含氧产物，并控制过度氧化和碳平衡。'
    },
    {
      id: 'plastic',
      label: '塑料回收转化',
      goal: '设计分子筛-光催化耦合体系用于塑料回收、降解与高值转化，利用分子筛孔道和酸性位调控中间体传质与产物分布，结合光生载流子驱动断链或选择性氧化，并区分矿化与高值产物路线。'
    },
    {
      id: 'antibiotic',
      label: '抗生素降解',
      goal: '设计分子筛-光催化耦合体系用于水中抗生素降解，利用分子筛吸附富集和孔道微环境提高污染物与活性物种的接触效率，结合可见光催化实现母体去除、矿化和毒性降低，同时控制催化剂浸出与循环稳定性。'
    }
  ],
  thermal_catalysis: [
    {
      id: 'methane',
      label: '甲烷转化',
      goal: '基于分子筛孔道、酸性与金属位协同，设计甲烷选择性热催化转化方向，重点控制深度氧化、副反应和高温稳定性。'
    },
    {
      id: 'plastic',
      label: '塑料升级回收',
      goal: '面向废塑料热催化升级回收，设计分子筛孔结构、酸性和扩散协同的产物选择性调控方案，并控制积碳和失活。'
    },
    {
      id: 'stability',
      label: '稳定性窗口',
      goal: '从分子筛热催化证据图谱中寻找兼顾低温活化、选择性、抗积碳和水热稳定性的可验证研究窗口。'
    }
  ]
} as const;

const nodeTypeLabel: Record<string, string> = {
  paper: '论文',
  keyword: '关键词',
  entity: '实体',
  experiment: '实验',
  observation: '观测',
  claim: 'Claim'
};

const confidenceLabel = (value: number) => `${Math.round(Math.max(0, Math.min(1, value || 0)) * 100)}%`;

export default function ResearchLabPage() {
  const { id: workspaceId = '' } = useParams();
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [stats, setStats] = useState<any>(null);
  const [nodes, setNodes] = useState<ResearchGraphNode[]>([]);
  const [experiments, setExperiments] = useState<ResearchExperimentLog[]>([]);
  const [search, setSearch] = useState('');
  const [goal, setGoal] = useState('');
  const [question, setQuestion] = useState('');
  const [focus, setFocus] = useState<(typeof focusOptions)[number]['id']>('engineering');
  const [advice, setAdvice] = useState<ResearchAdvice | null>(null);
  const [runId, setRunId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [advising, setAdvising] = useState(false);
  const [planningIndex, setPlanningIndex] = useState<number | null>(null);
  const [savingExperiment, setSavingExperiment] = useState(false);
  const [activeExperimentId, setActiveExperimentId] = useState('');
  const [experimentStatus, setExperimentStatus] = useState<ResearchExperimentLog['status']>('planned');
  const [observationDraft, setObservationDraft] = useState('');
  const [outcomeDraft, setOutcomeDraft] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [profileFollowUps, setProfileFollowUps] = useState<ProfileFollowUpQuestion[]>([]);
  const [followUpAnswers, setFollowUpAnswers] = useState<Record<number, string>>({});
  const [savedFollowUps, setSavedFollowUps] = useState<number[]>([]);

  const load = async (query = search) => {
    if (!workspaceId) return;
    setLoading(true);
    setError(null);
    try {
      const [workspaceResult, statsResult, graphResult, experimentResult] = await Promise.all([
        researchApi.getWorkspace(workspaceId),
        researchApi.getStats(workspaceId),
        researchApi.getGraph(workspaceId, { search: query.trim() || undefined, limit: query.trim() ? 160 : 320 }),
        researchApi.listExperiments(workspaceId)
      ]);
      setWorkspace(workspaceResult);
      setStats(statsResult);
      setNodes(graphResult.nodes);
      setExperiments(experimentResult);
      setGoal((current) => current || topicTemplates[workspaceResult.catalysisSystem][0].goal);
    } catch (loadError: any) {
      setError(loadError?.response?.data?.error || loadError?.message || '科研图谱加载失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load('');
  }, [workspaceId]);

  const nodeGroups = useMemo(() => {
    const result: Record<string, ResearchGraphNode[]> = {};
    nodes.forEach((node) => {
      (result[node.type] ||= []).push(node);
    });
    return result;
  }, [nodes]);

  const activeExperiment = useMemo(
    () => experiments.find((experiment) => experiment.id === activeExperimentId) || null,
    [experiments, activeExperimentId]
  );

  useEffect(() => {
    setExperimentStatus(activeExperiment?.status || 'planned');
    setObservationDraft('');
    setOutcomeDraft('');
  }, [activeExperimentId]);

  const requestAdvice = async (experimentId = activeExperimentId) => {
    if (!workspaceId || !goal.trim()) return;
    setAdvising(true);
    setError(null);
    try {
      const result = await researchApi.requestAdvice(workspaceId, {
        goal: goal.trim(),
        question: [
          experimentId
            ? '请结合当前实验的最新观察和结果，判断已有假设应保留、修正还是停止，并给出信息增益最高的下一步。'
            : '',
          question.trim()
        ].filter(Boolean).join('\n') || undefined,
        experimentId: experimentId || null,
        focus,
        preferredDirectionCount: 1,
        constraints: {
          outputMode: 'evidence_grounded_hypothesis',
          researchMode: workspace?.catalysisSystem === 'thermal_catalysis'
            ? 'zeolite_thermal_catalysis'
            : 'zeolite_photocatalysis_coupling',
          mandatoryComponents: workspace?.catalysisSystem === 'thermal_catalysis'
            ? ['molecular_sieve', 'thermal_active_phase']
            : ['molecular_sieve', 'photocatalyst'],
          requireExperimentFeedbackLoop: true
        }
      });
      setAdvice(result.advice);
      setRunId(result.runId);
      setProfileFollowUps(result.profileFollowUpQuestions || []);
      setFollowUpAnswers({});
      setSavedFollowUps([]);
    } catch (adviceError: any) {
      setError(adviceError?.response?.data?.error || adviceError?.message || 'AI 方向生成失败');
    } finally {
      setAdvising(false);
    }
  };

  const saveProfileFollowUp = async (item: ProfileFollowUpQuestion, index: number) => {
    const answer = followUpAnswers[index]?.trim();
    if (!answer) return;
    setError(null);
    try {
      await api.learnProfile(item.category, answer, `${item.question}\n${answer}`);
      setSavedFollowUps((current) => [...current, index]);
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : '画像回答保存失败');
    }
  };

  const thermal = workspace?.catalysisSystem === 'thermal_catalysis';
  const activeTopicTemplates = thermal ? topicTemplates.thermal_catalysis : topicTemplates.photocatalysis;
  const platformLabel = thermal ? 'Thermal Catalysis Research Lab' : 'Photocatalysis Research Lab';
  const designTitle = thermal ? '分子筛热催化课题设计' : '分子筛-光催化课题设计';
  const activePhaseLabel = thermal ? '热催化活性相作用' : '光催化作用';
  const focusDescriptions = thermal
    ? {
        performance: '活性、选择性、酸性/金属位、路径与失活机理',
        engineering: '温压窗口、传质、积碳、再生与水热稳定性',
        gap: '冲突证据、缺失对照与尚未验证的位点协同'
      }
    : {
        performance: '光响应、载流子、活性物种和反应路径',
        engineering: '稳定、回收、循环、浸出和真实反应介质',
        gap: '冲突证据、缺失对照和未验证的界面组合'
      };

  const saveDirectionAsExperiment = async (direction: ResearchAdvice['candidateDirections'][number], directionIndex: number) => {
    if (!workspaceId || !runId) return;
    setSavingExperiment(true);
    setError(null);
    try {
      const experiment = await researchApi.saveExperiment(workspaceId, {
        title: direction.title,
        objective: direction.nextExperiment.objective || direction.hypothesis,
        status: 'planned',
        materials: direction.nextExperiment.materials || [],
        procedure: [
          ...(direction.nextExperiment.procedure || []).map((item, stepIndex) => ({ step: stepIndex + 1, text: item })),
          { section: 'variables', items: direction.nextExperiment.variables },
          { section: 'controls', items: direction.nextExperiment.controls },
          { section: 'measurements', items: direction.nextExperiment.measurements },
          { section: 'decisionRules', items: direction.nextExperiment.decisionRules || [] },
          { section: 'stoppingCriteria', items: direction.nextExperiment.stoppingCriteria }
        ],
        conditions: { couplingDesign: direction.couplingDesign },
        observations: [],
        outcome: {},
        constraints: {
          sourceAdviceRunId: runId,
          directionIndex,
          hypothesis: direction.hypothesis,
          supportingEvidence: direction.supportingEvidence
        },
        source: 'research_advice'
      });
      setExperiments((current) => [experiment, ...current.filter((item) => item.id !== experiment.id)]);
      setActiveExperimentId(experiment.id);
    } catch (saveError: any) {
      setError(saveError?.response?.data?.error || saveError?.message || '实验记录保存失败');
    } finally {
      setSavingExperiment(false);
    }
  };

  const saveExperimentProgress = async (continueWithAdvice = false) => {
    if (!workspaceId || !activeExperiment) return;
    setSavingExperiment(true);
    setError(null);
    try {
      const recordedAt = new Date().toISOString();
      const experiment = await researchApi.saveExperiment(workspaceId, {
        ...activeExperiment,
        status: experimentStatus,
        observations: observationDraft.trim()
          ? [...activeExperiment.observations, { recordedAt, text: observationDraft.trim() }]
          : activeExperiment.observations,
        outcome: outcomeDraft.trim()
          ? { ...activeExperiment.outcome, latestSummary: outcomeDraft.trim(), recordedAt }
          : activeExperiment.outcome
      });
      setExperiments((current) => [experiment, ...current.filter((item) => item.id !== experiment.id)]);
      setObservationDraft('');
      setOutcomeDraft('');
      if (continueWithAdvice) await requestAdvice(experiment.id);
    } catch (saveError: any) {
      setError(saveError?.response?.data?.error || saveError?.message || '实验进展保存失败');
    } finally {
      setSavingExperiment(false);
    }
  };

  const planExperiment = async (directionIndex: number) => {
    if (!workspaceId || !runId) return;
    setPlanningIndex(directionIndex);
    setError(null);
    try {
      const result = await researchApi.planExperiment(workspaceId, runId, directionIndex);
      setAdvice((current) => {
        if (!current) return current;
        const candidateDirections = [...current.candidateDirections];
        candidateDirections[directionIndex] = result.direction;
        return { ...current, candidateDirections, safetyNotes: result.safetyNotes, dataGaps: result.dataGaps };
      });
    } catch (planError: any) {
      setError(planError?.response?.data?.error || planError?.message || '实验方案生成失败');
    } finally {
      setPlanningIndex(null);
    }
  };

  return (
    <section className="flex h-[100dvh] min-h-0 flex-col overflow-hidden bg-[#f6f7f8] text-[#202124]">
      <header className="flex h-14 shrink-0 items-center justify-between border-b border-[#e5e7eb] bg-white px-4">
        <div className="flex min-w-0 items-center gap-3">
          <Link to="/workspaces" className="inline-flex h-8 w-8 items-center justify-center rounded-md text-[#4d5864] hover:bg-[#f1f3f5]">
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <FlaskConical className="h-4 w-4 text-[#147d64]" />
              <h1 className="truncate text-sm font-semibold">{platformLabel}</h1>
            </div>
            <p className="mt-0.5 truncate text-xs text-[#666a70]">
              {stats ? `${stats.documents} 篇论文 · ${stats.nodeCount} 个节点 · ${stats.edgeCount} 条单向证据边` : '科研证据图谱与实验建议'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Link
            to="/profile"
            className="inline-flex h-9 items-center gap-2 rounded-lg border border-[#d8dde4] bg-white px-3 text-sm hover:bg-[#f5f6f7]"
          >
            <UserRoundCog className="h-4 w-4" />
            研究者画像
          </Link>
          <div className="relative hidden sm:block">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-[#8b939d]" />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              onKeyDown={(event) => event.key === 'Enter' && void load()}
              placeholder="检索材料、指标或 Claim"
              className="h-9 w-64 rounded-lg border border-[#d8dde4] pl-9 pr-3 text-sm outline-none focus:border-[#147d64]"
            />
          </div>
          <button type="button" onClick={() => void load()} disabled={loading} className="inline-flex h-9 items-center gap-2 rounded-lg border border-[#d8dde4] bg-white px-3 text-sm hover:bg-[#f5f6f7] disabled:opacity-60">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
            刷新
          </button>
        </div>
      </header>

      {error ? <div className="shrink-0 border-b border-[#ffd6d6] bg-[#fff7f7] px-4 py-2 text-sm text-[#b42318]">{error}</div> : null}

      <div className="grid min-h-0 flex-1 grid-cols-1 overflow-hidden xl:grid-cols-[minmax(0,0.92fr)_minmax(520px,1.08fr)]">
        <div className="min-h-0 overflow-y-auto border-r border-[#e1e4e8] p-5">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              ['论文', stats?.documents || 0, BookOpen],
              ['图谱节点', stats?.nodeCount || 0, Network],
              ['原子观测', stats?.nodes?.observation || 0, Beaker],
              ['论文 Claims', stats?.nodes?.claim || 0, Lightbulb]
            ].map(([label, value, Icon]: any) => (
              <div key={label} className="rounded-xl border border-[#e2e5e9] bg-white p-3 shadow-sm">
                <div className="flex items-center gap-2 text-xs text-[#68717d]"><Icon className="h-4 w-4 text-[#147d64]" />{label}</div>
                <div className="mt-2 text-2xl font-semibold">{value}</div>
              </div>
            ))}
          </div>

          <div className="mt-5 rounded-xl border border-[#e2e5e9] bg-white shadow-sm">
            <div className="flex items-center justify-between border-b border-[#eceef1] px-4 py-3">
              <div>
                <h2 className="text-sm font-semibold">证据节点</h2>
                <p className="mt-0.5 text-xs text-[#737b85]">当前显示 {nodes.length} 个节点，所有边均保留单向来源语义</p>
              </div>
            </div>
            <div className="divide-y divide-[#eef0f2]">
              {Object.entries(nodeGroups).flatMap(([type, group]) => group.slice(0, type === 'paper' ? 8 : 6)).slice(0, 32).map((node) => (
                <div key={node.id} className="px-4 py-3">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="rounded bg-[#eaf5f1] px-1.5 py-0.5 text-[10px] font-medium text-[#176a58]">{nodeTypeLabel[node.type] || node.type}</span>
                        <span className="truncate text-sm font-medium">{node.label}</span>
                      </div>
                      {node.evidence?.[0]?.quote ? <p className="mt-1 line-clamp-2 text-xs leading-5 text-[#666f79]">“{node.evidence[0].quote}”</p> : null}
                    </div>
                    <span className="shrink-0 text-[11px] text-[#7c848e]">{confidenceLabel(node.confidence)}</span>
                  </div>
                </div>
              ))}
              {!nodes.length && !loading ? <div className="px-4 py-12 text-center text-sm text-[#7a828c]">尚未导入科研语料，或没有匹配节点。</div> : null}
            </div>
          </div>
        </div>

        <div className="min-h-0 overflow-y-auto bg-white p-5">
          <div className="mx-auto max-w-3xl">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-[#147d64]" />
              <div>
                <h2 className="text-base font-semibold">{designTitle}</h2>
                <p className="text-xs text-[#737b85]">
                  {thermal
                    ? '输入课题，组合分子筛孔道、酸性、活性相与传质机制，再用实验结果持续修正方向。'
                    : '输入课题，组合分子筛功能与光催化机制，再用实验结果持续修正方向。'}
                </p>
              </div>
            </div>

            <div className="mt-4 border-y border-[#e3e7e5] py-4">
              <div className="flex items-center gap-2 text-sm font-semibold">
                <Workflow className="h-4 w-4 text-[#147d64]" />
                预设课题
              </div>
              <div className="mt-3 grid gap-2 sm:grid-cols-3">
                {activeTopicTemplates.map((topic) => (
                  <button
                    key={topic.id}
                    type="button"
                    onClick={() => {
                      setGoal(topic.goal);
                      setAdvice(null);
                      setRunId(null);
                    }}
                    className="min-h-16 rounded-lg border border-[#dce2df] bg-white px-3 py-2 text-left hover:border-[#147d64] hover:bg-[#f5faf8]"
                  >
                    <div className="text-sm font-medium">{topic.label}</div>
                    <div className="mt-1 line-clamp-2 text-[11px] leading-4 text-[#737b85]">{topic.goal}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-4 rounded-xl border border-[#dfe5e2] bg-[#f8fbfa] p-4">
              <div className="flex items-start gap-3">
                <ClipboardCheck className="mt-0.5 h-4 w-4 shrink-0 text-[#147d64]" />
                <div className="min-w-0 flex-1">
                  <div className="text-sm font-semibold">实验结果回流</div>
                  <p className="mt-0.5 text-xs leading-5 text-[#69736f]">选择已保存实验，记录最新观察；AI 会把课题组结果与论文证据分开处理，并据此修正下一步。</p>
                  <select
                    value={activeExperimentId}
                    onChange={(event) => setActiveExperimentId(event.target.value)}
                    className="mt-3 h-9 w-full rounded-lg border border-[#d6ddd9] bg-white px-3 text-sm outline-none focus:border-[#147d64]"
                  >
                    <option value="">不关联实验：从文献证据生成初始方向</option>
                    {experiments.map((experiment) => (
                      <option key={experiment.id} value={experiment.id}>{experiment.title} · {experiment.status}</option>
                    ))}
                  </select>

                  {activeExperiment ? (
                    <div className="mt-3 space-y-2.5">
                      <div className="grid gap-2 sm:grid-cols-[150px_minmax(0,1fr)]">
                        <select
                          value={experimentStatus}
                          onChange={(event) => setExperimentStatus(event.target.value)}
                          className="h-9 rounded-lg border border-[#d6ddd9] bg-white px-2 text-sm outline-none focus:border-[#147d64]"
                        >
                          <option value="planned">计划中</option>
                          <option value="running">进行中</option>
                          <option value="completed">已完成</option>
                          <option value="failed">未达到目标</option>
                          <option value="stopped">已停止</option>
                        </select>
                        <div className="flex items-center rounded-lg border border-[#e0e5e2] bg-white px-3 text-xs text-[#69736f]">
                          已记录 {activeExperiment.observations.length} 条观察
                        </div>
                      </div>
                      <textarea
                        value={observationDraft}
                        onChange={(event) => setObservationDraft(event.target.value)}
                        rows={2}
                        placeholder="新增观察：样品颜色、降解曲线、循环表现、异常现象、表征变化……"
                        className="w-full resize-none rounded-lg border border-[#d6ddd9] bg-white p-2.5 text-sm leading-5 outline-none focus:border-[#147d64]"
                      />
                      <textarea
                        value={outcomeDraft}
                        onChange={(event) => setOutcomeDraft(event.target.value)}
                        rows={2}
                        placeholder="阶段结论：哪些目标达到或未达到，关键数值和当前判断"
                        className="w-full resize-none rounded-lg border border-[#d6ddd9] bg-white p-2.5 text-sm leading-5 outline-none focus:border-[#147d64]"
                      />
                      <div className="flex flex-wrap gap-2">
                        <button
                          type="button"
                          onClick={() => void saveExperimentProgress(false)}
                          disabled={savingExperiment}
                          className="inline-flex h-9 items-center gap-2 rounded-lg border border-[#cfd8d4] bg-white px-3 text-sm hover:bg-[#f3f7f5] disabled:opacity-50"
                        >
                          {savingExperiment ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
                          保存进展
                        </button>
                        <button
                          type="button"
                          onClick={() => void saveExperimentProgress(true)}
                          disabled={savingExperiment || advising}
                          className="inline-flex h-9 items-center gap-2 rounded-lg bg-[#147d64] px-3 text-sm font-medium text-white hover:bg-[#0f6c55] disabled:opacity-50"
                        >
                          {advising ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                          保存并调整建议
                        </button>
                      </div>
                    </div>
                  ) : null}
                </div>
              </div>
            </div>

            <div className="mt-4">
              <label className="mb-2 block text-xs font-semibold text-[#515a65]">课题目标</label>
              <textarea
                value={goal}
                onChange={(event) => setGoal(event.target.value)}
                rows={4}
                className="w-full resize-none rounded-xl border border-[#d8dde4] bg-[#fbfcfc] p-3 text-sm leading-6 outline-none focus:border-[#147d64] focus:bg-white focus:shadow-none"
                placeholder={thermal
                  ? '输入课题目标；系统将设计分子筛孔道、酸性、活性相、扩散与验证实验'
                  : '输入课题目标；系统将设计分子筛功能、光催化组分、界面耦合与验证实验'}
              />
            </div>

            <div className="mt-3">
              <div className="mb-2 flex items-center justify-between gap-3">
                <label className="block text-xs font-semibold text-[#515a65]">本轮补充要求与向 AI 提问</label>
                <span className="text-[10px] text-[#8a929c]">明确表达的长期偏好会用于更新画像</span>
              </div>
              <textarea
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                rows={3}
                className="w-full resize-none rounded-xl border border-[#d8dde4] bg-white p-3 text-sm leading-6 outline-none focus:border-[#147d64] focus:shadow-none"
                placeholder="说明现有设备、路线偏好、硬性禁区、期望指标，或直接提出需要 AI 回答的问题"
              />
              <div className="mt-2 flex flex-wrap gap-1.5">
                {supplementalQuestionPrompts.map((prompt) => (
                  <button
                    key={prompt}
                    type="button"
                    onClick={() => setQuestion((current) => `${current}${current.trim() ? '\n' : ''}${prompt}`)}
                    className="rounded-md border border-[#e0e4e8] bg-white px-2 py-1 text-[11px] text-[#69717b] hover:border-[#aeb7b2] hover:bg-[#f7f8f8]"
                  >
                    {prompt.replace('：', '')}
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-3">
              {focusOptions.map((option) => (
                <button
                  key={option.id}
                  type="button"
                  onClick={() => setFocus(option.id)}
                  className={`rounded-xl border p-3 text-left transition ${focus === option.id ? 'border-[#147d64] bg-[#edf8f4]' : 'border-[#e0e4e8] hover:bg-[#f7f8f9]'}`}
                >
                  <div className="text-sm font-medium">{option.label}</div>
                  <div className="mt-1 text-[11px] leading-4 text-[#737b85]">{focusDescriptions[option.id]}</div>
                </button>
              ))}
            </div>

            <button
              type="button"
              onClick={() => void requestAdvice()}
              disabled={advising || !goal.trim() || !stats?.documents}
              className="mt-3 inline-flex h-10 items-center gap-2 rounded-lg bg-[#147d64] px-4 text-sm font-medium text-white hover:bg-[#0f6c55] disabled:cursor-not-allowed disabled:opacity-50"
            >
              {advising ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              {advising
                ? '正在检索图谱并设计研究体系…'
                : activeExperiment
                  ? '结合当前实验调整课题方向'
                  : thermal
                    ? '生成分子筛热催化方案'
                    : '生成分子筛-光催化方案'}
            </button>

            {advice ? (
              <div className="mt-5 space-y-4">
                <div className="rounded-xl border border-[#dfe6e3] bg-[#f8fbfa] p-4 text-sm leading-6 text-[#35413e]">{advice.answer}</div>
                {advice.candidateDirections.map((direction, index) => {
                  const hasPlan = direction.nextExperiment.controls.length || direction.nextExperiment.measurements.length;
                  return (
                    <article key={`${direction.title}-${index}`} className="rounded-2xl border border-[#dce2e0] bg-white p-5 shadow-sm">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="rounded-full bg-[#e7f5ef] px-2 py-1 text-[11px] font-medium text-[#147d64]">候选假设</span>
                            <span className="text-xs text-[#6e7781]">证据置信度 {confidenceLabel(direction.confidence)}</span>
                          </div>
                          <h3 className="mt-2 text-base font-semibold leading-6">{direction.title}</h3>
                        </div>
                        <span className="rounded bg-[#f1f3f5] px-2 py-1 text-xs">{direction.feasibility === 'high' ? '高可行性' : direction.feasibility === 'low' ? '低可行性' : '中等可行性'}</span>
                      </div>
                      <p className="mt-3 text-sm leading-6"><span className="font-medium">假设：</span>{direction.hypothesis}</p>
                      <p className="mt-2 text-sm leading-6 text-[#515b65]"><span className="font-medium text-[#30363d]">依据：</span>{direction.rationale}</p>
                      <p className="mt-2 text-sm leading-6 text-[#515b65]"><span className="font-medium text-[#30363d]">潜在创新：</span>{direction.novelty}</p>

                      {direction.couplingDesign ? (
                        <div className="mt-4 border-y border-[#e4e8e6] py-4">
                          <div className="text-xs font-semibold text-[#4e5964]">{thermal ? '分子筛热催化体系原理' : '分子筛-光催化组合原理'}</div>
                          <div className="mt-3 grid gap-x-5 gap-y-3 sm:grid-cols-2">
                            {[
                              ['分子筛作用', direction.couplingDesign.molecularSieveRole],
                              [activePhaseLabel, direction.couplingDesign.photocatalystRole],
                              ['界面策略', direction.couplingDesign.interfaceStrategy],
                              ['选择性目标', direction.couplingDesign.selectivityTarget],
                              ['拟议路径', direction.couplingDesign.proposedPathway],
                              ['证据边界', direction.couplingDesign.evidenceBoundary]
                            ].map(([label, value]) => (
                              <div key={label} className={label === '拟议路径' || label === '证据边界' ? 'sm:col-span-2' : ''}>
                                <div className="text-[11px] font-medium text-[#147d64]">{label}</div>
                                <p className="mt-1 text-xs leading-5 text-[#555f68]">{value || '待实验与补充证据确认'}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      ) : null}

                      <div className="mt-4 rounded-xl bg-[#f7f8f9] p-3">
                        <div className="text-xs font-semibold text-[#4e5964]">引用的图谱证据</div>
                        <div className="mt-2 space-y-2">
                          {direction.supportingEvidence.map((evidence) => (
                            <div key={`${evidence.nodeId}-${evidence.role}`} className="text-xs leading-5 text-[#5e6872]">
                              <span className="font-medium text-[#147d64]">{evidence.role}</span>
                              {evidence.quote ? ` · “${evidence.quote}”` : ` · ${evidence.nodeId}`}
                            </div>
                          ))}
                        </div>
                      </div>

                      {hasPlan ? (
                        <div className="mt-4 rounded-xl border border-[#dfe6e3] p-4">
                          <div className="flex items-center gap-2 text-sm font-semibold"><Beaker className="h-4 w-4 text-[#147d64]" />最小验证实验</div>
                          <p className="mt-2 text-sm leading-6">{direction.nextExperiment.objective}</p>
                          {[
                            ['材料', direction.nextExperiment.materials || []],
                            ['步骤', direction.nextExperiment.procedure || []],
                            ['变量', direction.nextExperiment.variables],
                            ['对照', direction.nextExperiment.controls],
                            ['测量', direction.nextExperiment.measurements],
                            ['迭代判据', direction.nextExperiment.decisionRules || []],
                            ['停止条件', direction.nextExperiment.stoppingCriteria]
                          ].map(([label, items]: any) => (
                            <div key={label} className="mt-3">
                              <div className="text-xs font-medium text-[#65707a]">{label}</div>
                              <div className="mt-1 flex flex-wrap gap-1.5">{items.map((item: string) => <span key={item} className="rounded-md bg-[#f1f4f3] px-2 py-1 text-xs">{item}</span>)}</div>
                            </div>
                          ))}
                          <button
                            type="button"
                            onClick={() => void saveDirectionAsExperiment(direction, index)}
                            disabled={savingExperiment}
                            className="mt-4 inline-flex h-9 items-center gap-2 rounded-lg border border-[#147d64] px-3 text-sm font-medium text-[#147d64] hover:bg-[#edf8f4] disabled:opacity-50"
                          >
                            {savingExperiment ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
                            保存为实验并开始跟踪
                          </button>
                        </div>
                      ) : (
                        <button
                          type="button"
                          onClick={() => void planExperiment(index)}
                          disabled={planningIndex !== null}
                          className="mt-4 inline-flex h-9 items-center gap-2 rounded-lg border border-[#147d64] px-3 text-sm font-medium text-[#147d64] hover:bg-[#edf8f4] disabled:opacity-50"
                        >
                          {planningIndex === index ? <Loader2 className="h-4 w-4 animate-spin" /> : <ChevronRight className="h-4 w-4" />}
                          展开最小验证实验
                        </button>
                      )}
                    </article>
                  );
                })}

                {advice.dataGaps.length ? <Notice title="证据缺口" items={advice.dataGaps} icon={Search} /> : null}
                {advice.safetyNotes.length ? <Notice title="安全与边界" items={advice.safetyNotes} icon={ShieldAlert} tone="warning" /> : null}
                {profileFollowUps.length ? (
                  <div className="rounded-xl border border-[#cfe0da] bg-[#f6fbf9] p-4">
                    <div className="flex items-center gap-2 text-sm font-semibold">
                      <UserRoundCog className="h-4 w-4 text-[#147d64]" />
                      为了让下一轮建议更贴合你，AI 还想确认
                    </div>
                    <div className="mt-3 space-y-3">
                      {profileFollowUps.map((item, index) => (
                        <div key={`${item.category}-${index}`} className="rounded-lg border border-[#dde8e4] bg-white p-3">
                          <div className="text-sm font-medium">{item.question}</div>
                          <p className="mt-1 text-xs leading-5 text-[#6b747c]">{item.reason}</p>
                          <div className="mt-2 flex gap-2">
                            <input
                              value={followUpAnswers[index] || ''}
                              onChange={(event) => setFollowUpAnswers((current) => ({ ...current, [index]: event.target.value }))}
                              disabled={savedFollowUps.includes(index)}
                              className="h-9 min-w-0 flex-1 rounded-lg border border-[#d6ddd9] bg-white px-3 text-sm outline-none focus:border-[#147d64] disabled:bg-[#f1f5f3]"
                              placeholder="回答后会写入可查看、可删除的研究者画像"
                            />
                            <button
                              type="button"
                              disabled={!followUpAnswers[index]?.trim() || savedFollowUps.includes(index)}
                              onClick={() => void saveProfileFollowUp(item, index)}
                              className="h-9 rounded-lg bg-[#147d64] px-3 text-sm font-medium text-white disabled:opacity-50"
                            >
                              {savedFollowUps.includes(index) ? '已写入画像' : '保存回答'}
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : null}
              </div>
            ) : (
              <div className="mt-8 rounded-2xl border border-dashed border-[#d7dcdf] px-6 py-10 text-center">
                <FlaskConical className="mx-auto h-8 w-8 text-[#8a949d]" />
                <p className="mt-3 text-sm font-medium">尚未生成候选方向</p>
                <p className="mt-1 text-xs text-[#737b85]">AI 只会引用当前科研图谱中能够定位的证据节点。</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

function Notice({ title, items, icon: Icon, tone = 'default' }: { title: string; items: string[]; icon: any; tone?: 'default' | 'warning' }) {
  return (
    <div className={`rounded-xl border p-4 ${tone === 'warning' ? 'border-[#f2dfb8] bg-[#fffaf0]' : 'border-[#dfe4e8] bg-[#fafbfc]'}`}>
      <div className="flex items-center gap-2 text-sm font-semibold"><Icon className="h-4 w-4" />{title}</div>
      <ul className="mt-2 space-y-1 text-xs leading-5 text-[#5f6871]">{items.map((item) => <li key={item}>• {item}</li>)}</ul>
    </div>
  );
}

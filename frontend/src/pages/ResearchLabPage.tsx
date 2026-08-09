import { useEffect, useMemo, useState } from 'react';
import {
  ArrowLeft, Beaker, BookOpen, BrainCircuit, CheckCircle2, ChevronRight, CircleDot,
  FlaskConical, LoaderCircle, Network, RefreshCw, Save, Search, ShieldAlert, Sparkles
} from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { Advice, api, Direction, Experiment, GraphNode, Workspace } from '../api';

const nodeColors: Record<string, string> = {
  paper: '#2563eb',
  entity: '#059669',
  keyword: '#7c3aed',
  experiment: '#ea580c',
  observation: '#0891b2',
  claim: '#be123c'
};

const templates = {
  photocatalysis: [
    '设计分子筛与光催化活性相协同的甲烷温和转化体系，优先探索含氧产物并控制过度氧化。',
    '设计分子筛-光催化耦合体系用于塑料降解和高值转化，区分矿化路径与高值产物路径。',
    '设计分子筛-光催化耦合体系用于抗生素降解，同时关注矿化率、毒性、浸出和循环稳定性。'
  ],
  thermal_catalysis: [
    '基于分子筛孔道、酸性和金属位协同，提出甲烷选择性转化的新方向与最小验证实验。',
    '面向废塑料热催化升级回收，设计分子筛孔结构、酸性和扩散协同的产物选择性调控方案。',
    '从热催化图谱中寻找可迁移到分子筛稳定性、抗积碳和低温活化的新研究窗口。'
  ]
};

function GraphPreview({ nodes, edges, onSelect }: {
  nodes: GraphNode[];
  edges: Array<{ id: string; from: string; to: string; type: string }>;
  onSelect: (node: GraphNode) => void;
}) {
  const visible = nodes.slice(0, 70);
  const positions = useMemo(() => {
    const map = new Map<string, { x: number; y: number }>();
    visible.forEach((node, index) => {
      const ring = index % 3;
      const angle = index * 2.399963;
      const radius = 65 + ring * 66 + Math.floor(index / 18) * 5;
      map.set(node.id, { x: 260 + Math.cos(angle) * radius, y: 220 + Math.sin(angle) * radius });
    });
    return map;
  }, [visible.map((node) => node.id).join('|')]);
  const visibleEdges = edges.filter((edge) => positions.has(edge.from) && positions.has(edge.to)).slice(0, 140);

  if (!visible.length) return <div className="empty-state">当前筛选没有图谱节点。</div>;
  return (
    <svg className="graph-canvas" viewBox="0 0 520 440" role="img" aria-label="知识图谱预览">
      <g opacity="0.22">
        {visibleEdges.map((edge) => {
          const from = positions.get(edge.from)!;
          const to = positions.get(edge.to)!;
          return <line key={edge.id} x1={from.x} y1={from.y} x2={to.x} y2={to.y} stroke="#52606d" strokeWidth="0.8" />;
        })}
      </g>
      {visible.map((node) => {
        const position = positions.get(node.id)!;
        const radius = node.type === 'paper' ? 6 : node.type === 'claim' ? 5 : 4;
        return (
          <g key={node.id} transform={`translate(${position.x} ${position.y})`} className="graph-node" onClick={() => onSelect(node)}>
            <circle r={radius + 5} fill="transparent" />
            <circle r={radius} fill={nodeColors[node.type] || '#64748b'} opacity={node.reviewStatus === 'needs_review' ? 0.55 : 0.9} />
          </g>
        );
      })}
    </svg>
  );
}

const ListBlock = ({ title, items }: { title: string; items: string[] }) => (
  items.length ? (
    <div className="detail-block">
      <h4>{title}</h4>
      <ul>{items.map((item, index) => <li key={`${title}-${index}`}>{item}</li>)}</ul>
    </div>
  ) : null
);

function DirectionCard({ direction, index, runId, workspaceId, onUpdated, onSaved }: {
  direction: Direction;
  index: number;
  runId: string;
  workspaceId: string;
  onUpdated: (direction: Direction) => void;
  onSaved: (experiment: Experiment) => void;
}) {
  const [planning, setPlanning] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const plan = async () => {
    setPlanning(true);
    setError('');
    try { onUpdated((await api.plan(workspaceId, runId, index)).direction); }
    catch (e) { setError(e instanceof Error ? e.message : '方案生成失败'); }
    finally { setPlanning(false); }
  };
  const save = async () => {
    setSaving(true);
    setError('');
    try {
      const result = await api.saveExperiment(workspaceId, {
        title: direction.title,
        objective: direction.nextExperiment.objective || direction.hypothesis,
        status: 'planned',
        materials: direction.nextExperiment.materials,
        procedure: direction.nextExperiment.procedure,
        conditions: {
          variables: direction.nextExperiment.variables,
          controls: direction.nextExperiment.controls,
          measurements: direction.nextExperiment.measurements
        },
        observations: [],
        outcome: {},
        constraints: {
          sourceAdviceRunId: runId,
          directionIndex: index,
          hypothesis: direction.hypothesis,
          evidence: direction.supportingEvidence
        },
        source: 'research_advice'
      });
      onSaved(result.experiment);
    } catch (e) { setError(e instanceof Error ? e.message : '实验保存失败'); }
    finally { setSaving(false); }
  };
  return (
    <article className="direction-card">
      <div className="direction-head">
        <div>
          <span className={`feasibility ${direction.feasibility}`}>{direction.feasibility}</span>
          <span className="confidence">置信度 {Math.round(direction.confidence * 100)}%</span>
          <h3>{direction.title}</h3>
        </div>
        <Sparkles size={22} />
      </div>
      <div className="hypothesis"><strong>研究假设</strong><p>{direction.hypothesis}</p></div>
      <div className="two-column-detail">
        <div><h4>推理依据</h4><p>{direction.rationale}</p></div>
        <div><h4>预期创新</h4><p>{direction.novelty}</p></div>
      </div>
      <div className="system-design">
        <div><span>分子筛作用</span><p>{direction.systemDesign.molecularSieveRole}</p></div>
        <div><span>活性相作用</span><p>{direction.systemDesign.activePhaseRole}</p></div>
        <div><span>界面策略</span><p>{direction.systemDesign.interfaceStrategy}</p></div>
        <div><span>拟议路径</span><p>{direction.systemDesign.proposedPathway}</p></div>
        <div><span>选择性目标</span><p>{direction.systemDesign.selectivityTarget}</p></div>
        <div><span>证据边界</span><p>{direction.systemDesign.evidenceBoundary}</p></div>
      </div>
      <div className="evidence-list">
        <h4>支持证据</h4>
        {direction.supportingEvidence.map((item, evidenceIndex) => (
          <div key={`${item.nodeId}-${evidenceIndex}`}><code>{item.nodeId.slice(-10)}</code><span>{item.role}</span><p>{item.quote || '证据节点已记录，未附短引文。'}</p></div>
        ))}
      </div>
      {direction.nextExperiment.objective && (
        <div className="experiment-plan">
          <h4><Beaker size={17} /> 首轮判别实验</h4>
          <p>{direction.nextExperiment.objective}</p>
          <ListBlock title="材料" items={direction.nextExperiment.materials} />
          <ListBlock title="步骤" items={direction.nextExperiment.procedure} />
          <ListBlock title="变量" items={direction.nextExperiment.variables} />
          <ListBlock title="对照" items={direction.nextExperiment.controls} />
          <ListBlock title="测量" items={direction.nextExperiment.measurements} />
          <ListBlock title="判定规则" items={direction.nextExperiment.decisionRules} />
          <ListBlock title="停止条件" items={direction.nextExperiment.stoppingCriteria} />
        </div>
      )}
      {error && <div className="error-box">{error}</div>}
      <div className="card-actions">
        <button className="secondary-button" onClick={() => void plan()} disabled={planning}>
          {planning ? <LoaderCircle className="spin" size={17} /> : <BrainCircuit size={17} />}
          完善实验方案
        </button>
        <button className="primary-button compact" onClick={() => void save()} disabled={saving}>
          {saving ? <LoaderCircle className="spin" size={17} /> : <Save size={17} />}
          保存为实验
        </button>
      </div>
    </article>
  );
}

export default function ResearchLabPage() {
  const { id = '' } = useParams();
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [stats, setStats] = useState<any>(null);
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<Array<{ id: string; from: string; to: string; type: string }>>([]);
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [search, setSearch] = useState('');
  const [goal, setGoal] = useState('');
  const [focus, setFocus] = useState('performance');
  const [advice, setAdvice] = useState<Advice | null>(null);
  const [runId, setRunId] = useState('');
  const [activeTab, setActiveTab] = useState<'graph' | 'advice' | 'experiments'>('graph');
  const [activeExperimentId, setActiveExperimentId] = useState('');
  const [observation, setObservation] = useState('');
  const [outcome, setOutcome] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const load = async (query = '') => {
    setBusy(true);
    setError('');
    try {
      const [workspaceResult, statsResult, graphResult, experimentResult] = await Promise.all([
        api.workspace(id), api.stats(id), api.graph(id, query), api.experiments(id)
      ]);
      setWorkspace(workspaceResult.workspace);
      setStats(statsResult);
      setNodes(graphResult.nodes);
      setEdges(graphResult.edges);
      setExperiments(experimentResult.experiments);
      if (!goal) setGoal(templates[workspaceResult.workspace.catalysisSystem][0]);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : '加载失败');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => { void load(); }, [id]);
  const activeExperiment = experiments.find((item) => item.id === activeExperimentId) || null;

  const requestAdvice = async () => {
    if (!goal.trim()) return;
    setBusy(true);
    setError('');
    try {
      const result = await api.advice(id, {
        goal: goal.trim(),
        focus,
        experimentId: activeExperimentId || null,
        preferredDirectionCount: 2,
        question: activeExperimentId
          ? '结合当前实验最新观察，判断旧假设应保留、修正还是停止，并提出信息增益最高的下一步。'
          : undefined,
        constraints: { evidenceGrounded: true, requireFeedbackLoop: true }
      });
      setAdvice(result.advice);
      setRunId(result.runId);
      setActiveTab('advice');
    } catch (adviceError) {
      setError(adviceError instanceof Error ? adviceError.message : 'AI 建议生成失败');
    } finally {
      setBusy(false);
    }
  };

  const saveFeedback = async (continueAdvice: boolean) => {
    if (!activeExperiment) return;
    setBusy(true);
    setError('');
    try {
      const recordedAt = new Date().toISOString();
      const result = await api.saveExperiment(id, {
        ...activeExperiment,
        observations: observation.trim()
          ? [...activeExperiment.observations, { text: observation.trim(), recordedAt }]
          : activeExperiment.observations,
        outcome: outcome.trim()
          ? { ...activeExperiment.outcome, latestSummary: outcome.trim(), recordedAt }
          : activeExperiment.outcome
      });
      setExperiments((items) => [result.experiment, ...items.filter((item) => item.id !== result.experiment.id)]);
      setObservation('');
      setOutcome('');
      if (continueAdvice) await requestAdvice();
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : '反馈保存失败');
    } finally {
      setBusy(false);
    }
  };

  const systemLabel = workspace?.catalysisSystem === 'thermal_catalysis' ? '热催化' : '光催化';
  const systemTemplates = workspace ? templates[workspace.catalysisSystem] : templates.photocatalysis;

  return (
    <main className="lab-page">
      <header className="lab-topbar">
        <div className="heading-with-back">
          <Link to="/workspaces" className="icon-button"><ArrowLeft size={18} /></Link>
          <div>
            <p className="eyebrow">{workspace?.catalysisSystem?.toUpperCase().replace('_', ' ') || 'RESEARCH LAB'}</p>
            <h1>{workspace?.name || '催化科研实验平台'}</h1>
          </div>
        </div>
        <div className="topbar-actions">
          <Link to="/profile" className="secondary-button"><BrainCircuit size={17} />研究者画像</Link>
          <button className="icon-button" onClick={() => void load(search)}><RefreshCw size={18} className={busy ? 'spin' : ''} /></button>
        </div>
      </header>

      {error && <div className="error-box lab-error">{error}</div>}
      <section className="lab-summary">
        <div><BookOpen size={18} /><strong>{stats?.documents || 0}</strong><span>论文</span></div>
        <div><CircleDot size={18} /><strong>{stats?.nodeCount || 0}</strong><span>节点</span></div>
        <div><Network size={18} /><strong>{stats?.edgeCount || 0}</strong><span>证据边</span></div>
        <div><Beaker size={18} /><strong>{experiments.length}</strong><span>实验记录</span></div>
      </section>

      <nav className="lab-tabs">
        <button className={activeTab === 'graph' ? 'active' : ''} onClick={() => setActiveTab('graph')}><Network size={17} />证据图谱</button>
        <button className={activeTab === 'advice' ? 'active' : ''} onClick={() => setActiveTab('advice')}><Sparkles size={17} />方向预测</button>
        <button className={activeTab === 'experiments' ? 'active' : ''} onClick={() => setActiveTab('experiments')}><FlaskConical size={17} />实验闭环</button>
      </nav>

      {activeTab === 'graph' && (
        <section className="lab-grid">
          <div className="panel">
            <div className="panel-head">
              <div><p className="eyebrow">EVIDENCE GRAPH</p><h2>{systemLabel}单向证据图</h2></div>
              <div className="search-box"><Search size={17} /><input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && void load(search)} placeholder="检索材料、反应、指标或 Claim" /></div>
            </div>
            <GraphPreview nodes={nodes} edges={edges} onSelect={setSelectedNode} />
            <div className="legend">
              {Object.entries(nodeColors).map(([type, color]) => <span key={type}><i style={{ background: color }} />{type}</span>)}
            </div>
          </div>
          <aside className="panel node-panel">
            <p className="eyebrow">NODE INSPECTOR</p>
            {selectedNode ? (
              <>
                <span className="node-type">{selectedNode.type}</span>
                <h2>{selectedNode.label}</h2>
                <div className="node-meta"><span>置信度 {Math.round(selectedNode.confidence * 100)}%</span><span>{selectedNode.reviewStatus}</span></div>
                <pre>{JSON.stringify(selectedNode.data, null, 2)}</pre>
                {selectedNode.evidence.slice(0, 3).map((item, index) => (
                  <blockquote key={index}>{String(item.quote || '无短引文')}<small>p.{String(item.pdf_page_index ?? '?')} · {String(item.evidence_validation || '')}</small></blockquote>
                ))}
              </>
            ) : <div className="empty-state">点击图中的节点查看论文事实与原文证据。</div>}
          </aside>
        </section>
      )}

      {activeTab === 'advice' && (
        <section className="advice-layout">
          <aside className="panel request-panel">
            <p className="eyebrow">RESEARCH ORCHESTRATOR</p>
            <h2>提出一个研究课题</h2>
            <p className="muted">系统将检索当前 {systemLabel} 图谱，结合研究者画像生成证据约束的候选假设。</p>
            <div className="template-row">
              {systemTemplates.map((item, index) => <button key={index} onClick={() => setGoal(item)}>课题 {index + 1}</button>)}
            </div>
            <label>研究目标<textarea value={goal} onChange={(e) => setGoal(e.target.value)} /></label>
            <label>优先关注
              <select value={focus} onChange={(e) => setFocus(e.target.value)}>
                <option value="performance">性能与机理</option>
                <option value="engineering">工程可用性</option>
                <option value="gap">证据空白与新颖性</option>
              </select>
            </label>
            <label>结合实验记录
              <select value={activeExperimentId} onChange={(e) => setActiveExperimentId(e.target.value)}>
                <option value="">不绑定实验</option>
                {experiments.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}
              </select>
            </label>
            <button className="primary-button" onClick={() => void requestAdvice()} disabled={busy || !goal.trim()}>
              {busy ? <LoaderCircle className="spin" size={18} /> : <Sparkles size={18} />}生成研究方向
            </button>
          </aside>
          <div className="advice-results">
            {advice ? (
              <>
                <div className="panel answer-card"><p className="eyebrow">ORCHESTRATOR SUMMARY</p><p>{advice.answer}</p></div>
                {advice.candidateDirections.map((direction, index) => (
                  <DirectionCard
                    key={`${direction.title}-${index}`}
                    direction={direction}
                    index={index}
                    runId={runId}
                    workspaceId={id}
                    onUpdated={(updated) => setAdvice((current) => current ? {
                      ...current,
                      candidateDirections: current.candidateDirections.map((item, itemIndex) => itemIndex === index ? updated : item)
                    } : current)}
                    onSaved={(experiment) => {
                      setExperiments((items) => [experiment, ...items.filter((item) => item.id !== experiment.id)]);
                      setActiveExperimentId(experiment.id);
                    }}
                  />
                ))}
                <div className="panel evidence-boundaries">
                  <ListBlock title="证据冲突" items={advice.contradictions} />
                  <ListBlock title="数据缺口" items={advice.dataGaps} />
                  <ListBlock title="安全边界" items={advice.safetyNotes} />
                </div>
              </>
            ) : <div className="panel empty-state tall"><Sparkles size={30} /><p>填写课题后生成候选方向。AI 不会把待验证假设伪装成论文结论。</p></div>}
          </div>
        </section>
      )}

      {activeTab === 'experiments' && (
        <section className="experiment-layout">
          <aside className="panel experiment-list">
            <p className="eyebrow">EXPERIMENT LEDGER</p>
            <h2>实验记录</h2>
            {experiments.length ? experiments.map((item) => (
              <button key={item.id} className={activeExperimentId === item.id ? 'active' : ''} onClick={() => setActiveExperimentId(item.id)}>
                <span>{item.status}</span><strong>{item.title}</strong><ChevronRight size={17} />
              </button>
            )) : <div className="empty-state">从候选方向中保存首个实验方案。</div>}
          </aside>
          <div className="panel feedback-panel">
            {activeExperiment ? (
              <>
                <div className="direction-head"><div><p className="eyebrow">EXPERIMENT FEEDBACK</p><h2>{activeExperiment.title}</h2></div><CheckCircle2 size={23} /></div>
                <p className="muted">{activeExperiment.objective}</p>
                <div className="experiment-snapshot">
                  <div><h4>材料</h4><pre>{JSON.stringify(activeExperiment.materials, null, 2)}</pre></div>
                  <div><h4>条件与对照</h4><pre>{JSON.stringify(activeExperiment.conditions, null, 2)}</pre></div>
                </div>
                <label>新增实验观察<textarea value={observation} onChange={(e) => setObservation(e.target.value)} placeholder="记录转化率、选择性、表征变化、失活、异常现象等；不要把推测写成观测。" /></label>
                <label>阶段性结论<textarea value={outcome} onChange={(e) => setOutcome(e.target.value)} placeholder="说明当前结果支持、削弱或否定了什么。" /></label>
                <div className="card-actions">
                  <button className="secondary-button" onClick={() => void saveFeedback(false)} disabled={busy}><Save size={17} />保存记录</button>
                  <button className="primary-button compact" onClick={() => void saveFeedback(true)} disabled={busy}><Sparkles size={17} />保存并生成下一步</button>
                </div>
              </>
            ) : <div className="empty-state tall"><ShieldAlert size={30} /><p>选择一条实验记录，录入观察和阶段性结果。</p></div>}
          </div>
        </section>
      )}
    </main>
  );
}

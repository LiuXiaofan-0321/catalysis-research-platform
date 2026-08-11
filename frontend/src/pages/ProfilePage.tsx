import { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, BrainCircuit, MessageCircleQuestion, Save, Trash2, UserRoundCog } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api, ResearcherProfile } from '../api';

const emptyProfile: ResearcherProfile = {
  institution: '',
  role: '',
  primaryCatalysis: 'undecided',
  molecularSievePreference: 'when_helpful',
  heterojunctionPreference: 'evidence_based',
  riskTolerance: 'balanced',
  researchInterests: [],
  catalystSystems: [],
  techniques: [],
  currentGoals: [],
  researchPriorities: [],
  availableResources: [],
  avoidances: [],
  experimentalConstraints: {},
  preferredOutputStyle: 'evidence_first',
  openResearchContext: '',
  notes: '',
  learnedPreferences: [],
  interviewAnswers: {}
};

const join = (values: string[]) => values.join('，');
const split = (value: string) => value.split(/[,，;\n]/).map((item) => item.trim()).filter(Boolean);
const valueOf = (value: unknown) => typeof value === 'string' ? value : '';

const learningLabels: Record<string, string> = {
  research_interest: '研究兴趣',
  catalyst_system: '催化体系',
  technique: '技术能力',
  goal: '长期目标',
  constraint: '实验约束',
  output_style: '输出偏好',
  avoidance: '明确禁区',
  resource: '可用资源'
};

const priorityOptions = [
  ['performance', '性能提升'],
  ['mechanism', '机理清晰'],
  ['engineering', '工程可行'],
  ['novelty', '研究新颖性'],
  ['cost', '成本控制'],
  ['sustainability', '绿色与安全']
] as const;

const controlClass = 'mt-2 w-full rounded-lg border border-[#d9dde2] bg-white px-3 py-2.5 text-sm leading-6 outline-none focus:border-[#747c86] focus:shadow-none';
const sectionClass = 'border-t border-[#eceef0] py-7';
const sectionHeadingClass = 'mb-5 flex flex-col justify-between gap-2 sm:flex-row sm:items-end';

export default function ProfilePage() {
  const [profile, setProfile] = useState<ResearcherProfile>(emptyProfile);
  const [maxTemperature, setMaxTemperature] = useState('');
  const [pressureCapability, setPressureCapability] = useState('');
  const [otherConstraints, setOtherConstraints] = useState('');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    api.profile().then(({ profile: value }) => {
      setProfile(value);
      setMaxTemperature(valueOf(value.experimentalConstraints?.maxTemperature));
      setPressureCapability(valueOf(value.experimentalConstraints?.pressureCapability));
      setOtherConstraints(valueOf(value.experimentalConstraints?.other));
    }).catch((loadError) => setError(loadError instanceof Error ? loadError.message : '画像加载失败'));
  }, []);

  const completion = useMemo(() => {
    const signals = [
      profile.primaryCatalysis !== 'undecided',
      Boolean(profile.role),
      profile.researchInterests.length > 0,
      profile.currentGoals.length > 0,
      profile.availableResources.length > 0,
      profile.avoidances.length > 0,
      Boolean(profile.openResearchContext)
    ];
    return Math.round(signals.filter(Boolean).length / signals.length * 100);
  }, [profile]);

  const field = <K extends keyof ResearcherProfile>(key: K, value: ResearcherProfile[K]) =>
    setProfile((current) => ({ ...current, [key]: value }));
  const listField = (
    key: 'researchInterests' | 'catalystSystems' | 'techniques' | 'currentGoals' | 'availableResources' | 'avoidances',
    value: string
  ) => field(key, split(value));
  const togglePriority = (value: string) => field(
    'researchPriorities',
    profile.researchPriorities.includes(value)
      ? profile.researchPriorities.filter((item) => item !== value)
      : [...profile.researchPriorities, value]
  );

  const save = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      const experimentalConstraints = {
        ...profile.experimentalConstraints,
        maxTemperature: maxTemperature.trim(),
        pressureCapability: pressureCapability.trim(),
        other: otherConstraints.trim()
      };
      const result = await api.updateProfile({ ...profile, experimentalConstraints });
      setProfile(result.profile);
      setMessage('研究者画像已保存，后续 AI 建议会按这些偏好和约束进行排序。');
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : '保存失败');
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="min-h-[100dvh] bg-white text-[#202124]">
      <header className="sticky top-0 z-10 flex min-h-14 items-center justify-between border-b border-[#eceef0] bg-white/95 px-4 backdrop-blur sm:px-6">
        <div className="flex items-center gap-3">
          <Link to="/workspaces" className="grid h-9 w-9 place-items-center rounded-lg border border-[#e0e3e7] hover:bg-[#f6f6f7]" title="返回工作空间">
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div>
            <p className="text-[10px] font-medium uppercase text-[#8a929c]">Researcher Profile</p>
            <h1 className="text-sm font-semibold sm:text-base">研究者画像</h1>
          </div>
        </div>
        <button className="inline-flex h-9 items-center gap-2 rounded-lg bg-[#202124] px-4 text-sm font-medium text-white disabled:opacity-50" onClick={() => void save()} disabled={busy}>
          <Save className="h-4 w-4" />{busy ? '保存中…' : '保存画像'}
        </button>
      </header>

      <div className="mx-auto max-w-5xl px-5 py-8 sm:px-8">
        <section className="grid gap-5 border-b border-[#eceef0] pb-7 sm:grid-cols-[auto_minmax(0,1fr)_120px] sm:items-center">
          <span className="grid h-11 w-11 place-items-center rounded-lg border border-[#dfe3e7] bg-[#fafafa]">
            <UserRoundCog className="h-5 w-5" />
          </span>
          <div>
            <h2 className="text-base font-semibold">画像约束建议，但不改变论文事实</h2>
            <p className="mt-1 text-sm leading-6 text-[#7a828c]">你填写的内容优先级最高；AI 只学习对话中明确表达、可长期复用的偏好，学习记录可查看和删除。</p>
          </div>
          <div className="sm:text-right">
            <strong className="block text-2xl font-semibold">{completion}%</strong>
            <span className="text-xs text-[#858d97]">画像完整度</span>
          </div>
        </section>

        {error && <div className="mt-5 rounded-lg border border-[#ffd4d4] bg-[#fff7f7] px-3 py-2 text-sm text-[#b42318]">{error}</div>}
        {message && <div className="mt-5 rounded-lg border border-[#bee6d5] bg-[#f4fbf8] px-3 py-2 text-sm text-[#176a58]">{message}</div>}

        <Link to="/profile/interview" className="mt-6 flex items-center gap-4 rounded-lg border border-[#dfe3e7] px-4 py-4 hover:bg-[#fafafa]">
          <MessageCircleQuestion className="h-5 w-5 shrink-0" />
          <div className="min-w-0 flex-1">
            <strong className="block text-sm">继续九题画像访谈</strong>
            <span className="mt-1 block text-xs leading-5 text-[#7a828c]">逐题补充研究对象、阶段目标、资源边界、风险偏好和成功标准。</span>
          </div>
          <span className="text-xs text-[#8a929c]">打开访谈</span>
        </Link>

        <section className={sectionClass}>
          <div className={sectionHeadingClass}>
            <div><p className="text-[10px] font-medium uppercase text-[#8a929c]">Research Direction</p><h2 className="mt-1 text-lg font-semibold">研究方向与方法偏好</h2></div>
            <p className="text-xs text-[#7a828c]">决定 AI 优先检索和推荐什么，不会改变证据本身。</p>
          </div>
          <div className="grid gap-x-5 gap-y-4 sm:grid-cols-2">
          <label className="text-xs font-medium">学校或机构<input className={controlClass} value={profile.institution} onChange={(e) => field('institution', e.target.value)} /></label>
          <label className="text-xs font-medium">角色/研究阶段<input className={controlClass} value={profile.role} onChange={(e) => field('role', e.target.value)} placeholder="硕士生、博士生、实验负责人…" /></label>
          <label className="text-xs font-medium">主要催化方向
            <select className={controlClass} value={profile.primaryCatalysis} onChange={(e) => field('primaryCatalysis', e.target.value as ResearcherProfile['primaryCatalysis'])}>
              <option value="undecided">尚未确定</option>
              <option value="photocatalysis">以光催化为主</option>
              <option value="thermal_catalysis">以热催化为主</option>
              <option value="both">光催化与热催化都做</option>
            </select>
          </label>
          <label className="text-xs font-medium">建议表达方式
            <select className={controlClass} value={profile.preferredOutputStyle} onChange={(e) => field('preferredOutputStyle', e.target.value)}>
              <option value="evidence_first">证据优先</option>
              <option value="experiment_first">实验优先</option>
              <option value="mechanism_first">机理优先</option>
              <option value="concise">精炼汇报</option>
            </select>
          </label>
          <label className="text-xs font-medium">分子筛在方案中的位置
            <select className={controlClass} value={profile.molecularSievePreference} onChange={(e) => field('molecularSievePreference', e.target.value as ResearcherProfile['molecularSievePreference'])}>
              <option value="central">优先作为核心设计</option>
              <option value="when_helpful">有明确作用时使用</option>
              <option value="minimal">尽量减少依赖</option>
            </select>
          </label>
          <label className="text-xs font-medium">异质结方案偏好
            <select className={controlClass} value={profile.heterojunctionPreference} onChange={(e) => field('heterojunctionPreference', e.target.value as ResearcherProfile['heterojunctionPreference'])}>
              <option value="prefer">愿意优先探索</option>
              <option value="evidence_based">有证据支持时采用</option>
              <option value="avoid_overuse">避免过度堆叠</option>
            </select>
          </label>
          <label className="text-xs font-medium">新方向风险偏好
            <select className={controlClass} value={profile.riskTolerance} onChange={(e) => field('riskTolerance', e.target.value as ResearcherProfile['riskTolerance'])}>
              <option value="conservative">稳健优先</option>
              <option value="balanced">平衡探索</option>
              <option value="exploratory">高风险探索</option>
            </select>
          </label>
          <label className="text-xs font-medium sm:col-span-2">研究兴趣<textarea className={controlClass} value={join(profile.researchInterests)} onChange={(e) => listField('researchInterests', e.target.value)} placeholder="分子筛、甲烷转化、塑料升级回收…" /></label>
          <label className="text-xs font-medium sm:col-span-2">熟悉的催化体系<textarea className={controlClass} value={join(profile.catalystSystems)} onChange={(e) => listField('catalystSystems', e.target.value)} /></label>
          <div className="sm:col-span-2">
            <span className="text-xs font-medium">研究决策优先级</span>
            <div className="mt-2 grid gap-2 sm:grid-cols-3">
              {priorityOptions.map(([value, label]) => (
                <label key={value} className="flex min-h-10 items-center gap-2 rounded-lg border border-[#e0e3e7] px-3 text-xs font-medium hover:bg-[#fafafa]">
                  <input className="h-4 w-4 accent-[#202124]" type="checkbox" checked={profile.researchPriorities.includes(value)} onChange={() => togglePriority(value)} />
                  <span>{label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className={sectionClass}>
        <div className={sectionHeadingClass}>
          <div><p className="text-[10px] font-medium uppercase text-[#8a929c]">Feasibility Boundary</p><h2 className="mt-1 text-lg font-semibold">能力、资源与硬约束</h2></div>
          <p className="text-xs text-[#7a828c]">这些条件直接影响候选方案的可行性排序。</p>
        </div>
        <div className="grid gap-x-5 gap-y-4 sm:grid-cols-2">
          <label className="text-xs font-medium sm:col-span-2">现有表征和实验技术<textarea className={controlClass} value={join(profile.techniques)} onChange={(e) => listField('techniques', e.target.value)} placeholder="XRD、BET、GC-MS、原位红外…" /></label>
          <label className="text-xs font-medium sm:col-span-2">可用设备、材料或合作资源<textarea className={controlClass} value={join(profile.availableResources)} onChange={(e) => listField('availableResources', e.target.value)} /></label>
          <label className="text-xs font-medium">最高温度范围<input className={controlClass} value={maxTemperature} onChange={(e) => setMaxTemperature(e.target.value)} placeholder="例如：不超过 500 °C" /></label>
          <label className="text-xs font-medium">压力能力<input className={controlClass} value={pressureCapability} onChange={(e) => setPressureCapability(e.target.value)} placeholder="例如：仅常压；最高 2 MPa" /></label>
          <label className="text-xs font-medium sm:col-span-2">其他实验约束<textarea className={controlClass} value={otherConstraints} onChange={(e) => setOtherConstraints(e.target.value)} placeholder="时间、样品量、安全、预算或测试周期等" /></label>
          <label className="text-xs font-medium sm:col-span-2">明确禁区<textarea className={controlClass} value={join(profile.avoidances)} onChange={(e) => listField('avoidances', e.target.value)} placeholder="不使用贵金属、避免高压、不要无证据堆叠异质结…" /></label>
        </div>
      </section>

      <section className={sectionClass}>
        <div className={sectionHeadingClass}>
          <div><p className="text-[10px] font-medium uppercase text-[#8a929c]">Open Context</p><h2 className="mt-1 text-lg font-semibold">当前目标与开放信息</h2></div>
          <p className="text-xs text-[#7a828c]">可以用自然语言告诉 AI 哪些背景很重要。</p>
        </div>
        <div className="grid gap-4">
          <label className="text-xs font-medium">当前研究目标<textarea className={controlClass} value={join(profile.currentGoals)} onChange={(e) => listField('currentGoals', e.target.value)} /></label>
          <label className="text-xs font-medium">影响研究决策的其他背景<textarea className={controlClass} value={profile.openResearchContext} onChange={(e) => field('openResearchContext', e.target.value)} placeholder="课题周期、合作团队、希望形成论文还是工程验证、当前最困扰的问题…" /></label>
          <label className="text-xs font-medium">补充说明<textarea className={controlClass} value={profile.notes} onChange={(e) => field('notes', e.target.value)} /></label>
        </div>
      </section>

      <section className={sectionClass}>
        <div className={sectionHeadingClass}>
          <div><p className="text-[10px] font-medium uppercase text-[#8a929c]">Learned From Conversations</p><h2 className="mt-1 text-lg font-semibold">AI 从交流中学到的画像</h2></div>
          <p className="text-xs text-[#7a828c]">{profile.interactionCount || 0} 次画像学习检查，当前保留 {profile.learnedPreferences.length} 条。</p>
        </div>
        {profile.learnedPreferences.length ? (
          <div className="divide-y divide-[#eceef0] border-y border-[#eceef0]">
            {profile.learnedPreferences.map((item) => (
              <article key={item.id} className="grid grid-cols-[36px_minmax(0,1fr)_36px] gap-3 py-4">
                <div className="grid h-9 w-9 place-items-center rounded-lg bg-[#f1f2f3]"><BrainCircuit className="h-4 w-4" /></div>
                <div className="min-w-0">
                  <div className="flex flex-wrap gap-1.5">
                    <span className="rounded bg-[#f0f1f2] px-1.5 py-0.5 text-[10px] text-[#5f6872]">{learningLabels[item.category] || item.category}</span>
                    <span className="rounded bg-[#f0f1f2] px-1.5 py-0.5 text-[10px] text-[#5f6872]">置信度 {Math.round(item.confidence * 100)}%</span>
                    {item.occurrences > 1 && <span className="rounded bg-[#f0f1f2] px-1.5 py-0.5 text-[10px] text-[#5f6872]">确认 {item.occurrences} 次</span>}
                  </div>
                  <strong className="mt-2 block text-sm font-medium">{item.value}</strong>
                  <p className="mt-1 text-xs leading-5 text-[#7a828c]">依据：{item.evidence || '本轮对话中的明确表达'}</p>
                </div>
                <button
                  className="grid h-9 w-9 place-items-center rounded-lg text-[#9b3434] hover:bg-[#fff2f2]"
                  title="删除这条学习记录"
                  onClick={() => field('learnedPreferences', profile.learnedPreferences.filter((entry) => entry.id !== item.id))}
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </article>
            ))}
          </div>
        ) : (
          <div className="grid min-h-32 place-items-center border-y border-dashed border-[#dfe3e7] px-5 text-center text-sm text-[#7a828c]">
            <div><BrainCircuit className="mx-auto h-5 w-5" /><p className="mt-2">暂无对话学习记录。AI 不会从论文事实或一次性课题中推断你的长期偏好。</p></div>
          </div>
        )}
      </section>
      </div>
    </main>
  );
}

import { useEffect, useState } from 'react';
import { ArrowLeft, Save, UserRoundCog } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api, ResearcherProfile } from '../api';

const emptyProfile: ResearcherProfile = {
  institution: '',
  role: '',
  researchInterests: [],
  catalystSystems: [],
  techniques: [],
  currentGoals: [],
  experimentalConstraints: {},
  preferredOutputStyle: 'evidence_first',
  notes: ''
};

const join = (values: string[]) => values.join('，');
const split = (value: string) => value.split(/[,，;\n]/).map((item) => item.trim()).filter(Boolean);

export default function ProfilePage() {
  const [profile, setProfile] = useState<ResearcherProfile>(emptyProfile);
  const [constraints, setConstraints] = useState('{}');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    api.profile().then(({ profile }) => {
      setProfile(profile);
      setConstraints(JSON.stringify(profile.experimentalConstraints || {}, null, 2));
    }).catch((loadError) => setError(loadError instanceof Error ? loadError.message : '画像加载失败'));
  }, []);

  const field = (key: keyof ResearcherProfile, value: string) =>
    setProfile((current) => ({ ...current, [key]: value }));
  const listField = (key: keyof ResearcherProfile, value: string) =>
    setProfile((current) => ({ ...current, [key]: split(value) }));

  const save = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      const parsedConstraints = JSON.parse(constraints || '{}');
      const result = await api.updateProfile({ ...profile, experimentalConstraints: parsedConstraints });
      setProfile(result.profile);
      setMessage('研究者画像已保存，后续 AI 建议会结合这些条件。');
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : '保存失败');
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="app-page narrow-page">
      <header className="topbar">
        <div className="heading-with-back">
          <Link to="/workspaces" className="icon-button"><ArrowLeft size={18} /></Link>
          <div><p className="eyebrow">RESEARCHER PROFILE</p><h1>研究者画像</h1></div>
        </div>
        <button className="primary-button compact" onClick={() => void save()} disabled={busy}>
          <Save size={17} /> {busy ? '保存中…' : '保存画像'}
        </button>
      </header>

      <section className="profile-intro">
        <UserRoundCog size={30} />
        <div>
          <h2>画像用于约束建议，不用于改变论文事实</h2>
          <p className="muted">设备条件、擅长技术、当前目标会影响实验可行性排序和输出形式；所有画像均可由用户查看和修改。</p>
        </div>
      </section>

      {error && <div className="error-box">{error}</div>}
      {message && <div className="success-box">{message}</div>}
      <section className="profile-grid">
        <label>学校或机构<input value={profile.institution} onChange={(e) => field('institution', e.target.value)} /></label>
        <label>角色/研究阶段<input value={profile.role} onChange={(e) => field('role', e.target.value)} placeholder="硕士生、博士生、实验负责人…" /></label>
        <label className="wide">研究兴趣<textarea value={join(profile.researchInterests)} onChange={(e) => listField('researchInterests', e.target.value)} placeholder="分子筛、甲烷转化、塑料升级回收…" /></label>
        <label className="wide">熟悉的催化体系<textarea value={join(profile.catalystSystems)} onChange={(e) => listField('catalystSystems', e.target.value)} /></label>
        <label className="wide">现有表征和实验技术<textarea value={join(profile.techniques)} onChange={(e) => listField('techniques', e.target.value)} placeholder="XRD、BET、GC-MS、原位红外…" /></label>
        <label className="wide">当前研究目标<textarea value={join(profile.currentGoals)} onChange={(e) => listField('currentGoals', e.target.value)} /></label>
        <label>建议表达方式
          <select value={profile.preferredOutputStyle} onChange={(e) => field('preferredOutputStyle', e.target.value)}>
            <option value="evidence_first">证据优先</option>
            <option value="experiment_first">实验优先</option>
            <option value="mechanism_first">机理优先</option>
            <option value="concise">精炼汇报</option>
          </select>
        </label>
        <label className="wide">实验约束（JSON）<textarea className="code-area" value={constraints} onChange={(e) => setConstraints(e.target.value)} placeholder={'{"maxTemperature":"500 °C","availableReactors":["fixed-bed"]}'} /></label>
        <label className="wide">补充说明<textarea value={profile.notes} onChange={(e) => field('notes', e.target.value)} /></label>
      </section>
    </main>
  );
}

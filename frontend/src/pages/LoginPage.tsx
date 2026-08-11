import { FormEvent, useState } from 'react';
import { ArrowLeft, ArrowRight, Atom, Eye, EyeOff } from 'lucide-react';
import { Navigate, useNavigate } from 'react-router-dom';
import { RegistrationProfile } from '../api';
import { useAuth } from '../state/auth';

const split = (value: string) =>
  value.split(/[,，;\n]/).map((item) => item.trim()).filter(Boolean);

const initialProfile: RegistrationProfile = {
  role: '',
  primaryCatalysis: 'undecided',
  molecularSievePreference: 'when_helpful',
  heterojunctionPreference: 'evidence_based',
  researchPriorities: [],
  availableResources: [],
  avoidances: [],
  preferredOutputStyle: 'evidence_first',
  openResearchContext: ''
};

const inputClass = 'h-11 w-full border-0 border-b border-[#d9dde2] bg-transparent px-0 text-sm outline-none focus:border-[#202124]';

export default function LoginPage() {
  const { user, login, register } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [registerStep, setRegisterStep] = useState<1 | 2>(1);
  const [identifier, setIdentifier] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [profile, setProfile] = useState<RegistrationProfile>(initialProfile);
  const [resources, setResources] = useState('');
  const [avoidances, setAvoidances] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  if (user) return <Navigate to={mode === 'register' ? '/profile/interview' : '/workspaces'} replace />;

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setError('');
    if (mode === 'register' && registerStep === 1) {
      setRegisterStep(2);
      return;
    }
    if (mode === 'register' && profile.primaryCatalysis === 'undecided') {
      setError('请选择当前主要研究的催化方向。');
      return;
    }
    setBusy(true);
    try {
      if (mode === 'login') {
        await login(identifier.trim(), password);
        navigate('/workspaces');
      } else {
        await register(username.trim(), email.trim(), password, {
          ...profile,
          availableResources: split(resources),
          avoidances: split(avoidances)
        });
        navigate('/profile/interview');
      }
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : '操作失败');
    } finally {
      setBusy(false);
    }
  };

  const switchMode = () => {
    setMode(mode === 'login' ? 'register' : 'login');
    setRegisterStep(1);
    setError('');
  };

  return (
    <main className="relative min-h-[100dvh] bg-white text-[#202124]">
      <div className="absolute left-6 top-5 flex items-center gap-2 text-sm font-semibold">
        <span className="grid h-8 w-8 place-items-center rounded-full border border-[#d8dce1]"><Atom className="h-4 w-4" /></span>
        Synapse Link
      </div>

      <div className="mx-auto flex min-h-[100dvh] w-full max-w-2xl items-center justify-center px-6 py-20">
        <section className={`w-full ${mode === 'register' && registerStep === 2 ? 'max-w-xl' : 'max-w-md'}`}>
          <div className="text-center">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-[#858d97]">
              {mode === 'login' ? 'Catalysis Research Platform' : `Create account · ${registerStep}/2`}
            </p>
            <h1 className="mt-3 text-2xl font-medium">
              {mode === 'login' ? '登录到 Synapse Link' : registerStep === 1 ? '注册到 Synapse Link' : '建立初始研究画像'}
            </h1>
            <p className="mt-2 text-sm leading-6 text-[#858d97]">
              {mode === 'register' && registerStep === 2
                ? '先回答几个基础问题，注册后系统还会继续进行逐题画像访谈。'
                : '光催化与热催化论文证据、实验记录和用户画像按账号隔离。'}
            </p>
          </div>

          <form onSubmit={submit} className="mt-8 space-y-5">
            {mode === 'login' && (
              <label className="block text-sm font-medium">
                邮箱或用户名
                <input className={inputClass} value={identifier} onChange={(event) => setIdentifier(event.target.value)} required />
              </label>
            )}

            {mode === 'register' && registerStep === 1 && (
              <>
                <label className="block text-sm font-medium">用户名<input className={inputClass} value={username} onChange={(event) => setUsername(event.target.value)} minLength={3} required /></label>
                <label className="block text-sm font-medium">邮箱<input className={inputClass} type="email" value={email} onChange={(event) => setEmail(event.target.value)} required /></label>
              </>
            )}

            {(mode === 'login' || registerStep === 1) && (
              <label className="block text-sm font-medium">
                密码
                <span className="relative block">
                  <input
                    className={`${inputClass} pr-10`}
                    type={passwordVisible ? 'text' : 'password'}
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    minLength={8}
                    required
                  />
                  <button type="button" title={passwordVisible ? '隐藏密码' : '显示密码'} onClick={() => setPasswordVisible((value) => !value)} className="absolute right-0 top-3 text-[#8b929b]">
                    {passwordVisible ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </span>
              </label>
            )}

            {mode === 'register' && registerStep === 2 && (
              <div className="grid gap-5 sm:grid-cols-2">
                <label className="block text-sm font-medium">当前主要研究方向
                  <select className={inputClass} value={profile.primaryCatalysis} onChange={(event) => setProfile({ ...profile, primaryCatalysis: event.target.value as RegistrationProfile['primaryCatalysis'] })}>
                    <option value="undecided">请选择</option>
                    <option value="photocatalysis">以光催化为主</option>
                    <option value="thermal_catalysis">以热催化为主</option>
                    <option value="both">两者都做</option>
                  </select>
                </label>
                <label className="block text-sm font-medium">角色或研究阶段<input className={inputClass} value={profile.role} onChange={(event) => setProfile({ ...profile, role: event.target.value })} placeholder="硕士生、博士生、实验负责人" /></label>
                <label className="block text-sm font-medium">分子筛在方案中的位置
                  <select className={inputClass} value={profile.molecularSievePreference} onChange={(event) => setProfile({ ...profile, molecularSievePreference: event.target.value as RegistrationProfile['molecularSievePreference'] })}>
                    <option value="central">优先作为核心设计</option>
                    <option value="when_helpful">有明确作用时使用</option>
                    <option value="minimal">尽量减少依赖</option>
                  </select>
                </label>
                <label className="block text-sm font-medium">对异质结方案的态度
                  <select className={inputClass} value={profile.heterojunctionPreference} onChange={(event) => setProfile({ ...profile, heterojunctionPreference: event.target.value as RegistrationProfile['heterojunctionPreference'] })}>
                    <option value="evidence_based">有证据支持时采用</option>
                    <option value="prefer">愿意优先探索</option>
                    <option value="avoid_overuse">避免过度堆叠</option>
                  </select>
                </label>
                <label className="block text-sm font-medium sm:col-span-2">现有设备、技术或合作资源
                  <textarea className="mt-2 min-h-24 w-full resize-y rounded-lg border border-[#d9dde2] p-3 text-sm outline-none focus:border-[#747c86]" value={resources} onChange={(event) => setResources(event.target.value)} />
                </label>
                <label className="block text-sm font-medium sm:col-span-2">明确不希望出现的建议
                  <textarea className="mt-2 min-h-24 w-full resize-y rounded-lg border border-[#d9dde2] p-3 text-sm outline-none focus:border-[#747c86]" value={avoidances} onChange={(event) => setAvoidances(event.target.value)} />
                </label>
              </div>
            )}

            {error && <div className="rounded-lg border border-[#ffd4d4] bg-[#fff7f7] px-3 py-2 text-sm text-[#b42318]">{error}</div>}

            <div className="flex gap-2">
              {mode === 'register' && registerStep === 2 && (
                <button type="button" onClick={() => setRegisterStep(1)} className="inline-flex h-11 items-center gap-2 rounded-full border border-[#d9dde2] px-5 text-sm font-medium">
                  <ArrowLeft className="h-4 w-4" />返回
                </button>
              )}
              <button disabled={busy} className="inline-flex h-11 flex-1 items-center justify-center gap-2 rounded-full bg-[#202124] px-5 text-sm font-medium text-white disabled:opacity-60">
                {busy ? '请稍候…' : mode === 'login' ? '登录' : registerStep === 1 ? <>继续<ArrowRight className="h-4 w-4" /></> : '创建账号并继续访谈'}
              </button>
            </div>
          </form>

          <button onClick={switchMode} className="mt-5 w-full text-center text-sm text-[#4d5661] underline underline-offset-4">
            {mode === 'login' ? '还没有账号？立即注册' : '已有账号？去登录'}
          </button>
        </section>
      </div>
    </main>
  );
}

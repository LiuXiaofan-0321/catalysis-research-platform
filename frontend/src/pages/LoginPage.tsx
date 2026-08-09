import { FormEvent, useState } from 'react';
import { Atom, FlaskConical } from 'lucide-react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../state/auth';

export default function LoginPage() {
  const { user, login, register } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [identifier, setIdentifier] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  if (user) return <Navigate to="/workspaces" replace />;

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError('');
    try {
      if (mode === 'login') await login(identifier.trim(), password);
      else await register(username.trim(), email.trim(), password);
      navigate('/workspaces');
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : '登录失败');
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="login-shell">
      <section className="login-brand">
        <div className="brand-mark"><Atom size={30} /></div>
        <p className="eyebrow">CATALYSIS RESEARCH INTELLIGENCE</p>
        <h1>让论文证据真正进入实验决策</h1>
        <p className="lead">
          面向光催化与分子筛热催化的证据知识图谱、多智能体方向分析、最小验证实验和结果回流平台。
        </p>
        <div className="brand-features">
          <span><FlaskConical size={17} /> 证据约束的研究假设</span>
          <span><FlaskConical size={17} /> 实验结果驱动的建议演化</span>
          <span><FlaskConical size={17} /> 可控制的研究者画像</span>
        </div>
      </section>
      <section className="login-panel">
        <div className="login-card">
          <p className="eyebrow">{mode === 'login' ? 'WELCOME BACK' : 'CREATE ACCOUNT'}</p>
          <h2>{mode === 'login' ? '登录科研平台' : '注册科研账户'}</h2>
          <p className="muted">所有图谱、实验和画像按账户隔离。</p>
          <form onSubmit={submit} className="form-stack">
            {mode === 'register' && (
              <>
                <label>用户名<input value={username} onChange={(e) => setUsername(e.target.value)} required /></label>
                <label>邮箱<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /></label>
              </>
            )}
            {mode === 'login' && (
              <label>用户名或邮箱<input value={identifier} onChange={(e) => setIdentifier(e.target.value)} required /></label>
            )}
            <label>密码<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} minLength={8} required /></label>
            {error && <div className="error-box">{error}</div>}
            <button className="primary-button" disabled={busy}>
              {busy ? '处理中…' : mode === 'login' ? '登录' : '注册'}
            </button>
          </form>
          <button className="text-button" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
            {mode === 'login' ? '没有账号？创建一个' : '已有账号？返回登录'}
          </button>
        </div>
      </section>
    </main>
  );
}

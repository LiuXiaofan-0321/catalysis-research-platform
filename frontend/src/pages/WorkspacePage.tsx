import { useEffect, useState } from 'react';
import { ArrowRight, Flame, LogOut, Settings2, SunMedium } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api, Workspace } from '../api';
import { useAuth } from '../state/auth';

export default function WorkspacePage() {
  const { user, logout } = useAuth();
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [stats, setStats] = useState<Record<string, any>>({});
  const [error, setError] = useState('');

  useEffect(() => {
    api.workspaces()
      .then(async ({ workspaces: values }) => {
        setWorkspaces(values);
        const pairs = await Promise.all(values.map(async (workspace) => {
          const value = await api.stats(workspace.id).catch(() => null);
          return [workspace.id, value] as const;
        }));
        setStats(Object.fromEntries(pairs));
      })
      .catch((loadError) => setError(loadError instanceof Error ? loadError.message : '加载失败'));
  }, []);

  return (
    <main className="app-page">
      <header className="topbar">
        <div>
          <p className="eyebrow">CATALYSIS RESEARCH PLATFORM</p>
          <h1>催化科研工作空间</h1>
        </div>
        <div className="topbar-actions">
          <span className="user-chip">{user?.displayName || user?.username}</span>
          <Link to="/profile" className="icon-button" title="研究者画像"><Settings2 size={18} /></Link>
          <button className="icon-button" title="退出登录" onClick={() => void logout()}><LogOut size={18} /></button>
        </div>
      </header>

      <section className="hero-card">
        <div>
          <p className="eyebrow">EVIDENCE → HYPOTHESIS → EXPERIMENT → FEEDBACK</p>
          <h2>从论文证据出发，形成可证伪的下一步研究方向</h2>
          <p className="muted">光催化与热催化语料相互隔离，论文事实、AI 推断和用户实验分别记录。</p>
        </div>
        <div className="hero-metric">
          <strong>{workspaces.reduce((sum, workspace) => sum + Number(stats[workspace.id]?.documents || 0), 0)}</strong>
          <span>篇结构化论文</span>
        </div>
      </section>

      {error && <div className="error-box">{error}</div>}
      <section className="workspace-grid">
        {workspaces.map((workspace) => {
          const photo = workspace.catalysisSystem === 'photocatalysis';
          const Icon = photo ? SunMedium : Flame;
          const data = stats[workspace.id];
          return (
            <Link key={workspace.id} className={`workspace-card ${photo ? 'photo' : 'thermal'}`} to={`/workspaces/${workspace.id}/research-lab`}>
              <div className="workspace-icon"><Icon size={25} /></div>
              <div className="workspace-heading">
                <div>
                  <p className="eyebrow">{photo ? 'PHOTOCATALYSIS' : 'THERMAL CATALYSIS'}</p>
                  <h3>{workspace.name}</h3>
                </div>
                <ArrowRight size={20} />
              </div>
              <p className="muted">{workspace.description}</p>
              <div className="workspace-stats">
                <span><strong>{data?.documents || 0}</strong>论文</span>
                <span><strong>{data?.nodeCount || 0}</strong>节点</span>
                <span><strong>{data?.edgeCount || 0}</strong>证据边</span>
              </div>
            </Link>
          );
        })}
      </section>
    </main>
  );
}

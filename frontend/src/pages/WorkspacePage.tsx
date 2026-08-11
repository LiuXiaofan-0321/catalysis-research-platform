import { useEffect, useState } from 'react';
import {
  Atom, BookOpen, ChevronRight, FlaskConical, LogOut, MessageCircleQuestion,
  Search, Settings2, SunMedium, ThermometerSun
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { api, Workspace } from '../api';
import { useAuth } from '../state/auth';

export default function WorkspacePage() {
  const { user, logout } = useAuth();
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [stats, setStats] = useState<Record<string, any>>({});
  const [search, setSearch] = useState('');
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
      .catch((loadError) => setError(loadError instanceof Error ? loadError.message : '平台加载失败'));
  }, []);

  const visible = workspaces.filter((workspace) =>
    `${workspace.name} ${workspace.description || ''}`.toLowerCase().includes(search.trim().toLowerCase())
  );

  return (
    <main className="flex h-[100dvh] min-h-0 overflow-hidden bg-white text-[#202124]">
      <aside className="hidden w-[292px] shrink-0 flex-col border-r border-[#f0f0f1] bg-[#f9f9fb] md:flex">
        <div className="flex h-12 items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <span className="grid h-7 w-7 place-items-center rounded-full border border-[#d8dbe0] bg-white text-[10px] font-semibold">SL</span>
            <strong className="text-sm">Synapse Link</strong>
          </div>
          <Atom className="h-4 w-4 text-[#65707c]" />
        </div>

        <nav className="px-2 pt-2 text-sm">
          <Link to="/workspaces" className="flex h-10 items-center gap-3 rounded-lg bg-[#ececef] px-3 font-medium">
            <FlaskConical className="h-4 w-4" />科研平台
          </Link>
          <Link to="/profile" className="mt-1 flex h-10 items-center gap-3 rounded-lg px-3 hover:bg-[#eeeeef]">
            <Settings2 className="h-4 w-4" />研究者画像
          </Link>
          <Link to="/profile/interview" className="mt-1 flex h-10 items-center gap-3 rounded-lg px-3 hover:bg-[#eeeeef]">
            <MessageCircleQuestion className="h-4 w-4" />画像访谈
          </Link>
        </nav>

        <div className="px-4 pb-2 pt-5 text-xs font-medium text-[#66707c]">Research Workspaces</div>
        <div className="px-2">
          {workspaces.map((workspace) => {
            const thermal = workspace.catalysisSystem === 'thermal_catalysis';
            const Icon = thermal ? ThermometerSun : SunMedium;
            return (
              <Link
                key={workspace.id}
                to={`/workspaces/${workspace.id}/research-lab`}
                className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm hover:bg-[#ececef]"
              >
                <Icon className={`h-4 w-4 ${thermal ? 'text-[#b45309]' : 'text-[#147d64]'}`} />
                <span className="min-w-0 flex-1 truncate">{thermal ? '热催化平台' : '光催化平台'}</span>
                <span className="text-[10px] text-[#98a0aa]">{stats[workspace.id]?.documents || 0}</span>
              </Link>
            );
          })}
        </div>

        <div className="mt-auto border-t border-[#ececef] p-3">
          <div className="flex items-center gap-3 rounded-lg px-2 py-2">
            <span className="grid h-8 w-8 place-items-center rounded-full bg-[#111827] text-xs font-medium text-white">
              {(user?.displayName || user?.username || 'U').slice(0, 1).toUpperCase()}
            </span>
            <span className="min-w-0 flex-1 truncate text-sm">{user?.displayName || user?.username}</span>
            <button title="退出登录" onClick={() => void logout()} className="grid h-8 w-8 place-items-center rounded-lg hover:bg-[#ececef]">
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
      </aside>

      <section className="min-w-0 flex-1 overflow-y-auto">
        <header className="sticky top-0 z-10 flex h-12 items-center justify-between border-b border-[#f0f1f2] bg-white/95 px-5 backdrop-blur">
          <nav className="flex items-center gap-7 text-sm">
            <span className="font-semibold text-[#202124]">Research Platforms</span>
            <Link to="/profile" className="text-[#a1a8b1] hover:text-[#202124]">Profile</Link>
            <Link to="/profile/interview" className="text-[#a1a8b1] hover:text-[#202124]">Interview</Link>
          </nav>
          <div className="relative hidden sm:block">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-[#939aa4]" />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search"
              className="h-9 w-56 rounded-lg border border-[#e2e5e9] bg-white pl-9 pr-3 text-sm outline-none focus:border-[#8c949e]"
            />
          </div>
        </header>

        <div className="mx-auto max-w-6xl px-6 py-8">
          <div className="flex items-end justify-between gap-5">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">Catalysis Research Platforms <span className="font-normal text-[#7a828c]">{visible.length}</span></h1>
              <p className="mt-2 text-sm text-[#7a828c]">保留原项目的科研证据图谱、方向生成与实验反馈闭环。</p>
            </div>
            <Link to="/profile/interview" className="hidden h-9 items-center gap-2 rounded-full bg-black px-4 text-sm font-medium text-white sm:inline-flex">
              <MessageCircleQuestion className="h-4 w-4" />完善画像
            </Link>
          </div>

          {error && <div className="mt-5 rounded-lg border border-[#ffd6d6] bg-[#fff7f7] px-4 py-3 text-sm text-[#b42318]">{error}</div>}

          <div className="mt-8 border-t border-[#eceef0]">
            <div className="grid grid-cols-[minmax(0,1fr)_110px_110px_36px] gap-4 border-b border-[#eceef0] px-2 py-3 text-xs text-[#7a828c]">
              <span>Platform</span><span>Papers</span><span>Graph</span><span />
            </div>
            {visible.map((workspace) => {
              const thermal = workspace.catalysisSystem === 'thermal_catalysis';
              const Icon = thermal ? ThermometerSun : SunMedium;
              const data = stats[workspace.id];
              return (
                <Link
                  key={workspace.id}
                  to={`/workspaces/${workspace.id}/research-lab`}
                  className="grid min-h-24 grid-cols-[minmax(0,1fr)_110px_110px_36px] items-center gap-4 border-b border-[#eceef0] px-2 py-4 hover:bg-[#fafafa]"
                >
                  <div className="flex min-w-0 items-center gap-4">
                    <span className={`grid h-11 w-11 shrink-0 place-items-center rounded-lg ${thermal ? 'bg-[#fff4e8] text-[#b45309]' : 'bg-[#eaf6f2] text-[#147d64]'}`}>
                      <Icon className="h-5 w-5" />
                    </span>
                    <div className="min-w-0">
                      <strong className="block truncate text-sm">{workspace.name}</strong>
                      <p className="mt-1 line-clamp-1 text-xs text-[#7a828c]">{workspace.description}</p>
                    </div>
                  </div>
                  <div className="text-sm">
                    <strong>{data?.documents || 0}</strong>
                    <span className="mt-1 block text-[10px] text-[#8f97a1]">structured</span>
                  </div>
                  <div className="text-sm">
                    <strong>{data?.nodeCount || 0}</strong>
                    <span className="mt-1 block text-[10px] text-[#8f97a1]">{data?.edgeCount || 0} edges</span>
                  </div>
                  <ChevronRight className="h-4 w-4 text-[#9ba2ab]" />
                </Link>
              );
            })}
          </div>

          <div className="mt-8 flex items-center gap-2 text-xs text-[#8b929b]">
            <BookOpen className="h-4 w-4" />
            当前语料共 {Object.values(stats).reduce((sum, item) => sum + Number(item?.documents || 0), 0)} 篇论文，论文事实与用户实验分开记录。
          </div>
        </div>
      </section>
    </main>
  );
}

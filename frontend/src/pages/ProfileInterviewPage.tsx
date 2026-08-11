import { useEffect, useMemo, useState } from 'react';
import {
  ArrowLeft, ArrowRight, Check, CheckCircle2, Circle, LoaderCircle, MessageCircleQuestion
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { api, ProfileQuestion } from '../api';

const listText = (value: string | string[]) => Array.isArray(value) ? value.join('，') : value;

export default function ProfileInterviewPage() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<ProfileQuestion[]>([]);
  const [index, setIndex] = useState(0);
  const [draft, setDraft] = useState<string | string[]>('');
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.profileQuestions()
      .then(({ questions: values }) => {
        setQuestions(values);
        const firstUnanswered = values.findIndex((question) => !question.answered);
        const initialIndex = firstUnanswered >= 0 ? firstUnanswered : 0;
        setIndex(initialIndex);
        setDraft(values[initialIndex]?.answer || '');
      })
      .catch((loadError) => setError(loadError instanceof Error ? loadError.message : '画像访谈加载失败'))
      .finally(() => setBusy(false));
  }, []);

  const question = questions[index];
  const answeredCount = useMemo(() => questions.filter((item) => item.answered).length, [questions]);
  const selected = Array.isArray(draft) ? draft : [];
  const canContinue = Array.isArray(draft) ? draft.length > 0 : Boolean(draft.trim());

  const move = (nextIndex: number) => {
    const bounded = Math.max(0, Math.min(questions.length - 1, nextIndex));
    setIndex(bounded);
    setDraft(questions[bounded]?.answer || '');
    setError('');
  };

  const saveAndContinue = async () => {
    if (!question || !canContinue) return;
    setBusy(true);
    setError('');
    try {
      await api.answerProfileQuestion(question.id, draft);
      const updated = questions.map((item, itemIndex) =>
        itemIndex === index ? { ...item, answer: draft, answered: true } : item
      );
      setQuestions(updated);
      if (index < questions.length - 1) {
        setIndex(index + 1);
        setDraft(updated[index + 1].answer || '');
      } else {
        await api.completeProfileInterview();
        navigate('/workspaces');
      }
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : '回答保存失败');
    } finally {
      setBusy(false);
    }
  };

  const finish = async () => {
    setBusy(true);
    setError('');
    try {
      await api.completeProfileInterview();
      navigate('/workspaces');
    } catch (finishError) {
      setError(finishError instanceof Error ? finishError.message : '访谈完成状态保存失败');
    } finally {
      setBusy(false);
    }
  };

  if (busy && !questions.length) {
    return (
      <div className="grid min-h-[100dvh] place-items-center bg-white text-sm text-[#69717b]">
        <LoaderCircle className="mr-2 inline h-4 w-4 animate-spin" />正在准备画像问题…
      </div>
    );
  }

  return (
    <main className="min-h-[100dvh] bg-white text-[#202124]">
      <header className="flex min-h-14 items-center justify-between border-b border-[#eceef0] px-4 sm:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <Link to="/profile" className="grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-[#e0e3e7] hover:bg-[#f6f6f7]" title="返回研究者画像">
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div className="min-w-0">
            <p className="text-[10px] font-medium uppercase text-[#8a929c]">Researcher Interview</p>
            <h1 className="truncate text-sm font-semibold sm:text-base">研究方式与实验边界访谈</h1>
          </div>
        </div>
        <button className="h-9 rounded-lg px-3 text-sm text-[#606873] hover:bg-[#f4f4f5] disabled:opacity-50" onClick={() => void finish()} disabled={busy}>
          稍后继续
        </button>
      </header>

      <div className="h-1 bg-[#f0f1f2]" aria-label="画像访谈进度">
        <div className="h-full bg-[#202124] transition-[width]" style={{ width: `${questions.length ? (answeredCount / questions.length) * 100 : 0}%` }} />
      </div>

      <div className="mx-auto grid min-h-[calc(100dvh-60px)] max-w-6xl md:grid-cols-[290px_minmax(0,1fr)]">
        <aside className="border-b border-[#eceef0] bg-[#fafafb] p-4 md:border-b-0 md:border-r md:p-5">
          <div className="flex items-center gap-3">
            <span className="grid h-9 w-9 place-items-center rounded-lg border border-[#e0e3e7] bg-white">
              <MessageCircleQuestion className="h-4 w-4" />
            </span>
            <div>
              <strong className="block text-sm">{answeredCount} / {questions.length} 已回答</strong>
              <span className="text-xs text-[#858d97]">答案会直接写入研究者画像</span>
            </div>
          </div>

          <nav className="mt-5 grid max-h-52 grid-cols-2 gap-1 overflow-y-auto md:max-h-[calc(100dvh-170px)] md:grid-cols-1" aria-label="访谈问题">
            {questions.map((item, itemIndex) => (
              <button
                key={item.id}
                type="button"
                onClick={() => move(itemIndex)}
                className={`flex min-h-11 items-center gap-3 rounded-lg px-3 py-2 text-left text-xs transition ${
                  itemIndex === index ? 'bg-[#e9e9eb] text-[#202124]' : 'text-[#68717b] hover:bg-[#f0f0f1]'
                }`}
              >
                {item.answered
                  ? <CheckCircle2 className="h-4 w-4 shrink-0 text-[#147d64]" />
                  : <Circle className="h-4 w-4 shrink-0 text-[#a4abb4]" />}
                <span className="min-w-0">
                  <span className="block text-[10px] text-[#959ca5]">{String(itemIndex + 1).padStart(2, '0')}</span>
                  <strong className="block truncate font-medium">{item.title}</strong>
                </span>
              </button>
            ))}
          </nav>
        </aside>

        {question && (
          <section className="flex min-w-0 items-start justify-center px-5 py-8 sm:px-10 sm:py-12">
            <article className="w-full max-w-2xl">
              <div className="flex items-center justify-between gap-4 border-b border-[#eceef0] pb-4">
                <p className="text-xs font-medium text-[#747c86]">问题 {String(index + 1).padStart(2, '0')} / {String(questions.length).padStart(2, '0')}</p>
                <span className="rounded bg-[#f0f1f2] px-2 py-1 text-[10px] text-[#69717b]">
                  {question.type === 'multiple' ? '可多选' : question.type === 'single' ? '单选' : '开放回答'}
                </span>
              </div>

              <p className="mt-7 text-xs font-medium text-[#147d64]">{question.title}</p>
              <h2 className="mt-2 text-xl font-semibold leading-8 sm:text-2xl">{question.prompt}</h2>
              {question.hint && <p className="mt-3 text-sm leading-6 text-[#7b838d]">{question.hint}</p>}

              {question.type === 'text' && (
                <textarea
                  autoFocus
                  rows={7}
                  value={listText(draft)}
                  onChange={(event) => setDraft(event.target.value)}
                  placeholder="请用自然语言回答；多个项目可用逗号或换行分隔。"
                  className="mt-7 w-full resize-y rounded-lg border border-[#d9dde2] bg-white p-4 text-sm leading-6 outline-none focus:border-[#747c86] focus:shadow-none"
                />
              )}

              {question.type === 'single' && (
                <div className="mt-7 grid gap-2">
                  {question.options?.map((option) => {
                    const active = draft === option.value;
                    return (
                      <button
                        type="button"
                        key={option.value}
                        className={`flex min-h-16 items-center gap-3 rounded-lg border px-4 py-3 text-left ${
                          active ? 'border-[#202124] bg-[#f5f5f6]' : 'border-[#e0e3e7] bg-white hover:bg-[#fafafa]'
                        }`}
                        onClick={() => setDraft(option.value)}
                      >
                        {active ? <CheckCircle2 className="h-5 w-5 shrink-0" /> : <Circle className="h-5 w-5 shrink-0 text-[#a7adb5]" />}
                        <span>
                          <strong className="block text-sm">{option.label}</strong>
                          {option.description && <small className="mt-1 block text-xs leading-5 text-[#7c848e]">{option.description}</small>}
                        </span>
                      </button>
                    );
                  })}
                </div>
              )}

              {question.type === 'multiple' && (
                <div className="mt-7 grid gap-2 sm:grid-cols-2">
                  {question.options?.map((option) => {
                    const active = selected.includes(option.value);
                    return (
                      <button
                        type="button"
                        key={option.value}
                        className={`flex min-h-12 items-center gap-3 rounded-lg border px-4 py-3 text-left ${
                          active ? 'border-[#202124] bg-[#f5f5f6]' : 'border-[#e0e3e7] bg-white hover:bg-[#fafafa]'
                        }`}
                        onClick={() => setDraft(
                          active ? selected.filter((value) => value !== option.value) : [...selected, option.value]
                        )}
                      >
                        <span className={`grid h-5 w-5 shrink-0 place-items-center rounded border ${active ? 'border-[#202124] bg-[#202124] text-white' : 'border-[#aeb4bc]'}`}>
                          {active && <Check className="h-3.5 w-3.5" />}
                        </span>
                        <strong className="text-sm font-medium">{option.label}</strong>
                      </button>
                    );
                  })}
                </div>
              )}

              {error && <div className="mt-5 rounded-lg border border-[#ffd4d4] bg-[#fff7f7] px-3 py-2 text-sm text-[#b42318]">{error}</div>}
              <div className="mt-8 flex items-center justify-between border-t border-[#eceef0] pt-5">
                <button
                  type="button"
                  className="inline-flex h-10 items-center gap-2 rounded-lg border border-[#dfe2e6] px-4 text-sm hover:bg-[#f6f6f7] disabled:cursor-not-allowed disabled:opacity-40"
                  disabled={index === 0 || busy}
                  onClick={() => move(index - 1)}
                >
                  <ArrowLeft className="h-4 w-4" />上一题
                </button>
                <button
                  type="button"
                  className="inline-flex h-10 items-center gap-2 rounded-lg bg-[#202124] px-4 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
                  disabled={!canContinue || busy}
                  onClick={() => void saveAndContinue()}
                >
                  {busy ? <LoaderCircle className="h-4 w-4 animate-spin" /> : index === questions.length - 1 ? <Check className="h-4 w-4" /> : <ArrowRight className="h-4 w-4" />}
                  {index === questions.length - 1 ? '完成访谈' : '保存并继续'}
                </button>
              </div>
            </article>
          </section>
        )}
      </div>
    </main>
  );
}

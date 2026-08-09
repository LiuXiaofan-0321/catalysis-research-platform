import { env } from '../config/env';

type JsonCall = {
  system: string;
  input: Record<string, unknown>;
  schema: Record<string, unknown>;
  maxTokens?: number;
};

const parseJsonObject = <T>(value: string): T => {
  const cleaned = value.trim()
    .replace(/^```(?:json)?\s*/i, '')
    .replace(/\s*```$/, '');
  const first = cleaned.indexOf('{');
  const last = cleaned.lastIndexOf('}');
  if (first < 0 || last <= first) throw new Error('DeepSeek 未返回 JSON 对象');
  return JSON.parse(cleaned.slice(first, last + 1)) as T;
};

export const deepseekClient = {
  isConfigured: () => Boolean(env.deepseekApiKey),

  async json<T>({ system, input, schema, maxTokens }: JsonCall) {
    if (!env.deepseekApiKey) throw new Error('DEEPSEEK_API_KEY 未配置');
    let lastError: unknown;
    for (let attempt = 1; attempt <= 2; attempt += 1) {
      try {
        const response = await fetch(`${env.deepseekBaseUrl}/chat/completions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${env.deepseekApiKey}`
          },
          signal: AbortSignal.timeout(env.researchTimeoutMs),
          body: JSON.stringify({
            model: env.researchModel,
            messages: [
              { role: 'system', content: system },
              {
                role: 'user',
                content: JSON.stringify({ schema, input })
              }
            ],
            response_format: { type: 'json_object' },
            temperature: 0.25,
            max_tokens: maxTokens || env.researchMaxTokens,
            stream: false
          })
        });
        const body = await response.json().catch(() => null) as any;
        if (!response.ok) {
          throw new Error(body?.error?.message || `DeepSeek HTTP ${response.status}`);
        }
        const content = body?.choices?.[0]?.message?.content;
        if (!content) throw new Error('DeepSeek 返回内容为空');
        return {
          data: parseJsonObject<T>(content),
          model: env.researchModel,
          provider: 'deepseek',
          usage: body?.usage || null
        };
      } catch (error) {
        lastError = error;
        if (attempt < 2) await new Promise((resolve) => setTimeout(resolve, 600));
      }
    }
    throw lastError;
  }
};

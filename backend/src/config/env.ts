import path from 'path';
import dotenv from 'dotenv';

dotenv.config({ path: path.resolve(process.cwd(), '../.env'), quiet: true });
dotenv.config({ path: path.resolve(process.cwd(), '.env'), override: true, quiet: true });

export const env = {
  port: Number(process.env.PORT || 3001),
  frontendOrigin: process.env.FRONTEND_ORIGIN || 'http://localhost:5173',
  sessionSecret: process.env.SESSION_SECRET?.trim() || '',
  cookieSecure: String(process.env.COOKIE_SECURE || 'false').toLowerCase() === 'true',
  deepseekApiKey: process.env.DEEPSEEK_API_KEY?.trim() || '',
  deepseekBaseUrl: (process.env.DEEPSEEK_BASE_URL || 'https://api.deepseek.com').replace(/\/+$/, ''),
  researchModel: process.env.AI_RESEARCH_MODEL || 'deepseek-v4-flash',
  researchTimeoutMs: Number(process.env.AI_RESEARCH_TIMEOUT_MS || 300000),
  researchMaxTokens: Number(process.env.AI_RESEARCH_MAX_TOKENS || 32768)
};

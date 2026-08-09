import './config/env';
import cookieParser from 'cookie-parser';
import cors from 'cors';
import express from 'express';
import { env } from './config/env';
import { configureDatabase } from './config/db';
import { ensureResearchSchema } from './config/ensureResearchSchema';
import authRoutes from './routes/auth';
import profileRoutes from './routes/profile';
import researchRoutes from './routes/research';
import workspaceRoutes from './routes/workspaces';

const main = async () => {
  if (env.sessionSecret.length < 24 || env.sessionSecret.startsWith('replace-with-')) {
    throw new Error('SESSION_SECRET 必须设置为至少24位的随机字符串');
  }
  await configureDatabase();
  await ensureResearchSchema();

  const app = express();
  app.use(cors({ origin: env.frontendOrigin, credentials: true }));
  app.use(express.json({ limit: '12mb' }));
  app.use(cookieParser());

  app.get('/api/health', (_req, res) => {
    res.json({ ok: true, model: env.researchModel, aiConfigured: Boolean(env.deepseekApiKey) });
  });
  app.use('/api/auth', authRoutes);
  app.use('/api/workspaces', workspaceRoutes);
  app.use('/api/profile', profileRoutes);
  app.use('/api/research', researchRoutes);

  app.use((error: unknown, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
    console.error(error);
    res.status(500).json({ error: error instanceof Error ? error.message : '服务器内部错误' });
  });

  app.listen(env.port, '0.0.0.0', () => {
    console.log(`Catalysis research API listening on http://0.0.0.0:${env.port}`);
  });
};

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

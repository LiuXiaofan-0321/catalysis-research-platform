import { Router } from 'express';
import { env } from '../config/env';
import prisma from '../config/db';
import { requireAuth } from '../middleware/auth';
import { hashPassword, verifyPassword } from '../utils/hash';
import { sessionService } from '../services/sessionService';

const router = Router();
const cookieOptions = {
  httpOnly: true,
  sameSite: 'lax' as const,
  secure: env.cookieSecure,
  path: '/'
};

const publicUser = (user: { id: string; username: string; email: string; displayName: string | null }) => ({
  id: user.id,
  username: user.username,
  email: user.email,
  displayName: user.displayName
});

router.post('/register', async (req, res) => {
  const username = String(req.body?.username || '').trim();
  const email = String(req.body?.email || '').trim().toLowerCase();
  const password = String(req.body?.password || '');
  if (username.length < 3 || !email.includes('@') || password.length < 8) {
    return res.status(400).json({ error: '用户名至少3位，密码至少8位，并填写有效邮箱' });
  }
  const exists = await prisma.user.findFirst({ where: { OR: [{ username }, { email }] } });
  if (exists) return res.status(409).json({ error: '用户名或邮箱已存在' });
  const user = await prisma.user.create({
    data: { username, email, password: hashPassword(password), displayName: username }
  });
  await prisma.researcherProfile.create({ data: { userId: user.id } });
  const session = await sessionService.create(user.id);
  res.cookie(sessionService.cookieName, session.cookieValue, { ...cookieOptions, expires: session.expiresAt });
  return res.status(201).json({ user: publicUser(user) });
});

router.post('/login', async (req, res) => {
  const identifier = String(req.body?.identifier || '').trim();
  const password = String(req.body?.password || '');
  const user = await prisma.user.findFirst({
    where: { OR: [{ username: identifier }, { email: identifier.toLowerCase() }] }
  });
  if (!user || !verifyPassword(password, user.password)) {
    return res.status(401).json({ error: '账号或密码错误' });
  }
  const session = await sessionService.create(user.id);
  res.cookie(sessionService.cookieName, session.cookieValue, { ...cookieOptions, expires: session.expiresAt });
  return res.json({ user: publicUser(user) });
});

router.get('/me', requireAuth, async (req, res) => {
  const user = await prisma.user.findUniqueOrThrow({ where: { id: req.authUser!.id } });
  return res.json({ user: publicUser(user) });
});

router.post('/logout', async (req, res) => {
  await sessionService.destroy(req.cookies?.[sessionService.cookieName]);
  res.clearCookie(sessionService.cookieName, cookieOptions);
  return res.json({ success: true });
});

router.get('/health', (_req, res) => {
  res.json({
    ok: true,
    aiConfigured: Boolean(env.deepseekApiKey),
    model: env.researchModel
  });
});

export default router;

import crypto from 'crypto';
import prisma from '../config/db';
import { env } from '../config/env';
import { stableHash } from '../utils/hash';

const COOKIE_NAME = 'catalysis_session';
const SESSION_DAYS = 14;

const sign = (token: string) =>
  crypto.createHmac('sha256', env.sessionSecret).update(token).digest('base64url');

const decode = (cookieValue?: string) => {
  if (!cookieValue) return null;
  const [token, signature] = cookieValue.split('.');
  if (!token || !signature) return null;
  const expected = Buffer.from(sign(token));
  const received = Buffer.from(signature);
  if (expected.length !== received.length || !crypto.timingSafeEqual(expected, received)) return null;
  return token;
};

export const sessionService = {
  cookieName: COOKIE_NAME,

  async create(userId: string) {
    const token = crypto.randomBytes(32).toString('base64url');
    const expiresAt = new Date(Date.now() + SESSION_DAYS * 24 * 60 * 60 * 1000);
    await prisma.authToken.create({
      data: {
        id: crypto.randomUUID(),
        userId,
        type: 'session',
        tokenHash: stableHash(token),
        expiresAt
      }
    });
    return { cookieValue: `${token}.${sign(token)}`, expiresAt };
  },

  async resolve(cookieValue?: string) {
    const token = decode(cookieValue);
    if (!token) return null;
    return prisma.authToken.findFirst({
      where: {
        type: 'session',
        tokenHash: stableHash(token),
        consumedAt: null,
        expiresAt: { gt: new Date() }
      },
      include: { user: true }
    });
  },

  async destroy(cookieValue?: string) {
    const token = decode(cookieValue);
    if (!token) return;
    await prisma.authToken.updateMany({
      where: { type: 'session', tokenHash: stableHash(token), consumedAt: null },
      data: { consumedAt: new Date() }
    });
  }
};

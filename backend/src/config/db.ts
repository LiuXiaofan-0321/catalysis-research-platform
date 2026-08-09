import { PrismaClient } from '@prisma/client';

const configuredUrl = process.env.DATABASE_URL || 'file:./dev.db';
const prisma = new PrismaClient({
  datasources: { db: { url: configuredUrl } }
});

export const configureDatabase = async () => {
  if (!configuredUrl.startsWith('file:')) return;
  await prisma.$queryRawUnsafe('PRAGMA busy_timeout = 30000');
  await prisma.$queryRawUnsafe('PRAGMA journal_mode = WAL');
  await prisma.$queryRawUnsafe('PRAGMA synchronous = NORMAL');
  await prisma.$queryRawUnsafe('PRAGMA foreign_keys = ON');
};

export default prisma;

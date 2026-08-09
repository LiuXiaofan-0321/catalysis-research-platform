import { NextFunction, Request, Response } from 'express';
import prisma from '../config/db';
import { sessionService } from '../services/sessionService';

export const requireAuth = async (req: Request, res: Response, next: NextFunction) => {
  const session = await sessionService.resolve(req.cookies?.[sessionService.cookieName]);
  if (!session) return res.status(401).json({ error: '请先登录' });
  req.authUser = {
    id: session.user.id,
    username: session.user.username,
    email: session.user.email
  };
  next();
};

export const requireWorkspaceAccess = async (req: Request, res: Response, next: NextFunction) => {
  if (!req.authUser) return res.status(401).json({ error: '请先登录' });
  const workspaceId = String(req.params.workspaceId || req.params.id || '');
  const workspace = await prisma.workspace.findFirst({
    where: { id: workspaceId, userId: req.authUser.id }
  });
  if (!workspace) return res.status(404).json({ error: 'Workspace 不存在或无权访问' });
  next();
};

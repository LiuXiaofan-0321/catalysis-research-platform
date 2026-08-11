declare global {
  namespace Express {
    interface Request {
      authUser?: {
        id: string;
        username: string;
        email: string;
      };
      workspace?: {
        id: string;
        userId: string;
        name: string;
        catalysisSystem: string;
        corpusWorkspaceId: string | null;
      };
    }
  }
}

export {};

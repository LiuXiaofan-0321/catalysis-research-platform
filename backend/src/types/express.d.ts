declare global {
  namespace Express {
    interface Request {
      authUser?: {
        id: string;
        username: string;
        email: string;
      };
    }
  }
}

export {};

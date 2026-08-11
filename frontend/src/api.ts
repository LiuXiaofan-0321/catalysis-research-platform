const request = async <T>(path: string, init: RequestInit = {}): Promise<T> => {
  const response = await fetch(`/api${path}`, {
    ...init,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(init.headers || {})
    }
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data as T;
};

export type User = { id: string; username: string; email: string; displayName?: string | null };
export type Workspace = {
  id: string;
  name: string;
  description?: string | null;
  catalysisSystem: 'photocatalysis' | 'thermal_catalysis';
};

export type GraphNode = {
  id: string;
  type: string;
  label: string;
  sourceDocumentId?: string | null;
  data: Record<string, any>;
  evidence: Array<Record<string, any>>;
  confidence: number;
  reviewStatus: string;
};

export type Experiment = {
  id: string;
  title: string;
  objective: string;
  status: string;
  materials: unknown[];
  procedure: unknown[];
  conditions: Record<string, unknown>;
  observations: unknown[];
  outcome: Record<string, unknown>;
  constraints: Record<string, unknown>;
  source: string;
  createdAt: string;
  updatedAt: string;
};

export type Direction = {
  title: string;
  hypothesis: string;
  rationale: string;
  novelty: string;
  systemDesign: {
    molecularSieveRole: string;
    activePhaseRole: string;
    interfaceStrategy: string;
    proposedPathway: string;
    selectivityTarget: string;
    evidenceBoundary: string;
  };
  supportingEvidence: Array<{ nodeId: string; paperId?: string | null; quote?: string | null; role: string }>;
  feasibility: 'high' | 'medium' | 'low';
  confidence: number;
  risks: string[];
  nextExperiment: {
    objective: string;
    materials: string[];
    procedure: string[];
    variables: string[];
    controls: string[];
    measurements: string[];
    decisionRules: string[];
    stoppingCriteria: string[];
  };
};

export type Advice = {
  answer: string;
  candidateDirections: Direction[];
  contradictions: string[];
  dataGaps: string[];
  safetyNotes: string[];
};

export const api = {
  me: () => request<{ user: User }>('/auth/me'),
  login: (identifier: string, password: string) =>
    request<{ user: User }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ identifier, password })
    }),
  register: (username: string, email: string, password: string, profile: RegistrationProfile) =>
    request<{ user: User }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password, profile })
    }),
  logout: () => request('/auth/logout', { method: 'POST' }),
  workspaces: () => request<{ workspaces: Workspace[] }>('/workspaces'),
  workspace: (id: string) => request<{ workspace: Workspace }>(`/workspaces/${id}`),
  stats: (id: string) => request<any>(`/research/workspaces/${id}/stats`),
  graph: (id: string, search = '') =>
    request<{ nodes: GraphNode[]; edges: Array<{ id: string; from: string; to: string; type: string }> }>(
      `/research/workspaces/${id}/graph?limit=320&search=${encodeURIComponent(search)}`
    ),
  experiments: (id: string) =>
    request<{ experiments: Experiment[] }>(`/research/workspaces/${id}/experiments`),
  saveExperiment: (id: string, experiment: Partial<Experiment> & { title: string }) =>
    request<{ experiment: Experiment }>(`/research/workspaces/${id}/experiments`, {
      method: 'POST',
      body: JSON.stringify(experiment)
    }),
  advice: (
    id: string,
    input: {
      goal: string;
      question?: string;
      experimentId?: string | null;
      preferredDirectionCount?: number;
      focus?: string;
      constraints?: Record<string, unknown>;
    }
  ) => request<{
    runId: string;
    advice: Advice;
    provider: string;
    model: string;
    evidenceNodeCount: number;
    paperCount: number;
    profileLearning: {
      updated: boolean;
      learned: Array<{ category: string; value: string; confidence: number }>;
      total: number;
    };
    profileFollowUpQuestions: ProfileFollowUpQuestion[];
  }>(`/research/workspaces/${id}/advice`, {
    method: 'POST',
    body: JSON.stringify(input)
  }),
  plan: (workspaceId: string, runId: string, directionIndex: number) =>
    request<{ direction: Direction; safetyNotes: string[]; dataGaps: string[] }>(
      `/research/workspaces/${workspaceId}/advice/${runId}/experiment-plan`,
      { method: 'POST', body: JSON.stringify({ directionIndex }) }
    ),
  profile: () => request<{ profile: ResearcherProfile }>('/profile'),
  updateProfile: (profile: ResearcherProfile) =>
    request<{ profile: ResearcherProfile }>('/profile', {
      method: 'PUT',
      body: JSON.stringify(profile)
    }),
  profileQuestions: () =>
    request<{
      questions: ProfileQuestion[];
      progress: { answered: number; total: number; completed: boolean };
    }>('/profile/questions'),
  answerProfileQuestion: (questionId: string, answer: string | string[]) =>
    request<{ profile: ResearcherProfile }>(`/profile/questions/${questionId}`, {
      method: 'PUT',
      body: JSON.stringify({ answer })
    }),
  completeProfileInterview: () =>
    request<{ profile: ResearcherProfile }>('/profile/questions/complete', { method: 'POST' }),
  learnProfile: (category: string, value: string, evidence: string) =>
    request<{ learning: { updated: boolean; total: number } }>('/profile/learn', {
      method: 'POST',
      body: JSON.stringify({ category, value, evidence })
    })
};

export type ResearcherProfile = {
  institution: string;
  role: string;
  primaryCatalysis: 'photocatalysis' | 'thermal_catalysis' | 'both' | 'undecided';
  molecularSievePreference: 'central' | 'when_helpful' | 'minimal';
  heterojunctionPreference: 'prefer' | 'evidence_based' | 'avoid_overuse';
  riskTolerance: 'conservative' | 'balanced' | 'exploratory';
  researchInterests: string[];
  catalystSystems: string[];
  techniques: string[];
  currentGoals: string[];
  researchPriorities: string[];
  availableResources: string[];
  avoidances: string[];
  experimentalConstraints: Record<string, unknown>;
  preferredOutputStyle: string;
  openResearchContext: string;
  notes: string;
  learnedPreferences: LearnedPreference[];
  interviewAnswers: Record<string, { answer: unknown; answeredAt: string }>;
  interactionCount?: number;
  lastLearnedAt?: string | null;
  onboardingCompletedAt?: string | null;
  updatedAt?: string;
};

export type ProfileQuestion = {
  id: string;
  title: string;
  prompt: string;
  hint?: string;
  type: 'text' | 'single' | 'multiple';
  options?: Array<{ value: string; label: string; description?: string }>;
  answer: string | string[];
  answered: boolean;
};

export type ProfileFollowUpQuestion = {
  category: string;
  question: string;
  reason: string;
};

export type LearnedPreference = {
  id: string;
  category: string;
  value: string;
  evidence: string;
  confidence: number;
  occurrences: number;
  firstSeenAt: string;
  lastSeenAt: string;
  source: 'conversation';
};

export type RegistrationProfile = Pick<
  ResearcherProfile,
  | 'role'
  | 'primaryCatalysis'
  | 'molecularSievePreference'
  | 'heterojunctionPreference'
  | 'researchPriorities'
  | 'availableResources'
  | 'avoidances'
  | 'preferredOutputStyle'
  | 'openResearchContext'
>;

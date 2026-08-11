import {
  api,
  Direction,
  Experiment,
  GraphNode,
  ProfileFollowUpQuestion
} from '../api';

export type ResearchGraphNode = GraphNode & {
  key?: string;
  canonicalName?: string;
  zhName?: string;
  localId?: string | null;
};

export type ResearchExperimentLog = Experiment;

export type ResearchDirection = Omit<Direction, 'systemDesign'> & {
  couplingDesign: {
    molecularSieveRole: string;
    photocatalystRole: string;
    interfaceStrategy: string;
    proposedPathway: string;
    selectivityTarget: string;
    evidenceBoundary: string;
  };
};

export type ResearchAdvice = {
  answer: string;
  candidateDirections: ResearchDirection[];
  contradictions: string[];
  dataGaps: string[];
  safetyNotes: string[];
};

const directionFromApi = (direction: Direction): ResearchDirection => {
  const { systemDesign, ...rest } = direction;
  return {
    ...rest,
    couplingDesign: {
      molecularSieveRole: systemDesign.molecularSieveRole,
      photocatalystRole: systemDesign.activePhaseRole,
      interfaceStrategy: systemDesign.interfaceStrategy,
      proposedPathway: systemDesign.proposedPathway,
      selectivityTarget: systemDesign.selectivityTarget,
      evidenceBoundary: systemDesign.evidenceBoundary
    }
  };
};

const adviceFromApi = (advice: Awaited<ReturnType<typeof api.advice>>['advice']): ResearchAdvice => ({
  ...advice,
  candidateDirections: advice.candidateDirections.map(directionFromApi)
});

export const researchApi = {
  getWorkspace: async (workspaceId: string) => (await api.workspace(workspaceId)).workspace,
  getStats: (workspaceId: string) => api.stats(workspaceId),
  getGraph: async (workspaceId: string, params?: { search?: string; nodeTypes?: string[]; limit?: number }) => {
    const result = await api.graph(workspaceId, params?.search || '');
    return { ...result, documents: [] as Array<Record<string, unknown>> };
  },
  listExperiments: async (workspaceId: string) => (await api.experiments(workspaceId)).experiments,
  saveExperiment: async (
    workspaceId: string,
    experiment: Partial<ResearchExperimentLog> & { title: string }
  ) => (await api.saveExperiment(workspaceId, experiment)).experiment,
  requestAdvice: async (
    workspaceId: string,
    input: {
      goal: string;
      question?: string;
      experimentId?: string | null;
      constraints?: Record<string, unknown>;
      preferredDirectionCount?: number;
      focus?: 'performance' | 'engineering' | 'gap';
    }
  ) => {
    const result = await api.advice(workspaceId, input);
    return {
      ...result,
      advice: adviceFromApi(result.advice),
      profileFollowUpQuestions: result.profileFollowUpQuestions as ProfileFollowUpQuestion[]
    };
  },
  planExperiment: async (workspaceId: string, runId: string, directionIndex: number) => {
    const result = await api.plan(workspaceId, runId, directionIndex);
    return { ...result, direction: directionFromApi(result.direction) };
  }
};

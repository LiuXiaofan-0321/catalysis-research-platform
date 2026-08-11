import prisma from '../config/db';

export const PRIMARY_CATALYSIS = ['photocatalysis', 'thermal_catalysis', 'both', 'undecided'] as const;
export const MOLECULAR_SIEVE_PREFERENCES = ['central', 'when_helpful', 'minimal'] as const;
export const HETEROJUNCTION_PREFERENCES = ['prefer', 'evidence_based', 'avoid_overuse'] as const;
export const OUTPUT_STYLES = ['evidence_first', 'experiment_first', 'mechanism_first', 'concise'] as const;
export const RISK_TOLERANCES = ['conservative', 'balanced', 'exploratory'] as const;

const LEARNING_CATEGORIES = [
  'research_interest',
  'catalyst_system',
  'technique',
  'goal',
  'constraint',
  'output_style',
  'avoidance',
  'resource'
] as const;

export type LearningCategory = typeof LEARNING_CATEGORIES[number];

export type LearnedPreference = {
  id: string;
  category: LearningCategory;
  value: string;
  evidence: string;
  confidence: number;
  occurrences: number;
  firstSeenAt: string;
  lastSeenAt: string;
  source: 'conversation';
};

export type ProfileLearningCandidate = {
  category?: unknown;
  value?: unknown;
  confidence?: unknown;
};

const parse = <T>(value: string | null | undefined, fallback: T): T => {
  try {
    return value ? JSON.parse(value) as T : fallback;
  } catch {
    return fallback;
  }
};

const clip = (value: unknown, max = 1200) => {
  const normalized = String(value ?? '').replace(/\s+/g, ' ').trim();
  return normalized.length > max ? `${normalized.slice(0, max)}...` : normalized;
};

const stringList = (value: unknown, maxItems = 50, maxLength = 240) =>
  Array.isArray(value)
    ? Array.from(new Set(value.map((item) => clip(item, maxLength)).filter(Boolean))).slice(0, maxItems)
    : [];

const enumValue = <T extends readonly string[]>(value: unknown, allowed: T, fallback: T[number]) => {
  const normalized = String(value || '');
  return (allowed as readonly string[]).includes(normalized) ? normalized as T[number] : fallback;
};

const constraints = (value: unknown) => {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {};
  return Object.fromEntries(
    Object.entries(value as Record<string, unknown>)
      .slice(0, 40)
      .map(([key, item]) => {
        const safeKey = clip(key, 80);
        if (Array.isArray(item)) return [safeKey, stringList(item, 20, 180)];
        if (typeof item === 'number' || typeof item === 'boolean') return [safeKey, item];
        return [safeKey, clip(item, 500)];
      })
      .filter(([key]) => Boolean(key))
  );
};

const learnedPreferences = (value: unknown): LearnedPreference[] => {
  if (!Array.isArray(value)) return [];
  return value
    .map((item: any) => {
      const category = enumValue(item?.category, LEARNING_CATEGORIES, '' as LearningCategory);
      const preferenceValue = clip(item?.value, 280);
      if (!category || !preferenceValue) return null;
      const firstSeenAt = Number.isNaN(Date.parse(String(item?.firstSeenAt))) ? new Date().toISOString() : String(item.firstSeenAt);
      const lastSeenAt = Number.isNaN(Date.parse(String(item?.lastSeenAt))) ? firstSeenAt : String(item.lastSeenAt);
      return {
        id: clip(item?.id, 120) || `${category}:${preferenceValue.toLowerCase()}`,
        category,
        value: preferenceValue,
        evidence: clip(item?.evidence, 600),
        confidence: Math.max(0, Math.min(1, Number(item?.confidence) || 0)),
        occurrences: Math.max(1, Math.min(999, Number(item?.occurrences) || 1)),
        firstSeenAt,
        lastSeenAt,
        source: 'conversation' as const
      };
    })
    .filter(Boolean)
    .slice(0, 50) as LearnedPreference[];
};

export const serializeResearcherProfile = (profile: any) => ({
  id: profile.id,
  institution: profile.institution || '',
  role: profile.role || '',
  primaryCatalysis: enumValue(profile.primaryCatalysis, PRIMARY_CATALYSIS, 'undecided'),
  molecularSievePreference: enumValue(
    profile.molecularSievePreference,
    MOLECULAR_SIEVE_PREFERENCES,
    'when_helpful'
  ),
  heterojunctionPreference: enumValue(
    profile.heterojunctionPreference,
    HETEROJUNCTION_PREFERENCES,
    'evidence_based'
  ),
  riskTolerance: enumValue(profile.riskTolerance, RISK_TOLERANCES, 'balanced'),
  researchInterests: parse<string[]>(profile.researchInterestsJson, []),
  catalystSystems: parse<string[]>(profile.catalystSystemsJson, []),
  techniques: parse<string[]>(profile.techniquesJson, []),
  currentGoals: parse<string[]>(profile.currentGoalsJson, []),
  researchPriorities: parse<string[]>(profile.researchPrioritiesJson, []),
  availableResources: parse<string[]>(profile.availableResourcesJson, []),
  avoidances: parse<string[]>(profile.avoidancesJson, []),
  experimentalConstraints: parse<Record<string, unknown>>(profile.experimentalConstraintsJson, {}),
  preferredOutputStyle: enumValue(profile.preferredOutputStyle, OUTPUT_STYLES, 'evidence_first'),
  openResearchContext: profile.openResearchContext || '',
  notes: profile.notes || '',
  learnedPreferences: learnedPreferences(parse(profile.learnedPreferencesJson, [])),
  interviewAnswers: parse<Record<string, { answer: unknown; answeredAt: string }>>(profile.interviewAnswersJson, {}),
  interactionCount: profile.interactionCount || 0,
  lastLearnedAt: profile.lastLearnedAt || null,
  onboardingCompletedAt: profile.onboardingCompletedAt || null,
  updatedAt: profile.updatedAt
});

export const profileCreateData = (userId: string, input: any = {}, completeOnboarding = false) => ({
  userId,
  institution: clip(input.institution, 240) || null,
  role: clip(input.role, 160) || null,
  primaryCatalysis: enumValue(input.primaryCatalysis, PRIMARY_CATALYSIS, 'undecided'),
  molecularSievePreference: enumValue(
    input.molecularSievePreference,
    MOLECULAR_SIEVE_PREFERENCES,
    'when_helpful'
  ),
  heterojunctionPreference: enumValue(
    input.heterojunctionPreference,
    HETEROJUNCTION_PREFERENCES,
    'evidence_based'
  ),
  riskTolerance: enumValue(input.riskTolerance, RISK_TOLERANCES, 'balanced'),
  researchInterestsJson: JSON.stringify(stringList(input.researchInterests)),
  catalystSystemsJson: JSON.stringify(stringList(input.catalystSystems)),
  techniquesJson: JSON.stringify(stringList(input.techniques)),
  currentGoalsJson: JSON.stringify(stringList(input.currentGoals)),
  researchPrioritiesJson: JSON.stringify(stringList(input.researchPriorities)),
  availableResourcesJson: JSON.stringify(stringList(input.availableResources)),
  avoidancesJson: JSON.stringify(stringList(input.avoidances)),
  experimentalConstraintsJson: JSON.stringify(constraints(input.experimentalConstraints)),
  preferredOutputStyle: enumValue(input.preferredOutputStyle, OUTPUT_STYLES, 'evidence_first'),
  openResearchContext: clip(input.openResearchContext, 4000),
  notes: clip(input.notes, 4000),
  learnedPreferencesJson: JSON.stringify(learnedPreferences(input.learnedPreferences)),
  interviewAnswersJson: JSON.stringify(
    input.interviewAnswers && typeof input.interviewAnswers === 'object' ? input.interviewAnswers : {}
  ),
  onboardingCompletedAt: completeOnboarding ? new Date() : null
});

export const profileUpdateData = (input: any = {}, completeOnboarding = true) => {
  const { userId: _userId, ...data } = profileCreateData('', input, completeOnboarding);
  return data;
};

export const getOrCreateResearcherProfile = (userId: string) =>
  prisma.researcherProfile.upsert({
    where: { userId },
    update: {},
    create: { userId }
  });

export const getResearcherProfileContext = async (userId: string) => {
  const row = await getOrCreateResearcherProfile(userId);
  const profile = serializeResearcherProfile(row);
  const primaryCatalysisRule = {
    photocatalysis: 'Prioritize photocatalysis unless the user explicitly asks to compare with thermal catalysis.',
    thermal_catalysis: 'Prioritize thermal catalysis unless the user explicitly asks to compare with photocatalysis.',
    both: 'The researcher works across both catalysis modes; keep the current workspace evidence boundary.',
    undecided: 'Do not assume a long-term catalysis preference.'
  }[profile.primaryCatalysis];
  const molecularSieveRule = {
    central: 'Prefer directions where the molecular sieve has a clear, central and testable function.',
    when_helpful: 'Use a molecular sieve only when its adsorption, confinement, acidity, shape selectivity or support role is justified.',
    minimal: 'Avoid making the molecular sieve central unless the evidence shows it is necessary.'
  }[profile.molecularSievePreference];
  const heterojunctionRule = {
    prefer: 'Heterojunction designs may be prioritized when they are evidence-grounded and experimentally testable.',
    evidence_based: 'Recommend a heterojunction only when the interface and expected benefit are supported by evidence.',
    avoid_overuse: 'Do not stack or overemphasize heterojunctions; require a specific interface mechanism and a discriminating control.'
  }[profile.heterojunctionPreference];
  return {
    primaryCatalysis: profile.primaryCatalysis,
    molecularSievePreference: profile.molecularSievePreference,
    heterojunctionPreference: profile.heterojunctionPreference,
    riskTolerance: profile.riskTolerance,
    institution: profile.institution,
    role: profile.role,
    researchInterests: profile.researchInterests,
    catalystSystems: profile.catalystSystems,
    techniques: profile.techniques,
    currentGoals: profile.currentGoals,
    researchPriorities: profile.researchPriorities,
    availableResources: profile.availableResources,
    avoidances: profile.avoidances,
    experimentalConstraints: profile.experimentalConstraints,
    preferredOutputStyle: profile.preferredOutputStyle,
    openResearchContext: profile.openResearchContext,
    notes: profile.notes,
    learnedPreferences: profile.learnedPreferences.map(({ category, value, confidence, occurrences }) => ({
      category,
      value,
      confidence,
      occurrences
    })),
    activePreferenceRules: [primaryCatalysisRule, molecularSieveRule, heterojunctionRule],
    instruction: [
      'Use this profile to rank feasible directions, choose explanation depth, and respect explicit constraints.',
      'Treat avoidances and constraints as hard requirements unless they conflict with safety or evidence.',
      'Do not let profile preferences alter paper facts or inflate evidence confidence.',
      'When a preference conflicts with the evidence, explain the conflict instead of silently following it.'
    ]
  };
};

export const mergeConversationLearning = async (
  userId: string,
  candidates: ProfileLearningCandidate[],
  sourceText: string
) => {
  const row = await getOrCreateResearcherProfile(userId);
  const current = learnedPreferences(parse(row.learnedPreferencesJson, []));
  const now = new Date();
  const evidence = clip(sourceText, 600);
  const accepted = (Array.isArray(candidates) ? candidates : [])
    .map((candidate) => ({
      category: enumValue(candidate?.category, LEARNING_CATEGORIES, '' as LearningCategory),
      value: clip(candidate?.value, 280),
      confidence: Math.max(0, Math.min(1, Number(candidate?.confidence) || 0))
    }))
    .filter((candidate) => candidate.category && candidate.value && candidate.confidence >= 0.8)
    .slice(0, 6);

  for (const candidate of accepted) {
    const key = `${candidate.category}:${candidate.value.toLowerCase()}`;
    const existing = current.find((item) => item.id === key);
    if (existing) {
      existing.confidence = Math.max(existing.confidence, candidate.confidence);
      existing.occurrences += 1;
      existing.lastSeenAt = now.toISOString();
      existing.evidence = evidence;
    } else {
      current.push({
        id: key,
        category: candidate.category,
        value: candidate.value,
        evidence,
        confidence: candidate.confidence,
        occurrences: 1,
        firstSeenAt: now.toISOString(),
        lastSeenAt: now.toISOString(),
        source: 'conversation'
      });
    }
  }

  const ordered = current
    .sort((left, right) => Date.parse(right.lastSeenAt) - Date.parse(left.lastSeenAt))
    .slice(0, 50);
  await prisma.researcherProfile.update({
    where: { userId },
    data: {
      learnedPreferencesJson: JSON.stringify(ordered),
      interactionCount: { increment: 1 },
      lastLearnedAt: accepted.length ? now : row.lastLearnedAt
    }
  });
  return {
    updated: accepted.length > 0,
    learned: accepted,
    total: ordered.length
  };
};

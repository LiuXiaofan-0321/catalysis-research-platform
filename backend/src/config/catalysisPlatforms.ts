export const CATALYSIS_PLATFORMS = [
  {
    id: 'catalysis-photocatalysis-corpus-v1',
    name: '光催化科研实验平台',
    catalysisSystem: 'photocatalysis',
    description: '面向光催化文献证据图谱、候选研究方向预测与实验反馈迭代的科研工作空间'
  },
  {
    id: 'catalysis-thermal-corpus-v1',
    name: '热催化科研实验平台',
    catalysisSystem: 'thermal_catalysis',
    description: '面向分子筛热催化文献证据检索、研究方向生成与实验反馈闭环的科研工作空间'
  }
] as const;

export const platformForSystem = (catalysisSystem: string) =>
  CATALYSIS_PLATFORMS.find((platform) => platform.catalysisSystem === catalysisSystem);

export const userWorkspaceData = (catalysisSystem: string) => {
  const platform = platformForSystem(catalysisSystem);
  if (!platform) throw new Error(`Unsupported catalysis system: ${catalysisSystem}`);
  return {
    name: platform.name,
    catalysisSystem: platform.catalysisSystem,
    description: platform.description,
    corpusWorkspaceId: platform.id
  };
};

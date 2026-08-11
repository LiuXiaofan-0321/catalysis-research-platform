import '../config/env';
import fs from 'fs/promises';
import os from 'os';
import path from 'path';
import AdmZip from 'adm-zip';
import { platformForSystem } from '../config/catalysisPlatforms';
import prisma, { configureDatabase } from '../config/db';
import { ensureResearchSchema } from '../config/ensureResearchSchema';
import { researchGraphService } from '../services/researchGraphService';

const args = process.argv.slice(2);
const valueFor = (name: string) => {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : undefined;
};

const findJsonDirectory = async (root: string): Promise<string> => {
  const direct = path.join(root, 'json');
  if (await fs.stat(direct).then((stat) => stat.isDirectory()).catch(() => false)) return direct;
  const files = await fs.readdir(root, { withFileTypes: true });
  if (files.some((entry) => entry.isFile() && entry.name.endsWith('.json'))) return root;
  for (const entry of files.filter((item) => item.isDirectory())) {
    const nested = path.join(root, entry.name);
    const found: string | null = await findJsonDirectory(nested).catch(() => null);
    if (found) return found;
  }
  throw new Error('数据包中未找到 JSON 目录');
};

const main = async () => {
  await configureDatabase();
  await ensureResearchSchema();
  const input = valueFor('--input');
  const system = valueFor('--system');
  const username = valueFor('--username') || process.env.INITIAL_ADMIN_USERNAME || 'admin';
  if (!input || !['photocatalysis', 'thermal_catalysis'].includes(String(system))) {
    throw new Error('用法：--input <目录或zip> --system photocatalysis|thermal_catalysis [--username admin] [--replace]');
  }
  const user = await prisma.user.findUnique({ where: { username } });
  if (!user) throw new Error(`用户不存在：${username}，请先运行 bootstrap`);
  const platform = platformForSystem(String(system));
  const workspace = platform
    ? await prisma.workspace.findUnique({ where: { id: platform.id } })
    : null;
  if (!workspace) throw new Error(`未找到 ${system} Workspace`);

  const resolved = path.resolve(input);
  let temporaryDirectory: string | null = null;
  let root = resolved;
  if (resolved.toLowerCase().endsWith('.zip')) {
    temporaryDirectory = await fs.mkdtemp(path.join(os.tmpdir(), 'catalysis-import-'));
    new AdmZip(resolved).extractAllTo(temporaryDirectory, true);
    root = temporaryDirectory;
  }
  try {
    const jsonDirectory = await findJsonDirectory(root);
    const { artifacts, errors } = await researchGraphService.readArtifactsFromDirectory(jsonDirectory);
    if (errors.length) {
      console.warn(`跳过 ${errors.length} 个无效 JSON`);
      errors.slice(0, 10).forEach((error) => console.warn(`${error.file}: ${error.error}`));
    }
    const allowedSystems = system === 'photocatalysis'
      ? ['photocatalysis', 'both']
      : ['thermal_catalysis'];
    const result = await researchGraphService.importArtifacts(workspace.id, artifacts, {
      allowedSystems,
      replaceWorkspace: args.includes('--replace')
    });
    console.log(JSON.stringify({ workspace, jsonDirectory, parseErrors: errors.length, ...result }, null, 2));
  } finally {
    if (temporaryDirectory) {
      await fs.rm(temporaryDirectory, { recursive: true, force: true });
    }
  }
};

main()
  .catch((error) => {
    console.error(error instanceof Error ? error.message : error);
    process.exitCode = 1;
  })
  .finally(async () => prisma.$disconnect());

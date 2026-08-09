import fs from 'fs/promises';
import path from 'path';
import AdmZip from 'adm-zip';
import { stableHash } from '../utils/hash';

const args = process.argv.slice(2);
const valueFor = (name: string) => {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : undefined;
};
const valuesFor = (name: string) =>
  args.flatMap((item, index) => item === name && args[index + 1] ? [args[index + 1]] : []);

const main = async () => {
  const inputs = valuesFor('--input');
  const output = valueFor('--output');
  const systems = new Set(
    String(valueFor('--systems') || '').split(',').map((item) => item.trim()).filter(Boolean)
  );
  if (!inputs.length || !output || !systems.size) {
    throw new Error('用法：--input <stage1目录> [--input <另一目录>] --output <zip> --systems photocatalysis,both');
  }
  const zip = new AdmZip();
  const counts = {
    documents: 0,
    keywords: 0,
    entities: 0,
    experiments: 0,
    observations: 0,
    claims: 0,
    systems: {} as Record<string, number>,
    paperTypes: {} as Record<string, number>
  };
  const documentKeys: string[] = [];
  const selected = new Map<string, { name: string; buffer: Buffer; artifact: any }>();
  for (const input of inputs) {
    const root = path.resolve(input);
    const jsonDirectory = await fs.stat(path.join(root, 'json')).then((stat) => stat.isDirectory()).catch(() => false)
      ? path.join(root, 'json')
      : root;
    const files = (await fs.readdir(jsonDirectory))
      .filter((name) => name.toLowerCase().endsWith('.json'))
      .sort();
    for (const name of files) {
      const buffer = await fs.readFile(path.join(jsonDirectory, name));
      const artifact = JSON.parse(buffer.toString('utf8'));
      const paper = artifact?.extraction?.paper;
      const system = String(paper?.catalysis_system || 'unclear');
      if (!systems.has(system)) continue;
      const key = String(
        paper?.doi ||
        paper?.source_pdf_sha256 ||
        artifact?.source?.source_pdf_sha256 ||
        `${paper?.title || name}:${paper?.year || ''}`
      ).toLowerCase();
      selected.set(key, { name, buffer, artifact });
    }
  }
  let outputIndex = 0;
  for (const [documentKey, selectedItem] of selected) {
    const { name, buffer, artifact } = selectedItem;
    const extraction = artifact?.extraction;
    const paper = extraction?.paper;
    const system = String(paper?.catalysis_system || 'unclear');
    outputIndex += 1;
    zip.addFile(`json/${String(outputIndex).padStart(4, '0')}_${name}`, buffer);
    counts.documents += 1;
    counts.keywords += Array.isArray(extraction?.keywords?.extracted) ? extraction.keywords.extracted.length : 0;
    counts.entities += Array.isArray(extraction?.entities) ? extraction.entities.length : 0;
    counts.experiments += Array.isArray(extraction?.experiments) ? extraction.experiments.length : 0;
    counts.observations += Array.isArray(extraction?.observations) ? extraction.observations.length : 0;
    counts.claims += Array.isArray(extraction?.claims) ? extraction.claims.length : 0;
    counts.systems[system] = (counts.systems[system] || 0) + 1;
    const paperType = String(paper?.paper_type || 'unknown');
    counts.paperTypes[paperType] = (counts.paperTypes[paperType] || 0) + 1;
    documentKeys.push(documentKey);
  }
  const manifest = {
    schema: 'catalysis_research_dataset.v1',
    generatedAt: new Date().toISOString(),
    allowedSystems: Array.from(systems),
    counts,
    corpusFingerprint: stableHash(documentKeys.sort())
  };
  zip.addFile('dataset-manifest.json', Buffer.from(JSON.stringify(manifest, null, 2), 'utf8'));
  await fs.mkdir(path.dirname(path.resolve(output)), { recursive: true });
  zip.writeZip(path.resolve(output));
  console.log(JSON.stringify({ output: path.resolve(output), ...manifest }, null, 2));
};

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});

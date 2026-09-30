"""Merge fixed trajectory identities, never choose outcomes by performance."""
import argparse
import json
from pathlib import Path
import shutil
from summarize_jacs_au_kg_v4 import summarize


def merge(source, recovery, output):
    if output.exists():
        raise ValueError('Use a fresh merged output directory')
    manifest=[]
    for effort in ['low','high']:
        for mode in ['agent','rag_agent','small_kg_rag_agent']:
            for rep in range(1,4):
                relative=Path(effort)/'discovery'/f'{mode}-replicate-{rep}.json'
                original=source/relative
                row=json.loads(original.read_text(encoding='utf-8'))
                selected=original
                if row['status']=='failed' and (recovery/relative).exists():
                    selected=recovery/relative
                    recovered=json.loads(selected.read_text(encoding='utf-8'))
                    if Path(recovered.get('recovery',{}).get('source',''))!=original:
                        raise ValueError('Recovery source identity differs')
                destination=output/relative
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(selected,destination)
                manifest.append({'identity':str(relative),'original':str(original),'selected_record':str(selected),
                                 'original_status':row['status'],'original_retained':True})
    (output/'recovery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summarize(output)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for key in ['source','recovery','output']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();merge(args.source,args.recovery,args.output)

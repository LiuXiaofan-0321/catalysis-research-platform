"""Compute-node GLM probe. API credentials are read only from the environment."""
import argparse
import json
from pathlib import Path

from catalysis_research.models.glm import GlmClient


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    response = GlmClient(retries=0).chat_json(
        model='glm-5.3-flash', system='Return JSON only.',
        user='Return a JSON object with ok set to true.',
        max_tokens=1024, thinking='enabled', reasoning_effort='low')
    result = {'ok': response.structured.get('ok') is True,
              'model': response.model, 'finish_reason': response.raw['choices'][0].get('finish_reason'),
              'usage': response.usage}
    if not result['ok'] or result['finish_reason'] != 'stop':
        raise RuntimeError('Compute-node GLM probe failed')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'ok': True, 'model': result['model'], 'finish_reason': 'stop'}))


if __name__ == '__main__': main()

"""Headless article/text -> script -> optional speech, without the malformed UI."""

import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--text-file', type=Path)
    source.add_argument('--url')
    parser.add_argument('--output-dir', type=Path, default=Path('outputs/podcast'))
    parser.add_argument('--speech', action='store_true', help='Also request paid MiniMax speech synthesis')
    parser.add_argument('--max-chars', type=int, default=50000)
    args = parser.parse_args()
    from dotenv import load_dotenv
    load_dotenv()
    required = ['OPENROUTER_API_KEY']
    if args.url:
        required.append('FIRECRAWL_API_KEY')
    if args.speech:
        required.append('MINIMAX_API_KEY')
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        parser.error('Missing environment variables: ' + ', '.join(missing))
    if args.max_chars < 1:
        parser.error('--max-chars must be positive')
    if args.text_file:
        if args.text_file.stat().st_size > args.max_chars * 4:
            parser.error('Text file exceeds the input budget')
        content = args.text_file.read_text(encoding='utf-8')
    else:
        from urllib.parse import urlparse
        if urlparse(args.url).scheme not in {'http', 'https'}:
            parser.error('URL must use HTTP or HTTPS')
        from scraper import WebScraper
        content = WebScraper().scrape(args.url)
    if not content.strip() or len(content) > args.max_chars:
        parser.error('Source is empty or exceeds --max-chars')
    from script_generator import ScriptGenerator
    script = ScriptGenerator().generate(content)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'script.txt').write_text(script, encoding='utf-8')
    manifest = {'script': 'script.txt', 'status': 'script-complete', 'speech_requested': args.speech, 'audio_segments': []}
    manifest_path = args.output_dir / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    if args.speech:
        from tts_converter import TTSConverter
        try:
            converter = TTSConverter()
            if not converter._parse_script(script):
                raise ValueError('Generated script has no recognized Host 1/Host 2 speech segments')
            manifest['audio_segments'] = converter.convert(script, str(args.output_dir / 'segments'))
            manifest['status'] = 'speech-complete'
        except Exception:
            manifest['status'] = 'speech-failed'
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
            raise
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()

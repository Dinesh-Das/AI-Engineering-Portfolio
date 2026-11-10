"""Headless meeting-note processing with structured JSON output."""

import argparse
import json
import os
from dataclasses import asdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('audio', type=Path)
    parser.add_argument('--output', type=Path, default=Path('outputs/meeting.json'))
    parser.add_argument('--max-mb', type=int, default=100)
    args = parser.parse_args()
    if not args.audio.is_file() or not 0 < args.audio.stat().st_size <= args.max_mb * 1024 * 1024:
        parser.error('Audio must be a nonempty file within --max-mb')
    from dotenv import load_dotenv
    load_dotenv()
    missing = [name for name in ('ASSEMBLYAI_API_KEY', 'OPENAI_API_KEY') if not os.getenv(name)]
    if missing:
        parser.error('Missing environment variables: ' + ', '.join(missing))
    from src.services.audio_processor import MeetingProcessor
    result = MeetingProcessor(os.environ['ASSEMBLYAI_API_KEY'], os.environ['OPENAI_API_KEY']).process_meeting_audio(str(args.audio))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(asdict(result), default=str, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Wrote ' + str(args.output))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Convert a Claude Code JSONL session file to a readable Markdown document.
Extracts only human-readable user and assistant text, skipping tool calls,
tool results, thinking blocks, and system metadata.

Usage:
    python3 export_chat.py                        # uses hardcoded path below
    python3 export_chat.py <path_to.jsonl>        # specify a different session
"""

import json
import sys
import os
from datetime import datetime, timezone

JSONL_PATH = os.path.expanduser(
    '/Users/rohn/.claude/projects/-Users-rohn-Serve/'
    '90e862e6-df42-4e2e-84b3-331f52c3e391.jsonl'
)
OUTPUT_PATH = os.path.expanduser('/Users/rohn/Serve/chat_export.md')


def extract_text(content):
    """Return readable text from a message content field (string or list of blocks)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'text':
                text = block.get('text', '').strip()
                if text:
                    parts.append(text)
        return '\n\n'.join(parts)
    return ''


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else JSONL_PATH

    if not os.path.exists(path):
        print(f'Error: file not found: {path}')
        sys.exit(1)

    turns = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_type = obj.get('type')
            if msg_type not in ('user', 'assistant'):
                continue

            # Skip sidechain messages (sub-agent internal turns)
            if obj.get('isSidechain'):
                continue

            message = obj.get('message', {})
            content = message.get('content', '')
            timestamp = obj.get('timestamp', '')

            # For user turns, skip pure tool-result messages
            # (those are calculator/tool responses, not human text)
            if msg_type == 'user':
                if isinstance(content, list):
                    has_human_text = any(
                        b.get('type') == 'text' for b in content
                        if isinstance(b, dict)
                    )
                    if not has_human_text:
                        continue

            text = extract_text(content)
            if not text:
                continue

            turns.append({
                'role': msg_type,
                'text': text,
                'timestamp': timestamp,
            })

    if not turns:
        print('No readable turns found.')
        sys.exit(1)

    # Write Markdown
    lines = []
    lines.append('# Claude Code Session Transcript')
    lines.append('')

    # Try to get date from first turn
    if turns and turns[0]['timestamp']:
        try:
            dt = datetime.fromisoformat(turns[0]['timestamp'].replace('Z', '+00:00'))
            lines.append(f'**Session started:** {dt.strftime("%Y-%m-%d %H:%M UTC")}')
        except ValueError:
            pass

    lines.append(f'**Turns exported:** {len(turns)}')
    lines.append(f'**Source:** `{os.path.basename(path)}`')
    lines.append('')
    lines.append('---')
    lines.append('')

    for i, turn in enumerate(turns, 1):
        role_label = '## User' if turn['role'] == 'user' else '## Assistant'
        lines.append(role_label)
        lines.append('')
        lines.append(turn['text'])
        lines.append('')
        lines.append('---')
        lines.append('')

    output = '\n'.join(lines)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'Exported {len(turns)} turns to: {OUTPUT_PATH}')
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f'File size: {size_kb:.1f} KB')


if __name__ == '__main__':
    main()

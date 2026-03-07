#!/usr/bin/env python3
"""Translate SRT subtitle file while preserving timestamps.

Usage:
    # Using DeepL API
    python translate_srt.py input.srt -o output.srt --target zh --engine deepl

    # Using OpenAI-compatible API (Claude, GPT, etc.)
    python translate_srt.py input.srt -o output.srt --target zh --engine openai

Engines:
    deepl   - DeepL API (DEEPL_API_KEY required)
    openai  - OpenAI-compatible API (OPENAI_API_KEY + OPENAI_BASE_URL)

Exit code 1 on failure.
"""

import argparse
import os
import re
import sys
import json


def parse_srt(srt_path: str) -> list[dict]:
    """Parse SRT file into list of {index, timestamp, text}."""
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n\n+", content.strip())
    entries = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            entries.append({
                "index": lines[0].strip(),
                "timestamp": lines[1].strip(),
                "text": "\n".join(lines[2:]).strip()
            })
    return entries


def write_srt(entries: list[dict], output_path: str):
    """Write entries back to SRT format."""
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(f"{entry['index']}\n")
            f.write(f"{entry['timestamp']}\n")
            f.write(f"{entry['text']}\n\n")


def translate_deepl(texts: list[str], target_lang: str) -> list[str]:
    """Translate texts using DeepL API."""
    try:
        import deepl
    except ImportError:
        print("Error: deepl package not installed. Run: pip install deepl", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        print("Error: DEEPL_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Map common codes to DeepL codes
    lang_map = {
        "zh": "ZH-HANS", "zh-tw": "ZH-HANT", "zh_Hant": "ZH-HANT",
        "en": "EN-US", "pt": "PT-BR", "ja": "JA",
    }
    target = lang_map.get(target_lang, target_lang.upper())

    translator = deepl.Translator(api_key)
    # Batch translate (DeepL handles batching internally)
    results = translator.translate_text(texts, target_lang=target)
    return [r.text for r in results]


def translate_openai(texts: list[str], target_lang: str) -> list[str]:
    """Translate texts using OpenAI-compatible API (Claude, GPT, etc.)."""
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    client = OpenAI()  # reads OPENAI_API_KEY and OPENAI_BASE_URL from env

    lang_names = {
        "zh": "Simplified Chinese", "zh-tw": "Traditional Chinese",
        "zh_Hant": "Traditional Chinese", "zh_Hans": "Simplified Chinese",
        "ja": "Japanese", "en": "English", "ko": "Korean",
        "es": "Spanish", "fr": "French", "de": "German",
    }
    target_name = lang_names.get(target_lang, target_lang)

    # Process in chunks of 50 to avoid token limits
    translated = []
    chunk_size = 50
    for i in range(0, len(texts), chunk_size):
        chunk = texts[i:i + chunk_size]
        numbered = "\n".join(f"[{j}] {t}" for j, t in enumerate(chunk))

        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": f"Translate the following subtitle lines to {target_name}. "
                    f"Preserve the [N] numbering. Output ONLY the translated lines, one per [N] marker. "
                    f"Keep translations natural and context-aware across lines."},
                {"role": "user", "content": numbered}
            ],
            temperature=0.3,
        )

        result = response.choices[0].message.content
        # Parse numbered results
        for line in result.strip().split("\n"):
            match = re.match(r"\[(\d+)\]\s*(.*)", line)
            if match:
                translated.append(match.group(2).strip())

    return translated


def main():
    parser = argparse.ArgumentParser(description="Translate SRT subtitles")
    parser.add_argument("input", help="Input SRT file path")
    parser.add_argument("-o", "--output", help="Output SRT file path (default: input_translated.srt)")
    parser.add_argument("--target", required=True, help="Target language code (zh, zh-tw, ja, en, etc.)")
    parser.add_argument("--engine", default="deepl", choices=["deepl", "openai"],
                        help="Translation engine (default: deepl)")
    args = parser.parse_args()

    # Validate target language code (alphanumeric + hyphens/underscores only)
    if not re.match(r'^[a-zA-Z]{2}([_-][a-zA-Z]{2,4})?$', args.target):
        print(f"Error: Invalid language code: {args.target}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    entries = parse_srt(args.input)
    if not entries:
        print("Error: No subtitle entries found in file", file=sys.stderr)
        sys.exit(1)

    texts = [e["text"] for e in entries]
    print(f"Translating {len(texts)} subtitle lines to {args.target} via {args.engine}...")

    if args.engine == "deepl":
        translated = translate_deepl(texts, args.target)
    else:
        translated = translate_openai(texts, args.target)

    if len(translated) != len(entries):
        print(f"Warning: Got {len(translated)} translations for {len(entries)} entries", file=sys.stderr)

    for i, entry in enumerate(entries):
        if i < len(translated):
            entry["text"] = translated[i]

    output_path = args.output
    if not output_path:
        base, ext = os.path.splitext(args.input)
        output_path = f"{base}_{args.target}{ext}"

    write_srt(entries, output_path)
    print(f"Translated SRT saved: {output_path}")


if __name__ == "__main__":
    main()

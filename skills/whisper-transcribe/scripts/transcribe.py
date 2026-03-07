#!/usr/bin/env python3
"""Download audio from YouTube and transcribe with faster-whisper.

Usage:
    # From YouTube URL
    python transcribe.py "https://youtube.com/watch?v=xxx" -o ./output

    # From local audio file
    python transcribe.py audio.mp3 -o ./output

    # With options
    python transcribe.py "URL" -o ./output --model large-v3 --language ja --device cuda

Output: {output_dir}/{video_id}.srt + {video_id}.txt
Exit code 1 on failure.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile


def sanitize_filename(name: str) -> str:
    """Sanitize a string for safe use as a filename."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def download_audio(url: str, output_dir: str) -> tuple[str, str]:
    """Download audio from YouTube using yt-dlp. Returns (audio_path, video_id)."""
    # Get video ID first
    result = subprocess.run(
        ["yt-dlp", "--print", "id", "--no-download", url],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Error getting video ID (yt-dlp failed)", file=sys.stderr)
        sys.exit(1)
    video_id = sanitize_filename(result.stdout.strip())

    audio_path = os.path.join(output_dir, f"{video_id}.wav")
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "wav",
        "--audio-quality", "0",
        "-o", audio_path,
        url
    ]
    print(f"Downloading audio: {video_id}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error downloading audio (yt-dlp failed)", file=sys.stderr)
        sys.exit(1)

    return audio_path, video_id


def transcribe_local(audio_path: str, model: str, language: str | None, device: str) -> list[dict]:
    """Transcribe using faster-whisper locally."""
    from faster_whisper import WhisperModel

    compute_type = "float16" if device == "cuda" else "int8"
    print(f"Loading model: {model} on {device} ({compute_type})")
    whisper_model = WhisperModel(model, device=device, compute_type=compute_type)

    print("Transcribing...")
    segments, info = whisper_model.transcribe(
        audio_path,
        language=language,
        beam_size=5,
        vad_filter=True,
    )

    if not language:
        print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return results


def transcribe_groq(audio_path: str, language: str | None) -> list[dict]:
    """Transcribe using Groq Whisper API."""
    try:
        from groq import Groq
    except ImportError:
        print("Error: groq package not installed. Run: pip install groq", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    client = Groq(api_key=api_key)
    print("Transcribing via Groq API...")

    with open(audio_path, "rb") as f:
        params = {
            "file": (os.path.basename(audio_path), f),
            "model": "whisper-large-v3",
            "response_format": "verbose_json",
            "timestamp_granularities": ["segment"],
        }
        if language:
            params["language"] = language

        transcription = client.audio.transcriptions.create(**params)

    results = []
    for segment in transcription.segments:
        results.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })

    return results


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format HH:MM:SS,mmm."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(segments: list[dict], output_path: str):
    """Write segments to SRT file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n")
            f.write(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")
    print(f"SRT saved: {output_path} ({len(segments)} segments)")


def write_txt(segments: list[dict], output_path: str):
    """Write segments as plain text."""
    text = " ".join(seg["text"] for seg in segments)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"TXT saved: {output_path} ({len(text)} chars)")


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio/video with Whisper")
    parser.add_argument("input", help="YouTube URL or local audio file path")
    parser.add_argument("-o", "--output", default=".", help="Output directory (default: current)")
    parser.add_argument("--model", default="large-v3", help="Whisper model (default: large-v3)")
    parser.add_argument("--language", help="Language code (auto-detect if omitted)")
    parser.add_argument("--device", default="cuda", choices=["cuda", "cpu"], help="Device (default: cuda)")
    parser.add_argument("--backend", default="local", choices=["local", "groq"], help="Transcription backend (default: local)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Determine if input is URL or local file
    is_url = args.input.startswith(("http://", "https://"))

    if is_url:
        with tempfile.TemporaryDirectory() as tmp:
            audio_path, video_id = download_audio(args.input, tmp)
            if args.backend == "groq":
                segments = transcribe_groq(audio_path, args.language)
            else:
                segments = transcribe_local(audio_path, args.model, args.language, args.device)
    else:
        if not os.path.exists(args.input):
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        audio_path = args.input
        video_id = sanitize_filename(os.path.splitext(os.path.basename(audio_path))[0])
        if args.backend == "groq":
            segments = transcribe_groq(audio_path, args.language)
        else:
            segments = transcribe_local(audio_path, args.model, args.language, args.device)

    if not segments:
        print("Error: No speech detected in audio", file=sys.stderr)
        sys.exit(1)

    srt_path = os.path.join(args.output, f"{video_id}.srt")
    txt_path = os.path.join(args.output, f"{video_id}.txt")

    write_srt(segments, srt_path)
    write_txt(segments, txt_path)

    print(f"\nDone! Files in {args.output}/")


if __name__ == "__main__":
    main()

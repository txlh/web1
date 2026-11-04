#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从视频里抽出音轨，转成 128 kbps 的 MP3。

默认：D:\\sunset.mp4  ->  D:\\sunset.mp3

用法：
    python extract_audio.py
    python extract_audio.py --input "D:\\sunset.mp4" --output "D:\\sunset.mp3"
    python extract_audio.py --bitrate 128k --mono
    python extract_audio.py --start 00:00:30 --duration 120      # 只截取 2 分钟做循环

优先用 ffmpeg（命令行或 imageio-ffmpeg 自带的二进制），找不到时退回 moviepy。
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".flv", ".wmv"}


# ── ffmpeg 定位 ────────────────────────────────────────────────
def find_ffmpeg() -> str | None:
    """依次在 PATH、imageio-ffmpeg、常见安装目录里找 ffmpeg。"""
    exe = shutil.which("ffmpeg")
    if exe:
        return exe

    try:  # pip install imageio-ffmpeg —— 自带一个 ffmpeg.exe，最省事
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass

    candidates = [
        Path(r"C:\ffmpeg\bin\ffmpeg.exe"),
        Path(r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"),
        Path(r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"),
        Path.home() / "scoop" / "shims" / "ffmpeg.exe",
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    return None


# ── 两种实现 ──────────────────────────────────────────────────
def extract_with_ffmpeg(ffmpeg: str, opts: argparse.Namespace) -> None:
    cmd = [
        ffmpeg, "-y", "-hide_banner",
        "-i", str(opts.input),
        "-vn",                              # 丢掉视频轨
        "-map_metadata", "-1",              # 不搬运视频里的元数据
        "-ac", "1" if opts.mono else "2",
        "-ar", str(opts.sample_rate),
        "-codec:a", "libmp3lame",
        "-b:a", opts.bitrate,               # 强制 128k
        "-id3v2_version", "3",
    ]
    if opts.start:
        cmd += ["-ss", opts.start]
    if opts.duration:
        cmd += ["-t", opts.duration]
    cmd.append(str(opts.output))

    print("$ " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        tail = "\n".join((proc.stderr or "").strip().splitlines()[-8:])
        raise RuntimeError(f"ffmpeg 失败（退出码 {proc.returncode}）：\n{tail}")


def extract_with_moviepy(opts: argparse.Namespace) -> None:
    try:
        from moviepy import VideoFileClip  # moviepy 2.x
    except ImportError:
        from moviepy.editor import VideoFileClip  # moviepy 1.x

    clip = VideoFileClip(str(opts.input))
    audio = clip.audio
    if audio is None:
        raise RuntimeError("这个视频里没有音轨。")

    if opts.start or opts.duration:
        start = opts.start_seconds
        end = start + opts.duration_seconds if opts.duration else audio.duration
        audio = audio.subclipped(start, end) if hasattr(audio, "subclipped") else audio.subclip(start, end)

    audio.write_audiofile(
        str(opts.output),
        codec="libmp3lame",
        bitrate=opts.bitrate,
        fps=opts.sample_rate,
        ffmpeg_params=["-ac", "1" if opts.mono else "2"],
        logger=None,
    )
    audio.close()
    clip.close()


# ── 参数 ──────────────────────────────────────────────────────
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="从视频提取 128 kbps MP3")
    p.add_argument("--input", "-i", default=r"D:\sunset.mp4", help="源视频路径")
    p.add_argument("--output", "-o", default=r"D:\sunset.mp3", help="输出 MP3 路径")
    p.add_argument("--bitrate", "-b", default="128k", help="音频比特率，默认 128k")
    p.add_argument("--sample-rate", type=int, default=44100, help="采样率，默认 44100")
    p.add_argument("--mono", action="store_true", help="输出单声道（人声/环境音更省，纯音乐建议不加）")
    p.add_argument("--start", default=None, help="从第几秒开始，如 00:00:30 或 30")
    p.add_argument("--duration", default=None, help="截取多长，如 120 或 00:02:00")
    p.add_argument("--engine", choices=["auto", "ffmpeg", "moviepy"], default="auto",
                   help="用哪个引擎，默认自动")
    opts = p.parse_args(argv)

    opts.input = Path(opts.input).expanduser()
    opts.output = Path(opts.output).expanduser()
    opts.start_seconds = _to_seconds(opts.start) if opts.start else 0.0
    opts.duration_seconds = _to_seconds(opts.duration) if opts.duration else None
    return opts


def _to_seconds(value: str) -> float:
    """"00:01:30" / "1:30" / "90" -> 秒。"""
    parts = str(value).split(":")
    try:
        seconds = 0.0
        for part in parts:
            seconds = seconds * 60 + float(part or 0)
        return seconds
    except ValueError:
        raise SystemExit(f"看不懂的时间格式：{value}")


# ── 入口 ──────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    try:  # Windows 控制台默认 GBK，避免个别字符让 print 抛异常
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass

    opts = parse_args(argv)

    if not opts.input.exists():
        print(f"[ERROR] 找不到源文件：{opts.input}")
        print("    检查一下路径，或者用 --input 指定。")
        return 2
    if opts.input.suffix.lower() not in VIDEO_EXTS and opts.input.suffix.lower() != ".mp3":
        print(f"[!] 提示：{opts.input.suffix} 不是常见视频后缀，仍会照常尝试。")

    opts.output.parent.mkdir(parents=True, exist_ok=True)
    before = opts.input.stat().st_size
    print(f"[..] 源文件：{opts.input}  ({before / 1024 / 1024:.1f} MB)")

    ffmpeg = find_ffmpeg()
    engine = opts.engine
    if engine == "auto":
        engine = "ffmpeg" if ffmpeg else ("moviepy" if _has_moviepy() else "none")

    try:
        if engine == "ffmpeg":
            if not ffmpeg:
                print("[ERROR] 没找到 ffmpeg，请先安装：pip install imageio-ffmpeg")
                return 3
            extract_with_ffmpeg(ffmpeg, opts)
        elif engine == "moviepy":
            extract_with_moviepy(opts)
        else:
            print("[ERROR] 既没有 ffmpeg 也没有 moviepy。二选一安装：")
            print("    pip install imageio-ffmpeg     # 最轻，自带 ffmpeg 可执行文件")
            print("    pip install moviepy            # 会用 ffmpeg 封装，体积大一些")
            return 3
    except Exception as exc:  # noqa: BLE001 - 给用户看的人话错误
        print(f"[ERROR] 转换失败：{exc}")
        return 1

    if not opts.output.exists() or opts.output.stat().st_size == 0:
        print("[ERROR] 输出文件没有生成。")
        return 1

    after = opts.output.stat().st_size
    print(f"[OK] 完成：{opts.output}")
    print(f"    体积 {after / 1024 / 1024:.2f} MB(原文件 {before / 1024 / 1024:.1f} MB，"
          f"缩小到 {after / before * 100:.1f}%）")
    minutes = after * 8 / 128_000 / 60
    print(f"    128 kbps 约等于每分钟 0.94 MB，这个文件大约 {minutes:.1f} 分钟")
    return 0


def _has_moviepy() -> bool:
    import importlib.util

    return importlib.util.find_spec("moviepy") is not None


if __name__ == "__main__":
    sys.exit(main())

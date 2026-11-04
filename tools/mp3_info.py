"""Read an MP3's frame headers to report bitrate mode and duration."""
from pathlib import Path

PATH = Path(r"D:\sunset.mp3")

BITRATES = {
    (1, 1): [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448],
    (1, 2): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
    (1, 3): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
    (2, 1): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256],
    (2, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
    (2, 3): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
}
SAMPLERATES = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}


def main() -> None:
    data = PATH.read_bytes()
    size = len(data)
    pos = 0
    if data[:3] == b"ID3":
        tag = ((data[6] & 0x7F) << 21) | ((data[7] & 0x7F) << 14) | ((data[8] & 0x7F) << 7) | (data[9] & 0x7F)
        pos = tag + 10
        print(f"ID3v2 tag: {tag + 10:,} bytes")

    frames = 0
    total_seconds = 0.0
    bitrates = {}
    first = None
    while pos + 4 < size:
        b = data[pos:pos + 4]
        if b[0] != 0xFF or (b[1] & 0xE0) != 0xE0:
            pos += 1
            continue
        ver_bits = (b[1] >> 3) & 0x03       # 3 = MPEG1, 2 = MPEG2, 0 = MPEG2.5
        layer_bits = (b[1] >> 1) & 0x03     # 1 = Layer III
        br_idx = (b[2] >> 4) & 0x0F
        sr_idx = (b[2] >> 2) & 0x03
        if br_idx in (0, 15) or sr_idx == 3 or layer_bits == 0 or ver_bits == 1:
            pos += 1
            continue
        version = 1 if ver_bits == 3 else 2
        layer = {1: 3, 2: 2, 3: 1}[layer_bits]
        sample_rate = SAMPLERATES[0 if ver_bits == 0 else ver_bits][sr_idx]
        bitrate = BITRATES[(version, layer)][br_idx] * 1000
        padding = (b[2] >> 1) & 0x01
        if layer == 1:
            frame_len = (12 * bitrate // sample_rate + padding) * 4
            samples = 384
        elif layer == 3 and version == 1:
            frame_len = 144 * bitrate // sample_rate + padding
            samples = 1152
        else:
            frame_len = 72 * bitrate // sample_rate + padding
            samples = 576
        if frame_len <= 4:
            pos += 1
            continue
        if first is None:
            first = (pos, bitrate, sample_rate, layer, version)
        bitrates[bitrate] = bitrates.get(bitrate, 0) + 1
        total_seconds += samples / sample_rate
        frames += 1
        pos += frame_len

    print(f"first frame at {first[0]:,}  {first[1] // 1000} kbps  {first[2]} Hz  layer {first[3]}")
    print(f"frames: {frames:,}   approx duration: {total_seconds / 60:.1f} min ({total_seconds:.0f} s)")
    print("bitrate histogram:", {f"{k // 1000}k": v for k, v in sorted(bitrates.items())})
    print(f"file: {size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()

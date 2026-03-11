import argparse
import csv
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    parser = argparse.ArgumentParser(description="Render lecture verification logs to PNG captures.")
    parser.add_argument("--summary", default="results/lecture-verification/summary.tsv")
    parser.add_argument("--logs", default="results/lecture-verification/logs")
    parser.add_argument("--out", default="results/lecture-verification/captures")
    parser.add_argument("--title-suffix", default="")
    args = parser.parse_args()

    base = Path("/work") if Path("/work").exists() else Path(".")
    summary_path = base / args.summary
    log_dir = base / args.logs
    out_dir = base / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    font = ImageFont.load_default()
    width, height = 1800, 1000
    bg = (13, 17, 23)
    fg = (231, 238, 247)
    muted = (151, 164, 182)
    accent_ok = (87, 242, 135)
    accent_fail = (255, 99, 132)

    with summary_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)

    suffix = f" ({args.title_suffix})" if args.title_suffix else ""

    for row in rows:
        lecture = row["lecture"]
        status = row["status"]
        recap = row["recap"]
        log_path = log_dir / f"{lecture}.log"

        lines = []
        if log_path.exists():
            content = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            lines = content[-26:]

        img = Image.new("RGB", (width, height), bg)
        draw = ImageDraw.Draw(img)

        draw.text((32, 28), f"{lecture} ansible-playbook 실행 캡처{suffix}", fill=fg, font=font)
        color = accent_ok if status == "PASS" else accent_fail
        draw.text((32, 56), f"status={status} | recap={recap}", fill=color, font=font)
        draw.text(
            (32, 92),
            "mcr docker capture solution: mcr.microsoft.com/devcontainers/python:3.12",
            fill=muted,
            font=font,
        )

        y = 130
        for src in lines:
            wrapped = textwrap.wrap(src, width=165) or [""]
            for line in wrapped:
                if y > height - 20:
                    break
                draw.text((32, y), line, fill=fg, font=font)
                y += 16
            if y > height - 20:
                break

        img.save(out_dir / f"{lecture}.png")

    print(f"generated={len(rows)}")


if __name__ == "__main__":
    main()

"""Generate predictions from saved ensemble models without report/delivery dependencies."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from src.ensemble import ROOT, configuration, predict


def main() -> None:
    parser = argparse.ArgumentParser(description="从保存的 XGBoost 秩集成模型生成预测")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--model-dir", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/predictions.csv")
    parser.add_argument("--threads", type=int, default=16)
    args = parser.parse_args()
    if args.threads < 1:
        parser.error("--threads 必须大于零")
    print(json.dumps(predict(configuration(args.config), args.output, args.threads, args.model_dir),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

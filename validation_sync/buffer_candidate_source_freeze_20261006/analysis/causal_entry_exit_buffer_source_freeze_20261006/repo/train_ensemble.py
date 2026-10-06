"""Fit the recorded sixteen-seed recipe; saved models are reused unless --retrain is set."""
from __future__ import annotations
import argparse
from pathlib import Path
from src.ensemble import configuration, train


def main() -> None:
    parser = argparse.ArgumentParser(description="训练 67 特征、16 随机种子的 XGBoost 排序集成")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--retrain", action="store_true", help="重新训练并替换本地模型文件")
    args = parser.parse_args()
    if args.threads < 1:
        parser.error("--threads 必须大于零")
    train(configuration(args.config), args.threads, args.device, args.retrain)


if __name__ == "__main__":
    main()

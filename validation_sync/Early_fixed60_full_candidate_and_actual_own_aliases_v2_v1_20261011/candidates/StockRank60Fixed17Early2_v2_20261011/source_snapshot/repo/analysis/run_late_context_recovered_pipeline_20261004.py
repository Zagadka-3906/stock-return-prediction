"""Versioned constructor recovery composed with earlier future-only repairs."""
from pathlib import Path
import importlib
import sys
import traceback
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def main(number):
    from late_context_initialization_recovery_20261004 import install
    install(number,bind=True)
    pipeline=importlib.import_module(f'run_training_round{number}_pipeline')
    try:
        if number in (36,38,40):
            from run_future_inference_recovered_pipeline_20261004 import main as future_main
            future_main(number)
        else:pipeline.main()
    except Exception:
        pipeline.state('failed','failed',{'traceback':traceback.format_exc()});raise


if __name__=='__main__':main(int(sys.argv[1]))

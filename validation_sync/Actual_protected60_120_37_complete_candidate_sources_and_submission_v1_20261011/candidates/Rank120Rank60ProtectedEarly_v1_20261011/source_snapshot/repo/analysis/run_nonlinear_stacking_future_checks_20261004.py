"""Warm final training artifacts then verify future implementation without labels."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]


if __name__=='__main__':
    for script in ('warm_nonlinear_stacking_fulltraining_20261004.py','verify_nonlinear_stacking_future_pipelines_20261004.py'):
        subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/'analysis'/script)],cwd=ROOT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)

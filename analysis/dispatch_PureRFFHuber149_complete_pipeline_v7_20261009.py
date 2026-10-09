from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from bind_Pure149_all5_annual_native_v8_20261009 import execute
if __name__=='__main__':execute('dispatch_PureRFFHuber149_complete_pipeline_v4_20261008.py')

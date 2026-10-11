from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
s=(A/'bind_Pure149_all5_annual_native_v8_20261009.py').read_text(encoding='utf8').replace('PureRFFHuber80_native_historical_calendar_controls_v4_20261009','PureRFFHuber80_native_historical_calendar_controls_v6_20261009').replace('PureRFFHuber20_year2023_native_supplement_v1_20261009','PureRFFHuber20_year2023_native_supplement_v2_20261009')
ns={'__file__':str(A/'bind_Pure149_all5_annual_native_v8_20261009.py'),'__name__':'verified_annual_coverage_service_binding'}
exec(compile(s,str(A/'bind_Pure149_all5_annual_native_v8_20261009.py'),'exec'),ns)
if __name__=='__main__':ns['verify_coverage']()

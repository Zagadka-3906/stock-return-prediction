"""Actual tied-forecast rank/CDF controls and static44-score route preflight."""
from pathlib import Path
import ast
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import numpy as np
    from scipy.stats import rankdata
    from full_universe_HGB_percentile_CDF_transform_20261007 import centered_daily_forecast,prepare,apply_prepared,transform
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'full_universe_HGB44_transform_route_preflight_20261007';assert not out.exists();out.mkdir()
    sources=[Path(__file__),A/'full_universe_HGB_percentile_CDF_transform_20261007.py',A/'direct_flag_centered_rank_CDF_transform_20261007.py',A/'run_full_universe_HGB44_official_comparison_20261007.py',A/'cpu_full_universe_HGB_bank24_plan_20261007.json',ROOT/'后续选模标准.md']
    pins={str(p.resolve()):sha(p) for p in sources};create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'new_fits':0,'new_official_scores':0,'candidate_inference':False})
    with LockedReadHashCache(pins) as scope:
        raw=np.tile(np.array([0.,0.,6.,12.,18.,24.]),3);forecast=np.tile(np.array([4.,4.,2.,0.,1.,3.]),3)
        dates=np.repeat([20200102,20200103,20200106],6);flags=np.tile([1,0,0,1,0,0],3);valid=np.ones(18,dtype=bool)
        centered=centered_daily_forecast(forecast,dates);expected=np.tile(rankdata(forecast[:6],method='average')/6.-.5,3)
        assert np.array_equal(centered.view('u8'),expected.view('u8'))
        assert np.array_equal(centered.view('u8'),centered_daily_forecast(forecast*128.+256.,dates).view('u8'))
        prepared=prepare(raw,dates,flags,valid,'all_current_raw_forecasts');assert all(len(r[1])==6 for r in prepared)
        assert np.array_equal(apply_prepared(raw,centered,0.,prepared).view('u8'),raw.view('u8'))
        controls=[]
        for weight in read(A/'cpu_full_universe_HGB_bank24_plan_20261007.json')['planned_official_comparison']['weights']:
            actual=apply_prepared(raw,centered,weight,prepared);reference=[]
            for day in range(3):
                pool=sorted(raw[day*6:(day+1)*6]);parent=rankdata(raw[day*6:(day+1)*6],method='average')/6.
                for i in range(6):
                    q=min(1.,max(1./6.,(1.-weight)*parent[i]+weight*(expected[day*6+i]+.5)))
                    location=q*6.-1.;left=min(5,max(0,int(np.floor(location))));right=min(5,left+1);fraction=location-left
                    reference.append(pool[left]+fraction*(pool[right]-pool[left]))
            assert np.allclose(actual,np.asarray(reference),rtol=0.,atol=1e-12)
            for n in (6,12,18):
                cold_centered=centered_daily_forecast(forecast[:n],dates[:n]);cold=transform(raw[:n],dates[:n],flags[:n],valid[:n],cold_centered,weight,'all_current_raw_forecasts')
                assert np.array_equal(cold.view('u8'),actual[:n].view('u8'))
            poison=forecast.copy();poison[12:]=1e12-np.arange(6)
            changed=transform(raw,dates,flags,valid,centered_daily_forecast(poison,dates),weight,'all_current_raw_forecasts')
            assert np.array_equal(changed[:12].view('u8'),actual[:12].view('u8'))
            controls.append({'weight':weight,'independent_scalar_interpolation_within1e-12':True,'current_day_tied_rank_bits_exact':True,'future_day_poisoning_and_three_complete_day_prefix_bits_exact':True})
        text=(A/'run_full_universe_HGB44_official_comparison_20261007.py').read_text(encoding='utf-8');ast.parse(text)
        assert "assert len(cases) == 44" in text and "== 24" in text
        assert "CPU_HGB44_round112_full_registration" in text and "['actual_full_QA_version'] == 23" in text
        assert "raw_oof_predictions.npy" in text and "all44_final_past_return_mapped_CSVs_original_official_scored" in text
        assert 'first2020_raw_bits_identity' not in text and 'identity2020 =' not in text
        assert 'all1212_nonflag_raw_bits_exact_implies_same_orders_and_ties' not in text
        scope.reverify();create(out/'verification.json',{'status':'passed_actual_synthetic_full_universe_tie_CDF_prefix_future_poisoning_and_prospective44_route_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'controls':controls,'actual_synthetic_weights':6,'prospective_bank_models':24,'prospective_official_cases':44,'full5635800_actual_model_scoring_not_executed':True,'new_fits':0,'new_quality_scores':0,'future_candidate_inference_not_executed':True,'test_labels_read':False})
if __name__=='__main__':main()

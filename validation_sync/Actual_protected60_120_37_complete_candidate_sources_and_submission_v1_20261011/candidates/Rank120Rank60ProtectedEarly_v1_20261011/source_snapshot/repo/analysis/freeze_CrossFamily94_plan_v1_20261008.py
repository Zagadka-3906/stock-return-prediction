"""Freeze a finite new ensemble grid before quality scores or future inference."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'; sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from CrossFamily_complete_parent_CDF_v1_20261008 import GROUPS,HEADS


def main():
    bank_specs = {
        'bayes_scalar': ('nonflag_residual_EmpiricalBayes64_bank10_20261007', 'nonflag_residual_empirical_bayes64_scalar', 'linear'),
        'bayes_diagonal': ('nonflag_residual_EmpiricalBayes64_bank10_20261007', 'nonflag_residual_empirical_bayes64_diagonal', 'linear'),
        'ridge_l001': ('nonflag_residual_Ridge_bank10_20261007', 'nonflag_residual_ridge_l001', 'linear'),
        'ridge_l025': ('nonflag_residual_Ridge_bank10_20261007', 'nonflag_residual_ridge_l025', 'linear'),
        'rff_g00625': ('nonflag_residual_RFF128StreamMid_bank10_20261007', 'nonflag_residual_rff128streammid_g00625', 'random_fourier_linear'),
        'rff_g0125': ('nonflag_residual_RFF128StreamMid_bank10_20261007', 'nonflag_residual_rff128streammid_g0125', 'random_fourier_linear'),
    }
    pins = {}; records = {}
    def pin(path, expected=None):
        path=Path(path); digest=sha(path)
        assert expected is None or digest==expected,str(path)
        assert str(path) not in pins or pins[str(path)]==digest
        pins[str(path)] = digest
    for bank in dict.fromkeys(row[0] for row in bank_specs.values()):
        path=A/bank/'verification.json'; proof=read(path)
        assert proof['status'].startswith('passed_actual10_') and proof['actual_native_fits']==10
        pin(path)
        # Merge immutable existing source/data pins; the bank audit will rehash every file.
        for path,digest in proof['input_sha256'].items():
            assert Path(path).is_file(),path
            assert path not in pins or pins[path]==digest,path
            pins[path]=digest
    for head,(bank,name,kind) in bank_specs.items():
        folder=A/bank/name; infos={}
        for year in range(2021,2026):
            path=folder/f'info_{year}.json'; info=read(path); pin(path)
            assert info['name']==name and info['year']==year
            assert info['last_training_label_date']<info['exclusive_cutoff'] and info['last_training_label_end']<=info['exclusive_cutoff']
            pin(info['native_model_path'],info['native_model_sha256'])
            key='independent_'+kind+'_state'
            pin(info[key+'_path'],info[key+'_sha256'])
            infos[str(year)]=str(path)
        op=folder/'oof_verification.json'; proof=read(op); pin(op)
        array=folder/'nonflag_oof_predictions.npy'; pin(array,proof['prediction_array_sha256'])
        assert proof['rows']==5635800 and proof['flagged_and2020_zero_residual']
        records[head]={'folder':str(folder),'state_kind':kind,'infos':infos,'oof':str(array)}
    for path in (Path(__file__),A/'CrossFamily_complete_parent_CDF_v1_20261008.py',A/'verify_CrossFamily_bank30_and_synthetic_v1_20261008.py',
                 A/'nonflag_residual_Ridge_codec_20261007.py',A/'nonflag_empirical_Bayes64_codec_20261007.py',A/'nonflag_residual_RFF128_codec_20261007.py',
                 A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'connected_validation_20261002/combined_fold_frame.parquet',
                 A/'optimization_20261003_r106/selected_validation.npy',A/'nonflag_residual_HGB_bank10_20261007/actual_teacher_target_and_key_alignment.json',
                 ROOT/'evaluate.py',A/'github_validation_sync_main_20261005/round134_receipt.json'):
        pin(path)
    cases=[{'group':g,'share':s,'amplitude':a} for g in range(5) for s in (.25,.5,.75) for a in (.0025,.005,.01,.025,.05,.1)]
    create(A/'CrossFamily94_round136_plan_v1_20261008.json',{
        'status':'frozen_finite94_grid_before_new_quality_and_future_inference','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'target_round':136,'heads':records,'ordered_groups':GROUPS,'new_cases':cases,'new_case_count':90,
        'anchor_rounds':[112,134,135],'anchor_count':3,'zero_amplitude_identity_count':1,'expected_scored_cases':94,
        'parent_selection':'highest actually fully qualified official score among112,134,135; ties use fewer physical model heads then earlier round',
        'parent_frozen_only_after_round135_full_QA_and_actual_main_receipt':True,
        'position':'after ALL branches of the complete chosen parent including BF16 if present',
        'rank_and_inverse_CDF_universe':'all current raw parent forecasts including invalid sentinels',
        'eligible_application':'valid nonflag stocks in2021 onwards;2020,flag1 and invalid rows remain bit-identical',
        'teacher_feature':'original qualified106 current-day forecast average rank over N; frozen own-window feature64',
        'arithmetic':'ordered mean within component group; sign; share; ordered two-group addition; then amplitude and complete-parent CDF',
        'CPU_threads':2,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False,
        'complete136_sources_admission_required_before_first_quality_score':True,'input_sha256':pins,
        'finite_grid_does_not_prove_global_optimization_exhaustion':True})
    print('Frozen90 new nested mixtures plus3 anchors and1 exact identity; no quality score.',flush=True)


if __name__=='__main__': main()

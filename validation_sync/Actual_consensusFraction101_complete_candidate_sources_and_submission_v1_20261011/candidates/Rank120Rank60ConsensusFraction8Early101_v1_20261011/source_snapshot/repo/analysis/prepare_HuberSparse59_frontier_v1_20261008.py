"""Freeze a bounded new ensemble proposal and verify its actual saved-state metadata and synthetic causality."""
from pathlib import Path
import ast
import copy
import hashlib
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save


def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape
    assert np.array_equal(a.view('u8'),b.view('u8'))


def main():
    import numpy as np
    import HuberSparse_complete_parent_CDF_v1_20261008 as codec
    from run import fold_cutoff
    proposal=A/'HuberSparse59_round150_proposal_v1_20261008.json'
    assert not proposal.exists()
    source_plan=A/'HuberCrossFamily112_round139_plan_v1_20261008.json'
    existing=read(source_plan)
    heads={h:copy.deepcopy(existing['heads'][h]) for h in ('huber_d010','huber_d025')}
    bank=A/'nonflag_residual_SparseGram64_bank10_20261007'
    sparse_proof=read(bank/'verification.json')
    assert sparse_proof['actual_native_fits']==10 and sparse_proof['status'].startswith('passed_actual10_')
    for short,name in [('sparse_l1','nonflag_residual_sparseGram64_L1'),('sparse_elastic','nonflag_residual_sparseGram64_Elastic')]:
        folder=bank/name
        heads[short]={'folder':str(folder),'oof':str(folder/'nonflag_oof_predictions.npy'),
            'infos':{str(y):str(folder/f'info_{y}.json') for y in range(2021,2026)},
            'state_kind':'linear','native_stage_state_kind':'SparseGram64_linear'}
    cases=[{'group':0,'share':.5,'amplitude':0.}]
    cases += [{'group':g,'share':s,'amplitude':a} for g in range(6) for s in (.25,.5,.75) for a in (.001,.0025,.00325)]
    assert len(cases)==55
    original=A/'HuberCrossFamily_complete_parent_native_stage_v1_20261008.py'
    source=original.read_text(encoding='utf8')
    source=source.replace('HuberCrossFamily_complete_parent_CDF_v1_20261008','HuberSparse_complete_parent_CDF_v1_20261008')
    source=source.replace("GRAPH_KEY='nonflag_CPU_HuberCrossFamily_complete_parent_CDF'","GRAPH_KEY='nonflag_CPU_HuberSparse_complete_parent_CDF'")
    source=source.replace('    from nonflag_residual_Ridge_codec_20261007 import predict_native as lin_native,predict_decoded as lin_decoded\n','')
    source=source.replace('    from nonflag_residual_RFF128_codec_20261007 import predict_native as rff_native,predict_decoded as rff_decoded\n',
        '    from nonflag_sparse_Gram64_codec_20261007 import predict_native as sparse_native,predict_decoded as sparse_decoded\n')
    old="native,decoded=(huber_native,huber_decoded) if kind=='HuberIRLS64_linear' else ((rff_native,rff_decoded) if kind=='random_fourier_linear' else (lin_native,lin_decoded))"
    assert source.count(old)==1
    source=source.replace(old,"native,decoded=(huber_native,huber_decoded) if kind=='HuberIRLS64_linear' else (sparse_native,sparse_decoded)")
    source=source.replace("assert kind in ('linear','random_fourier_linear','HuberIRLS64_linear')","assert kind in ('HuberIRLS64_linear','SparseGram64_linear')")
    start=source.index("            elif head.startswith('ridge_'):")
    end=source.index('            values=np.zeros',start)
    source=source[:start]+"""            else:
                assert head in ('sparse_l1','sparse_elastic') and kind=='SparseGram64_linear'
                assert bundle['model'].get_params()==info['parameters']
                assert info['parameters']['solver']=='own_centered_Gram64_cyclic_coordinate_descent'
                assert state['kind']=='nonflag_residual_SparseGram64'
                assert bundle['model'].alpha_==info['parameters']['alpha']
"""+source[end:]
    native=save('HuberSparse_complete_parent_native_stage_v1_20261008.py',source)
    dependencies=[Path(__file__),Path(codec.__file__),A/'HuberCrossFamily_complete_parent_CDF_v1_20261008.py',original,native,
        source_plan,bank/'verification.json',A/'nonflag_residual_SparseGram6410_plan_20261007.json',
        A/'nonflag_sparse_Gram64_codec_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py',
        A/'nonflag_HuberIRLS64_streamed_v1_20261008.py',ROOT/'run.py',ROOT/'后续选模标准.md']
    metadata=[]
    for year in range(2021,2026):
        reference=None
        for head,row in heads.items():
            path=Path(row['infos'][str(year)]);info=read(path)
            assert info['year']==year and info['exclusive_cutoff']==fold_cutoff(year)
            assert info['last_training_label_date']<info['exclusive_cutoff']
            assert info['last_training_label_end']<=info['exclusive_cutoff']
            own={k:info[k] for k in ('features','training_rows','exclusive_cutoff','last_training_label_date','last_training_label_end','training_matrix_numeric_sha256','training_target_numeric_sha256')}
            if reference is None:reference=own
            assert own==reference,(head,year)
            state=Path(info['independent_linear_state_path'])
            model=Path(info['native_model_path'])
            assert sha(model)==info['native_model_sha256']
            assert sha(state)==info['independent_linear_state_sha256']
            dependencies.extend([path,model,state])
            metadata.append({'head':head,'year':year,'native_sha256':info['native_model_sha256'],
                'independent_sha256':info['independent_linear_state_sha256'],'native_kind':row['native_stage_state_kind'],
                'storage_kind':row['state_kind'],'own_past_mature_window_metadata_exact':True})
    for row in heads.values():
        folder=Path(row['folder']);oof=Path(row['oof'])
        assert oof.is_file() and (folder/'oof_verification.json').is_file()
        dependencies.extend([oof,folder/'oof_verification.json'])
    pins={str(p):sha(p) for p in dict.fromkeys(dependencies)}
    create(proposal,{'status':'frozen59_proposal_before_training_only_controls_not_admitted_or_scored',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'target_round':150,'after_round':149,
        'fixed_scientific_stage_base_round':134,'anchor_rounds':[146,147,148,149],
        'heads':heads,'groups':codec.GROUPS,'new_cases':cases,'expected_new_full_cases':55,
        'expected_cold_cases':165,'expected_official_cases':59,'teacher_round':106,
        'mixture_operation_order':'within-family ordered mean, sign, Huber share, sparse1-share, ordered sum',
        'input_sha256':pins,'existing_annual_states':20,'new_native_fits':0,
        'physical_models_per_nonidentity_case':{'single_sparse':3,'equal_mean_sparse':4},
        'positive_and_negative_sparse_directions_declared_before_any_quality':True,
        'selection':'highest_complete_connected2020_2024_official_score_then_physical_model_count_then_abs_weight_then_case',
        'selection_bias_uncorrected':True,'test_labels_read':False,
        'requirements_before_official_scoring':['actual20_state_rehash_and_new_native_reload_independent_decoders',
            'historical_own_year_and_frozen2025_two_calendar_and_cold80_controls',
            'full5635800_all55_and165_prefix_numeric_controls_and_actual_duplicate_audit',
            'own_D_scoring_scope_and_source_freeze_and_all59_complete_receivers_prospective_routes',
            'actual149_full_qualification_and_controls_main_receipt'],
        'requirements_before_adoption':['selected_scheme_freeze_before_futureX','two1599600_native_reload_independent_and_CSV_replays',
            'cold80_check','all_original_six_full_board_views_and_candidate_QA','main_receipt'],
        'coverage_claim':'new_mix_is_absent_from_current_explicit_plan_and_proposal_names; full_forecast_duplicate_audit_still_required',
        'global_optimization_or_compute_boundary_proven':False})
    rng=np.random.default_rng(15020261008)
    days=np.array([20201230,20210104,20210402,20211230,20240102,20241230,20250102,20260102],dtype=np.int64)
    dates=np.repeat(days,41);parent=np.round(rng.normal(size=len(dates)),1).astype(np.float64)
    parent[0]=-0.;flags=rng.integers(0,2,len(dates));valid=rng.random(len(dates))>.2
    raw={h:rng.normal(size=len(dates)).astype(np.float64) for h in codec.HEADS}
    records=[]
    for index,case in enumerate(cases):
        residual=codec.mixture(raw,case['group'],case['share'])
        exact(residual,codec.independent_mixture(raw,case['group'],case['share']))
        values=codec.transform(parent,residual,dates,flags,valid,case['amplitude'])
        exact(values,codec.pandas_oracle(parent,residual,dates,flags,valid,case['amplitude']))
        untouched=(dates<20210101)|(flags==1)|~valid
        exact(values[untouched],parent[untouched])
        cold=[]
        for n in (82,164,246):
            exact(values[:n],codec.transform(parent[:n],residual[:n],dates[:n],flags[:n],valid[:n],case['amplitude']))
            cold.append(n)
        changed={h:x.copy() for h,x in raw.items()}
        for x in changed.values():x[dates>=20250101]*=17.
        altered=codec.transform(parent,codec.mixture(changed,case['group'],case['share']),dates,flags,valid,case['amplitude'])
        exact(values[dates<20250101],altered[dates<20250101])
        records.append({'case':index,'configuration':case,'primary_independent_and_Pandas_bits_exact':True,
            'first2020_flag1_invalid_raw_bits_preserved':True,'cold_prefix_rows':cold,
            'future_residual_perturbation_does_not_change_past':True,
            'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()})
    proof=A/'HuberSparse59_synthetic55_and_state20_metadata_v1_20261008.json'
    create(proof,{'status':'passed_actual55_synthetic165_prefix_and_future_perturbation_controls_and20_saved_state_metadata',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{**pins,str(proposal):sha(proposal)},
        'records':records,'existing_state_metadata':metadata,'actual_cases':55,'actual_cold_cases':165,
        'actual_saved_state_metadata_count':20,'new_native_replays_claimed':False,
        'actual_historical5635800_full_controls_not_yet_prepared':True,
        'actual59_quality_receivers_not_yet_prepared':True,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'status':'HuberSparse59_proposal_frozen_and55_synthetic165_prefix20_state_metadata_passed','new_native_fits':0},flush=True)


if __name__=='__main__':main()

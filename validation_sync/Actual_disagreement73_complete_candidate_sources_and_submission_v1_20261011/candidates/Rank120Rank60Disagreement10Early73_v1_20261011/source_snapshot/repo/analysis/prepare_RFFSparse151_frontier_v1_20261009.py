"""Freeze an additional RFF plus sparse residual ensemble before any151 quality score."""
from pathlib import Path
import sys,copy,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def exact(a,b):
    import numpy as np
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape and np.array_equal(a.view('u8'),b.view('u8'))

def main():
    import numpy as np
    from run import fold_cutoff
    proposal=A/'RFFSparse59_round151_proposal_v1_20261009.json';assert not proposal.exists()
    original=A/'HuberSparse_complete_parent_CDF_v1_20261008.py'
    source=original.read_text(encoding='utf8').replace('Huber','RFF').replace('huber_d010','rff_g00625').replace('huber_d025','rff_g0125')
    codec_path=save('RFFSparse_complete_parent_CDF_v1_20261009.py',source)
    import RFFSparse_complete_parent_CDF_v1_20261009 as codec
    native_original=A/'HuberSparse_complete_parent_native_stage_v1_20261008.py'
    source=native_original.read_text(encoding='utf8').replace('HuberSparse_complete_parent_CDF_v1_20261008','RFFSparse_complete_parent_CDF_v1_20261009').replace('nonflag_CPU_HuberSparse_complete_parent_CDF','nonflag_CPU_RFFSparse_complete_parent_CDF')
    source=source.replace('    from nonflag_HuberIRLS64_streamed_v1_20261008 import CONFIGS,predict_native as huber_native,predict_decoded as huber_decoded',
        '    from nonflag_residual_RFF128_codec_20261007 import predict_native as rff_native,predict_decoded as rff_decoded')
    source=source.replace("(huber_native,huber_decoded) if kind=='HuberIRLS64_linear'","(rff_native,rff_decoded) if kind=='random_fourier_linear'")
    source=source.replace("('HuberIRLS64_linear','SparseGram64_linear')","('random_fourier_linear','SparseGram64_linear')")
    start=source.index("            if head.startswith('huber_'):");end=source.index('            else:',start)
    source=source[:start]+"""            if head.startswith('rff_'):
                assert kind=='random_fourier_linear' and state['kind']=='nonflag_residual_RFF128'
                projection=bundle['model'].named_steps['rbf'];linear=bundle['model'].named_steps['ridge']
                assert projection.gamma==info['parameters']['gamma'] and projection.n_components==128
                assert linear.alpha==info['parameters']['alpha']
                assert projection.random_state==info['parameters']['random_state'] and linear.solver=='cholesky'
"""+source[end:]
    native_path=save('RFFSparse_complete_parent_native_stage_v1_20261009.py',source)
    rff_path=A/'CrossFamilyFine125_round145_plan_v2_20261008.json';rff=read(rff_path)
    sparse_path=A/'HuberSparse59_round150_proposal_v1_20261008.json';sparse=read(sparse_path)
    heads={h:copy.deepcopy(rff['heads'][h]) for h in ('rff_g00625','rff_g0125')}
    heads.update({h:copy.deepcopy(sparse['heads'][h]) for h in ('sparse_l1','sparse_elastic')})
    cases=[{'group':0,'share':.5,'amplitude':0.}]+[{'group':g,'share':s,'amplitude':v} for g in range(6) for s in (.25,.5,.75) for v in (.001,.0025,.00325)]
    assert len(cases)==55
    inputs=[Path(__file__),original,codec_path,native_original,native_path,rff_path,sparse_path,ROOT/'run.py',ROOT/'后续选模标准.md',
        A/'nonflag_residual_RFF128_codec_20261007.py',A/'nonflag_sparse_Gram64_codec_20261007.py']
    metadata=[]
    for year in range(2021,2026):
        reference=None
        for head,row in heads.items():
            info_path=Path(row['infos'][str(year)]);info=read(info_path)
            assert info['year']==year and info['exclusive_cutoff']==fold_cutoff(year)
            assert info['last_training_label_date']<info['exclusive_cutoff'] and info['last_training_label_end']<=info['exclusive_cutoff']
            own={k:info[k] for k in ('features','training_rows','exclusive_cutoff','last_training_label_date','last_training_label_end','training_matrix_numeric_sha256','training_target_numeric_sha256')}
            if reference is None:reference=own
            assert reference==own,(head,year)
            kind=row['state_kind'];state=Path(info['independent_'+kind+'_state_path']);model=Path(info['native_model_path'])
            assert sha(model)==info['native_model_sha256'] and sha(state)==info['independent_'+kind+'_state_sha256']
            inputs.extend([info_path,state,model]);metadata.append({'head':head,'year':year,'native_sha256':info['native_model_sha256'],'independent_sha256':sha(state),'storage_kind':kind,'native_kind':row['native_stage_state_kind'],'own_mature_past_window_metadata_exact':True})
    for row in heads.values():inputs.extend([Path(row['oof']),Path(row['folder'])/'oof_verification.json'])
    for p in inputs:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    pins={str(p):sha(p) for p in dict.fromkeys(inputs)}
    create(proposal,{'status':'frozen59_RFFSparse_proposal_before_training_only_controls_not_quality_admitted','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'target_round':151,'after_round':150,'fixed_scientific_stage_base_round':134,'anchor_rounds':[147,148,149,150],'heads':heads,'groups':codec.GROUPS,
        'new_cases':cases,'expected_new_full_cases':55,'expected_cold_cases':165,'expected_official_cases':59,'teacher_round':106,'input_sha256':pins,
        'mixture_operation_order':'RFF ordered equal mean, signed sparse mean, RFF share, sparse one-minus-share, ordered sum',
        'existing_annual_states':20,'new_native_fits':0,'physical_models_per_nonidentity_case':{'single_sparse':3,'equal_mean_sparse':4},
        'selection':'highest_complete_connected2020_2024_official_score_then_physical_model_count_then_abs_weight_then_case','selection_bias_uncorrected':True,'test_labels_read':False,
        'coverage_claim':'new explicit RFFSparse mixtures; actual prior complete forecast duplicate audit required before quality',
        'requires_actual20_native_replay_and72_calendar_cold_controls_and55_full165_cold_controls':True,
        'requires32_complete_receivers_and_actual150_qualification_before59_official_scores':True,
        'requires_selected_source_freeze_before_futureX_two_full_native_independent_CSV_and_cold80_QA62_and_main_before_adoption':True,
        'global_optimization_or_compute_boundary_proven':False})
    rng=np.random.default_rng(15120261009);dates=np.repeat(np.array([20201230,20210104,20210402,20211230,20240102,20241230,20250102,20260102]),41)
    parent=np.round(rng.normal(size=len(dates)),1).astype(np.float64);parent[0]=-0.;flags=rng.integers(0,2,len(dates));valid=rng.random(len(dates))>.2
    raw={h:rng.normal(size=len(dates)).astype(np.float64) for h in codec.HEADS};records=[]
    for case,cfg in enumerate(cases):
        residual=codec.mixture(raw,cfg['group'],cfg['share']);exact(residual,codec.independent_mixture(raw,cfg['group'],cfg['share']))
        values=codec.transform(parent,residual,dates,flags,valid,cfg['amplitude']);exact(values,codec.pandas_oracle(parent,residual,dates,flags,valid,cfg['amplitude']))
        preserved=(dates<20210101)|(flags==1)|~valid;exact(values[preserved],parent[preserved])
        for n in (82,164,246):exact(values[:n],codec.transform(parent[:n],residual[:n],dates[:n],flags[:n],valid[:n],cfg['amplitude']))
        altered={h:x.copy() for h,x in raw.items()}
        for x in altered.values():x[dates>=20250101]*=17.
        changed=codec.transform(parent,codec.mixture(altered,cfg['group'],cfg['share']),dates,flags,valid,cfg['amplitude']);exact(values[dates<20250101],changed[dates<20250101])
        records.append({'case':case,'configuration':cfg,'independent_mixture_and_Pandas_CDF_bits_exact':True,'preserved2020_flag1_invalid_bits_exact':True,'cold_prefix_rows':[82,164,246],'future_perturbation_does_not_change_past':True,'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()})
    create(A/'RFFSparse59_synthetic55_and_state20_metadata_v1_20261009.json',{'status':'passed_actual55_synthetic165_prefix_future_perturbation_and20_saved_state_metadata',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{**pins,str(proposal):sha(proposal)},'records':records,'existing_state_metadata':metadata,
        'actual_cases':55,'actual_cold_cases':165,'actual_saved_state_metadata_count':20,'new_native_replays_claimed':False,
        'native72_and_full55_receivers_and_all59_quality_receivers_still_required':True,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'proposal':151,'synthetic':55,'prefix':165,'saved_metadata':20,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()

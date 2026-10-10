"""Bind the bounded52-case plan to the actual10-model bank and exact saved per-year states."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    from HuberIRLS64_complete_parent_CDF_v1_20261008 import HEADS
    plan_path=A/'HuberIRLS64_52_round137_plan_v2_20261008.json';plan=read(plan_path)
    assert plan['total_cases']==52 and len(plan['new_cases'])==48 and plan['anchors']==[134,135,136]
    pointer_path=A/'actual_nonflag_HuberIRLS64_bank10_location_v1_20261008.json';pointer=read(pointer_path);bank=Path(pointer['output'])
    proof_path=bank/'verification.json';proof=read(proof_path);assert sha(proof_path)==pointer['verification_sha256']
    assert proof['actual_native_fits']==10 and proof['actual_full_OOF_heads']==2 and proof['actual_official_scores']==0
    names=('nonflag_residual_huberIRLS64_d010','nonflag_residual_huberIRLS64_d025');heads={}
    paths=[Path(__file__),plan_path,pointer_path,proof_path,A/'Huber52_complete_parent_receiver_codec_v1_20261008.py',
        A/'HuberIRLS64_complete_parent_CDF_v1_20261008.py',A/'HuberIRLS64_complete_parent_native_stage_v2_20261008.py',
        A/'predict_HuberIRLS64_complete_parent_scheme_v2_20261008.py',A/'HuberIRLS64_bounded_plan_recheck_v2_20261008.json']
    for head,name in zip(HEADS,names):
        folder=bank/name;infos={str(year):str(folder/f'info_{year}.json') for year in range(2021,2026)}
        for year,path in infos.items():
            info=read(path);assert info['name']==name and info['year']==int(year)
            assert info['last_training_label_date']<info['exclusive_cutoff'] and info['last_training_label_end']<=info['exclusive_cutoff']
            assert sha(info['native_model_path'])==info['native_model_sha256'] and sha(info['independent_linear_state_path'])==info['independent_linear_state_sha256']
            paths += [Path(path),Path(info['native_model_path']),Path(info['independent_linear_state_path'])]
        oof=read(folder/'oof_verification.json');assert sha(folder/'nonflag_oof_predictions.npy')==oof['prediction_array_sha256']
        paths += [folder/'oof_verification.json',folder/'nonflag_oof_predictions.npy']
        heads[head]={'folder':str(folder),'oof':str(folder/'nonflag_oof_predictions.npy'),'infos':infos,
            'state_kind':'linear','native_stage_state_kind':'HuberIRLS64_linear'}
    create(A/'Huber52_round137_receiver_contract_v1_20261008.json',{'status':'bound_actual10_Huber_native_models_to_bounded52_case_receiver_contract',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(path):sha(path) for path in dict.fromkeys(paths)},
        'frozen_scientific_plan':str(plan_path),'frozen_scientific_plan_sha256':sha(plan_path),'anchor_rounds':plan['anchors'],
        'new_cases':[{**case,'share':.5} for case in plan['new_cases']],'expected_scored_cases':52,'new_case_count':48,
        'heads':heads,'fixed_share_is_unused_schema_field_not_extra_configuration':True,'actual_native_models':10,
        'maximum_amplitude':.1,'actual_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()

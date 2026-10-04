"""Create isolated sampling/audit/dispatch helpers; preserve every old frozen source."""
from pathlib import Path
import ast
import hashlib
import json
import time
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    pairs=[(f'{prefix}_neural_width_{suffix}_20261004.py',f'{prefix}_nystrom_ridge_{suffix}_20261004.py')
        for prefix,suffix in (('observe','resources'),('audit','resource_scope'),('audit','future_resources'),('run','evidence_audits'))]
    pairs += [('run_new_neural_families_locked_pipeline_20261004.py','run_nystrom_ridge_locked_pipeline_20261004.py'),
        ('verify_new_neural_families_frozen_provenance_20261004.py','verify_nystrom_ridge_frozen_provenance_20261004.py')]
    old={str((HERE/a).resolve()):sha(HERE/a) for a,b in pairs};new={}
    for original,target in pairs:
        path=HERE/target;assert not path.exists(),path
        text=(HERE/original).read_text(encoding='utf-8-sig')
        text=text.replace('neural_width','nystrom_ridge').replace('new_neural_families','nystrom_ridge')
        text=text.replace('(57,58,59,60)','(61,62)')
        if target.startswith('run_nystrom_ridge_locked'):
            before="def family(number):return 'nystrom_ridge' if number in (57,58) else 'portfolio_surrogate'"
            assert before in text;text=text.replace(before,"def family(number):return 'nystrom_ridge'")
            text=text.replace('R57/R58/R59/R60','R61/R62')
        if target.startswith('verify_nystrom_ridge_frozen'):
            text=text.replace("ROOT/'analysis/run_nystrom_ridge_round_pipeline_20261004.py',ROOT/'analysis/run_portfolio_surrogate_round_pipeline_20261004.py'","ROOT/'analysis/run_nystrom_ridge_round_pipeline_20261004.py'")
        text=text.replace('matched wide neural training','past-fold Nyström training')
        text=text.replace('Samples after start only;','Samples include the serialized resource-control wait and actual CPU fitting after start;')
        text=text.replace("'chosen_available_reserve_GiB':8.","'chosen_available_reserve_GiB':14.")
        text=text.replace('chosen8GiB_reserve','chosen14GiB_reserve').replace('12GiB_start_reserve','14GiB_start_reserve')
        text=text.replace('finite_width_grid_does_not_exhaust_neural_model_space','finite_landmark_grid_does_not_exhaust_kernel_model_space')
        if target.startswith('observe_'):
            anchor="'actual_spawned_official_workers':nworkers,'actual_completed_annual_fits':annual,'gpu_last_sample':gpu_value}"
            assert anchor in text
            text=text.replace(anchor,"'actual_spawned_official_workers':nworkers,'actual_completed_annual_fits':annual,'gpu_last_sample':gpu_value,\n                'training_bank_protocol_present':(bank/'protocol.json').exists(),'training_execution_scope_present':(bank/'training_execution_scope.json').exists()}")
        if target.startswith('audit_nystrom_ridge_resource'):
            text=text.replace("'prior_peaks_not_inferred':True,","'prior_peaks_not_inferred':True,'sampler_window_includes_serialized_pretraining_wait':True,\n        'samples_after_training_protocol_before_execution_scope':sum(r['training_bank_protocol_present'] and not r['training_execution_scope_present'] for r in rows),")
        ast.parse(text,filename=target);path.write_text(text,encoding='utf-8',newline='\n');new[str(path.resolve())]=sha(path)
    for p,d in old.items():assert sha(Path(p))==d,p
    with (HERE/'nystrom_ridge_execution_support_prepared_20261004.json').open('x',encoding='utf-8') as stream:
        json.dump({'status':'isolated_support_prepared_actual_dispatch_controls_pending',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'source_sha256':new,
            'original_source_sha256':old,'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)
    print('Six isolated Nyström resource/audit/scoped-dispatch helpers prepared',flush=True)

if __name__=='__main__':main()

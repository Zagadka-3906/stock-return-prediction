"""Prepare genuine72 native and55 full training controls for the frozen151 proposal."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    targets=[];originals=[]
    mapping={
        'HuberSparse72_native_historical_calendar_v1_20261008':'RFFSparse72_native_historical_calendar_v1_20261009',
        'HuberSparse59_round150_proposal_v1_20261008':'RFFSparse59_round151_proposal_v1_20261009',
        'HuberSparse59_synthetic55_and_state20_metadata_v1_20261008':'RFFSparse59_synthetic55_and_state20_metadata_v1_20261009',
        'HuberSparse_complete_parent_CDF_v1_20261008':'RFFSparse_complete_parent_CDF_v3_20261009',
        'HuberSparse_complete_parent_native_stage_v1_20261008':'RFFSparse_complete_parent_native_stage_v3_20261009',
        'actual_HuberSparse72_native_calendar_location_v1_20261008':'actual_RFFSparse72_native_calendar_location_v1_20261009',
        'HuberSparse55_parent134_historical_v1_20261008':'RFFSparse55_parent134_historical_v1_20261009',
        'actual_HuberSparse55_parent134_location_v1_20261008':'actual_RFFSparse55_parent134_location_v1_20261009',
        'HuberSparse72_native_historical_calendar_controls_v1_20261008':'RFFSparse72_native_historical_calendar_controls_v1_20261009',
        'JointCrossHuberOrder185_controls_main_publication_v1_20261008':'AdaptiveJointCrossHuber242_controls_main_publication_v1_20261008',
        'nonflag_HuberIRLS64_streamed_v1_20261008.py':'nonflag_residual_RFF128_codec_20261007.py',
        'passed_actual54_HuberSparse':'passed_actual54_RFFSparse',
        'passed_actual55_HuberSparse':'passed_actual55_RFFSparse'}
    for old,new in (
        ('verify_HuberSparse72_native_historical_calendar_v1_20261008.py','verify_RFFSparse72_native_historical_calendar_v1_20261009.py'),
        ('verify_HuberSparse55_full_historical_controls_v1_20261008.py','verify_RFFSparse55_full_historical_controls_v1_20261009.py')):
        path=A/old;originals.append(path);s=path.read_text(encoding='utf8')
        for before,after in mapping.items():s=s.replace(before,after)
        if '72_' in new:
            s=s.replace("assert row['state_kind']=='linear'","assert row['state_kind'] in ('linear','random_fourier_linear')")
            s=s.replace("info['independent_linear_state_path']","info['independent_'+row['state_kind']+'_state_path']")
            s=s.replace("info['independent_linear_state_sha256']","info['independent_'+row['state_kind']+'_state_sha256']")
        targets.append(save(new,s))
    create(A/'RFFSparse151_historical_receiver_preparation_v1_20261009.json',{'status':'prepared_actual72_native55_full_training_receivers_before151_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*targets,
            A/'RFFSparse59_round151_proposal_v1_20261009.json',A/'RFFSparse59_synthetic55_and_state20_metadata_v1_20261009.json',
            A/'RFFSparse_complete_parent_CDF_v3_20261009.py',A/'RFFSparse_complete_parent_native_stage_v3_20261009.py']},
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'native':72,'full':55,'quality':0},flush=True)
if __name__=='__main__':main()

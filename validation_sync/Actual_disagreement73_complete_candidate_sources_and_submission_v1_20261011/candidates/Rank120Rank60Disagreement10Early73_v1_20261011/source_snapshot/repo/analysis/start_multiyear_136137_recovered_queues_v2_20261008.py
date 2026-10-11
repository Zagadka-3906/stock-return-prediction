"""Start frozen calendar-safe queues; all scoring still waits qualified predecessors."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    sources=[Path(__file__),A/'multiyear136137_queue_recovery_v2_20261008.json',
        A/'CrossFamily94_prospective_routes_v4_20261008.json',A/'Huber52_prospective_routes_v3_20261008.json',
        A/'actual_multiyear_residual_calendar_location_v1_20261008.json',A/'verify_HuberIRLS64_49_current_parent_v4_20261008.py']
    pins={str(p):sha(p) for p in sources}
    parent=start('HuberIRLS64_49_current_parent_controls_v4_20261008','verify_HuberIRLS64_49_current_parent_v4_20261008.py',[],pins)
    from queue_CrossFamily136_complete_pipeline_v4_20261008 import main as cross
    from queue_Huber137_complete_pipeline_v3_20261008 import main as huber
    cross();huber()
    archives={}
    for family in ('CrossFamily136','Huber137'):
        driver=f'archive_{family}_completed_scoring_CSV_v3_20261008.py';name=f'{family}_completed_scoring_CSV_archivist_v3_20261008'
        bound={**pins,str(A/driver):sha(A/driver)};archives[name]=start(name,driver,[],bound)
        create(A/f'actual_{family}_completed_CSV_archivist_hidden_launch_v3_20261008.json',{
            'status':'started_only_closed_generated_scoring_CSV_archive_on_E','identity':archives[name],'input_sha256':bound,
            'all_models_inputs_and_capsules_retained':True,'new_quality_scores':0})
    create(A/'actual_multiyear136137_recovered_queue_launches_v2_20261008.json',{
        'status':'started_two_calendar_safe_complete_queues_and_closed_CSV_archivists',
        'current_parent_identity':parent,'archives':archives,'input_sha256':pins,
        'new_fits':0,'new_official_scores':0,'actual_future_X_and_Y_read':False})


if __name__=='__main__':main()

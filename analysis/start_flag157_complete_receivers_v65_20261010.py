"""Start the seven frozen157 phases; dependency gates keep actual work chronological."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    proof=A/'BF16FlagAfter15222_prospective_routes_v2_20261010.json';p=read(proof)
    assert (p['prospective_sources'],len(p['graph_controls']))==(40,380)
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    wrapper=A/'manual_resume_service_alias_runtime_v3_20261010.py';aliases=A/'manual_resume_service_aliases_v2_20261010.json'
    specs=[
        ('BF16FlagAfter15222_round157_source_admission_v1_20261009','verify_BF16FlagAfter15222_round157_sources_v1_20261010.py',[]),
        ('BF16FlagAfter15222_controls_main_publication_v1_20261009','publish_BF16FlagAfter15222_evidence_v1_20261009.py',['controls']),
        ('BF16FlagAfter15222_official_comparison_v3_20261009','run_BF16FlagAfter15222_official_comparison_v3_20261009.py',[]),
        ('BF16FlagAfter15222_scores_main_publication_v1_20261009','publish_BF16FlagAfter15222_evidence_v1_20261009.py',['scores']),
        ('BF16FlagAfter15222_selected_candidate_preparation_v1_20261009','prepare_BF16FlagAfter15222_selected_candidate_v1_20261009.py',[]),
        ('BF16FlagAfter15222_selected_candidate_sealing_v1_20261009','seal_BF16FlagAfter15222_selected_candidate_v1_20261009.py',[]),
        ('BF16FlagAfter15222_round157_full_registration_v1_20261009','run_BF16FlagAfter152157_safe_registration_v1_20261010.py',[]),
    ]
    rows={}
    for name,driver,arguments in specs:
        path=A/driver
        args=['--driver',str(path),'--aliases',str(aliases),*['--argument='+a for a in arguments]]
        pins={str(wrapper):sha(wrapper),str(aliases):sha(aliases),str(path):sha(path),str(proof):sha(proof)}
        rows[name]=start_service(name,wrapper.name,args,pins)
        print({'started':name,'worker':rows[name]['owned_worker_pid']},flush=True)
    create(A/'BF16FlagAfter152157_actual_complete_hidden_launches_v65_20261010.json',{
        'status':'started_seven157_receivers_after40_routes380_graphs_and_corrected_quality3',
        'launches':rows,'stop_at_local':control['stop_at_local'],'new_quality_scores_by_dispatch':0})

if __name__=='__main__':main()

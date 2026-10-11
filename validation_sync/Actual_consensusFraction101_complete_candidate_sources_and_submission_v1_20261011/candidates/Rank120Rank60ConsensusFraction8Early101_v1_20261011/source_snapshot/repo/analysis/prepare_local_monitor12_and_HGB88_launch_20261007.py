"""Admit complete88 sources and truthful observer12; start only actual consoleless services."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    preparation=A/'flagged_HGB88_complete_pipeline_preparation_v4_20261007.json';prepared=read(preparation)
    admission=A/'flagged_HGB88_round116_source_admission_20261007.json';proof=read(admission)
    assert proof['status']=='passed_actual85_full_controls_and24_prospective116_source_schema_baseline_and_ablation_routes'
    for path,digest in {**prepared['input_sha256'],**proof['input_sha256']}.items():assert sha(path)==digest,path
    source=A/'monitor_local_only_runtime_v11_20261007.py';monitor=A/'monitor_local_only_runtime_v12_20261007.py';assert not monitor.exists()
    text=source.read_text(encoding='utf8')
    before="'CPU_ELASTIC44_selected_candidate_sealing_v3','CPU_ELASTIC44_round114_full_registration_v3')"
    assert text.count(before)==1
    text=text.replace(before,"'CPU_ELASTIC44_selected_candidate_sealing_v3','CPU_ELASTIC44_round114_full_registration_v3',\n        'protected_upper_pool_HGB66_round115_full_registration_v5','flagged_HGB_small_amplitude88_official_comparison_v4',\n        'flagged_HGB_small_amplitude88_scores_main_publication_v4','flagged_HGB_small_amplitude88_selected_candidate_preparation_v4',\n        'flagged_HGB_small_amplitude88_selected_candidate_sealing_v4','flagged_HGB88_round116_full_registration')")
    text=text.replace('(113, 24), (114, 25))','(113, 24), (114, 25), (115, 26), (116, 27))')
    text=text.replace("114:'CPU_ELASTIC44_round114_full_registration_v3'}[n]","114:'CPU_ELASTIC44_round114_full_registration_v3',115:'protected_upper_pool_HGB66_round115_full_registration_v5',116:'flagged_HGB88_round116_full_registration'}[n]")
    text=text.replace("best_number = max(qualified, key=lambda n: (qualified[n]['official_score'], n))","best_number = min(qualified, key=lambda n: (-qualified[n]['official_score'], n))")
    needle="    write(A / 'single_host_optimization_live_status_v11_20261007.json', value)"
    assert text.count(needle)==1
    more="""    for family,folder,expected in (
        ('lower_pool_HGB66','protected_upper_pool_HGB66_official_comparison_v2_20261007',66),
        ('small_amplitude_HGB88','flagged_HGB_small_amplitude88_official_comparison_v4_20261007',88)):
        directory=A/folder
        value['actual_'+family+'_official_record_count']=len(list(directory.glob('case*_official.json')))
        value[family+'_expected_official_records']=expected
        stage=directory/'actual_stage.json'
        if stage.exists():value['actual_'+family+'_stage']=read(stage)
    value['no_full_qualification_claim_from_partial_case_counts']=True
"""
    text=text.replace(needle,more+needle).replace('single_host_optimization_live_status_v11_20261007','single_host_optimization_live_status_v12_20261007').replace("'local_only_v11'","'local_only_v12'")
    compile(text,str(monitor),'exec')
    with monitor.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
    pins={**prepared['input_sha256'],**proof['input_sha256'],str(Path(__file__)):sha(Path(__file__)),str(preparation):sha(preparation),str(admission):sha(admission),str(monitor):sha(monitor)}
    rows=[]
    for job in prepared['jobs']:
        row=start_service(job['name'],job['driver'],job['arguments'],pins);rows.append({'name':job['name'],'native_launch':row})
    record=A/'flagged_HGB88_complete_pipeline_actual_hidden_launches_v4_20261007.json'
    create(record,{'status':'launched_actual88_scoring_selected_candidate_and_full116_QA27_pipeline',
        'input_sha256':pins,'services':rows,'new_native_fits':0,'new_quality_scores_by_launch':0,'canonical116_sources_written':0,
        'qualification_waits_actual115_QA26_main_closure':True,'console_windows':0,'scientific_workers_stopped':0})
    print({'status':'launched_five_complete_pipeline_services','workers':[r['native_launch']['owned_worker_pid'] for r in rows]},flush=True)

if __name__=='__main__':main()

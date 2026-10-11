"""Launch the admitted actual scheme; preserve two zero-score stale-controller failures."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    folder=A/'service_owned_workflows_20261006/nonflag_RFFRidge40_round122_source_admission_v2'
    assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='passed'
    admission=A/'nonflag_RFFRidge40_round122_source_admission_v1_20261007.json';proof=read(admission)
    assert proof['status']=='passed_actual37_controls_and24_prospective122_complete_source_schema_paths_and_graph_routes'
    assert proof['declared_prospective_sources']==24 and len(proof['baseline_gain_regressions'])==9 and len(proof['graph_metadata_controls'])==12
    template=A/'continue_nonflag_RFFRidge40_after_actual_admission_v2_20261007.py'
    tree=ast.parse(template.read_text(encoding='utf8'))
    jobs=ast.literal_eval(next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='jobs' for t in n.targets)))
    assert len(jobs)==6 and all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),admission,template,*[A/driver for _,driver,_ in jobs]]}}
    for p,d in pins.items():assert sha(p)==d,p
    launches={}
    for name,driver,args in jobs:
        try:row=start_service(name,driver,args,pins)
        except AssertionError:
            # A fast successful helper can finish before the starter's live-only assertion.
            service=A/'service_owned_workflows_20261006'/name;row=read(service/'native_launch.json')
            assert not owned(row) and read(service/'service_execution.json')['status']=='passed'
            assert row['actual_native_console_handle']==0 and not row['independent_launch_root_in_any_job']
            assert read(service/'job_definition.json')['input_sha256']==pins
        launches[name]=row
    create(A/'nonflag_RFFRidge40_complete_pipeline_actual_hidden_launches_v1_20261007.json',{
        'status':'started_actual6_RFFRidge_stages_after_genuine_complete122_source_admission',
        'launches':launches,'input_sha256':pins,'new_quality_scores_by_launcher':0,'test_labels_read':False})
    print({'status':'started_actual6_admitted_scientific_stages'},flush=True)
if __name__=='__main__':main()

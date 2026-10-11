"""Repair only administrative dependency and receipt bindings; retain all scientific output contracts."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    service='exact135_144_connected_API_publication_reconciliation_v2_20261008'
    assert read(A/'service_owned_workflows_20261006'/service/'service_execution.json')['status']=='passed'
    records=[];outputs=[]
    for stem,receipt in [('BF16wide40',('v2','v3')),('ConeRidgeAlpha100',('v1','v2'))]:
        old_service=stem+'_scores_main_publication_v5_20261008'
        assert read(A/'service_owned_workflows_20261006'/old_service/'service_execution.json')['status']=='failed'
        for role in ('prepare','seal'):
            old=A/f'{role}_{stem}_selected_candidate_v5_20261008.py';new=A/f'{role}_{stem}_selected_candidate_v6_20261008.py'
            assert not new.exists();value=old.read_text(encoding='utf8')
            value=value.replace(old_service,service)
            value=value.replace(stem+'_selected_candidate_preparation_v5_20261008',stem+'_selected_candidate_preparation_v6_20261008')
            value=value.replace(stem+'_scores_github_'+receipt[0]+'_20261008/receipt.json',stem+'_scores_github_'+receipt[1]+'_20261008/receipt.json')
            # Include the actual administrative reconciliation in the pre-feature freeze.
            if role=='prepare':
                needle="    pins={**protocol_pins,**pilot['input_sha256'],**{str(p):sha(p) for p in sources}}";assert value.count(needle)==1
                value=value.replace(needle,"    sources.extend([A/'exact135_144_connected_API_reconciliation_v2_20261008.json',A/'reconcile_exact135_144_connected_API_publication_v2_20261008.py',A/'prepare135_144_candidates_after_connected_API_v1_20261008.py'])\n"+needle)
            compile(value,str(new),'exec');new.write_text(value,encoding='utf8',newline='\n');outputs.append(new);records.append({'source':str(old),'source_sha256':sha(old),'fresh':str(new),'fresh_sha256':sha(new)})
    pins={str(p):sha(p) for p in [Path(__file__),*outputs,A/'exact135_144_connected_API_reconciliation_v2_20261008.json']}
    proof=A/'candidates135_144_connected_API_recovery_v1_20261008.json'
    create(proof,{'status':'frozen_four_fresh_candidate_and_sealing_administrative_receivers_after_actual140_score_main_publication','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'new_quality_scores':0,'training_models_scoring_and_graph_math_unchanged':True,'old_failed_services_and_files_preserved':True})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={}
    for stem in ('BF16wide40','ConeRidgeAlpha100'):
        for role,stage in [('prepare','preparation'),('seal','sealing')]:
            name=f'{stem}_selected_candidate_{stage}_v6_20261008'
            launches[name]=start(name,f'{role}_{stem}_selected_candidate_v6_20261008.py',[],pins)
    create(A/'candidates135_144_connected_API_hidden_launches_v1_20261008.json',{'status':'started_fresh_candidate_and_sealing_receivers','launches':launches,'input_sha256':pins,'official_scores_complete':140,'full135_and144_registration_still_pending':True})
    print(json.dumps({'started':list(launches)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()

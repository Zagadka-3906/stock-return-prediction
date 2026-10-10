"""Freeze three fresh administrative receivers for the original94-case search; serialize main writes after144."""
from pathlib import Path
import sys,ast,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    assert read(A/'service_owned_workflows_20261006/BF16wide40_round135_full_registration_v7_20261008/service_execution.json')['status']=='passed'
    assert read(A/'service_owned_workflows_20261006/CrossFamily91_current_parent_controls_v2_20261008/service_execution.json')['status']=='passed'
    changes={'BF16wide40_round135_full_registration_v4_20261008':'BF16wide40_round135_full_registration_v7_20261008','CrossFamily91_current_parent_controls_v1_20261008':'CrossFamily91_current_parent_controls_v2_20261008','actual_CrossFamily91_current_parent_location_v1_20261008':'actual_CrossFamily91_current_parent_location_v2_20261008','CrossFamily94_round136_source_admission_v4_20261008':'CrossFamily94_round136_source_admission_v5_20261008','CrossFamily94_controls_main_publication_v4_20261008':'CrossFamily94_controls_main_publication_v5_20261008','CrossFamily94_official_comparison_v4_20261008':'CrossFamily94_official_comparison_v5_20261008','CrossFamily94_actual_controls_index_v3_20261008':'CrossFamily94_actual_controls_index_v4_20261008','CrossFamily94_controls_github_v1_20261008':'CrossFamily94_controls_github_v2_20261008'}
    outputs=[];originals=[]
    for stem in ('verify_CrossFamily94_round136_sources','run_CrossFamily94_official_comparison','publish_CrossFamily94_evidence'):
        source=A/(stem+'_v4_20261008.py');target=A/(stem+'_v5_20261008.py');assert not target.exists();old=source.read_text(encoding='utf8');value=old
        for before,after in changes.items():value=value.replace(before,after)
        # All original comparisons, math, loops, models, native controls and source-preview graph AST are unchanged.
        tree=ast.parse(old)
        for node in ast.walk(tree):
            if isinstance(node,ast.Constant) and isinstance(node.value,str):
                for before,after in changes.items():node.value=node.value.replace(before,after)
        assert ast.dump(tree)==ast.dump(ast.parse(value))
        if stem.startswith('publish_'):
            needle="    out=A/f'CrossFamily94_{phase}_github_v1_20261008'";assert value.count(needle)==1;value=value.replace(needle,"    out=A/f'CrossFamily94_{phase}_github_v2_20261008'")
            needle="    assert phase in ('controls','scores')";assert value.count(needle)==1;value=value.replace(needle,needle+"\n    closed('ConeRidgeAlpha100_round144_full_registration_v12_20261008')")
        if stem.startswith('run_'):
            needle="    closed('CrossFamily94_round136_source_admission_v5_20261008')";assert value.count(needle)==1;value=value.replace(needle,"    closed('ConeRidgeAlpha100_round144_full_registration_v12_20261008')\n"+needle)
        compile(value,str(target),'exec');target.write_text(value,encoding='utf8',newline='\n');outputs.append(target);originals.append(source)
    pins={str(p):sha(p) for p in [Path(__file__),*outputs,*originals,A/'CrossFamily91_current_parent_gate_recovery_v2_20261008.json']}
    create(A/'CrossFamily136_quality_receiver_recovery_v5_20261008.json',{'status':'frozen_three_fresh_exact94_case_receiver_dependencies_after_actual135_qualification','input_sha256':pins,'dependency_and_metadata_mapping':changes,'all_mathematical_AST_and_native_model_bank_and_24_preview_graphs_unchanged':True,'main_publication_and_quality_wait_for_complete144_to_prevent_competing_publishers':True,'old_failed_verifier4_scoring4_and_publication4_preserved':True,'new_quality_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=[('CrossFamily94_round136_source_admission_v5_20261008',outputs[0],[]),('CrossFamily94_controls_main_publication_v5_20261008',outputs[2],['controls']),('CrossFamily94_official_comparison_v5_20261008',outputs[1],[]),('CrossFamily94_scores_main_publication_v5_20261008',outputs[2],['scores'])]
    launches={n:start(n,p.name,args,pins) for n,p,args in jobs}
    create(A/'CrossFamily136_quality_receiver_hidden_launches_v5_20261008.json',{'status':'started_actual_source_admission_and_original94_scoring_publication_receivers','launches':launches,'input_sha256':pins,'new_quality_scores_by_dispatch':0})
    print(json.dumps({'started':list(launches)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()

"""Fresh actual118 routes also correct inherited descriptive proof labels."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    originals=['prepare_HGB_quarter_numeric28_round118_sources_20261007.py',
      'run_HGB_quarter_numeric28_round118_full_registration_20261007.py',
      'verify_HGB_quarter_numeric28_round118_sources_20261007.py',
      'verify_HGB_quarter_numeric28_transform_20261007.py','publish_HGB_quarter_numeric28_evidence_20261007.py']
    routes={n[:-3]:n[:-12]+'_v2_20261007' for n in originals}
    paths=[Path(__file__)]
    for old in originals:
        new=routes[old[:-3]]+'.py';p=A/new;assert not p.exists()
        text=substitute((A/old).read_text(encoding='utf8'),routes)
        if old.startswith('run_'):
            text=text.replace('passed_all_actual117_registry_source_paths','passed_all_actual118_registry_source_paths')
            text=text.replace('Register88 actual lower-pool scores and its sealed winner, full QA27, and main.','Register28 actual numerical-order scores and its sealed winner, full QA29, and main.')
        elif old.startswith('verify_HGB_quarter_numeric28_transform'):
            text=text.replace('parent116_not_complete_or_tested_by_this_preflight','selected_parent117_graph_not_used_by_reference112_preflight')
        elif old.startswith('verify_HGB_quarter_numeric28_round'):
            text=text.replace('Admit actual337 controls and prospective complete117 routes before official340 work.','Admit actual25 controls and prospective complete118 routes before official28 work.')
        elif old.startswith('publish_'):
            text=text.replace('Publish actual337 controls and actual340 scores separately to main.','Publish actual25 controls and actual28 scores separately to main.')
        compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');paths += [A/old,p]
    create(A/'HGB_quarter_numeric28_source_route_preparation_v2_20261007.json',{'status':'compiled_five_fresh_actual118_source_routes_and_descriptive_scope_labels_before_admission',
      'input_sha256':{str(p):sha(p) for p in paths},'routes':routes,'new_native_fits':0,'new_quality_scores':0})

if __name__=='__main__':main()

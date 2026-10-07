"""Generate the complete admitted 76-case scheme from the genuine selected parent."""
from pathlib import Path
import sys,hashlib,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_RFF128125_route_mapping_20261007 import convert
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import prepare_nonflag_RFFRidge40_round122_sources_v2_20261007 as base
NAMES={name:convert(name) for name in base.NAMES.values()}
def generate(parent):
    assert parent in (112,121,124)
    extra={'_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json',
      'PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
      'explicit_comparison_parent_round=112':f'explicit_comparison_parent_round={parent}',
      "'explicit_parent_round': 112":f"'explicit_parent_round': {parent}"}
    result={}
    for old,text in base.generate(112).items():
        name=NAMES[old];text=substitute(convert(text),extra)
        if name.startswith('register_'):
            needle="                graph['nonflag_CPU_RFF128_residual_CDF'] = {**cfg,";assert text.count(needle)==1
            text=text.replace(needle,"                assert cfg['residual_sign'] in (-1,1)\n"+needle)
        if name.startswith('publish_'):
            text=text.replace('112、120、121合格锚点','112、121、124合格锚点')
            text=text.replace('36项非涨停残差','72项双向非涨停残差')
        compile(text,str(A/name),'exec');result[name]=text
    assert len(result)==8
    return result
def main():
    ready_path=A/'nonflag_RFF12876_selected_release_v1_20261007/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual76_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'nonflag_RFF12876_official_comparison_v1_20261007/verification.json');assert len(pilot['records'])==76 and pilot['best']==ready['best']
    proof_path=A/'nonflag_RFF12876_round125_source_admission_v1_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual73_controls_and24_prospective125_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists(),name
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'nonflag_RFF12876_round125_source_preparation_v1_20261007.json',
      {'status':'passed_actual76_sealed_candidate_and_admitted_full125_QA36_sources',
       'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':125,'scored_records':76,
       'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
       'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},
       'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()

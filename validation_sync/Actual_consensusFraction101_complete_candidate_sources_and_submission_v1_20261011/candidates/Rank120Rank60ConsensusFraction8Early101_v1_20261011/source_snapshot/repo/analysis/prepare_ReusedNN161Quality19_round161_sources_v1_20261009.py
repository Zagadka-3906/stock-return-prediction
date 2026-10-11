"""Generate eight original-six-view routes for each qualified comparison anchor; fixed152 signal."""
from pathlib import Path
import ast,hashlib,sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_BF16Seed10_80_round155_sources_v1_20261009 as previous
from prepare_ReusedNN161Stage_core_drafts_v1_20261009 import route
STATUS='passed_actual19_reusedNN161_complete_parent_rank_CDF_full_official_comparisons'

def normalize(s):
    s=route(s)
    s=s.replace('passed_actual19_complete152_flag_neural_training_only_official_comparisons',STATUS)
    return s

NAMES={old:normalize(new) for old,new in previous.NAMES.items()}

def generate(parent):
    assert parent in (152, 160)
    output={}
    for name,s in previous.generate(152).items():
        name=normalize(name);s=normalize(s)
        tree=ast.parse(s);replacements=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Assign):
                names=[n.id for n in node.targets if isinstance(n,ast.Name)]
                value=None
                if 'comparison_baseline' in names:value=f"read(A/'optimization_20261003_r{parent}/selection.json')['winner']['metrics']['final_score']"
                elif 'PREVIOUS' in names:value=f"ROOT/'analysis/optimization_20261003_r{parent}'"
                elif 'PREVIOUS_NUMBER' in names:value=str(parent)
                if value is not None:replacements.append((node.value,value))
            if isinstance(node,ast.keyword) and node.arg in ('explicit_comparison_parent_round','explicit_parent_round'):replacements.append((node.value,str(parent)))
            if isinstance(node,ast.Dict):
                for key,value in zip(node.keys,node.values):
                    if isinstance(key,ast.Constant) and key.value=='explicit_parent_round':replacements.append((value,str(parent)))
                    if isinstance(key,ast.Constant) and key.value=='saved_selected_parent_models':replacements.append((value,f"len(read(ROOT/'candidates/optimization_20261003_r{parent}/verification.json')['models'])"))
        for node,value in sorted(replacements,key=lambda x:(x[0].lineno,x[0].col_offset),reverse=True):s=previous.previous.replace_node(s,node,value)
        s=s.replace('第161轮：单独seed09神经网络在固定完整148之后的73种正负排序融合，加七个合格锚点，共22项。',
            '第161轮：复用seed09神经网络，在完整152方案之后仅对flag_valid做17种正负排序融合，加五个合格锚点，共22项。')
        s=s.replace('依据实际73完整/219截断、42原生/42冷控制','依据实际17完整/51截断、14原生/14冷控制及原有六年度独立回放')
        compile(s,str(A/name),'exec');output[name]=s
    assert len(output)==8 and set(output)==set(NAMES.values())
    return output

def source_paths():
    names=[
        'prepare_ReusedNN161Stage_core_drafts_v1_20261009.py','prepare_ReusedNN161Stage_core_v62_20261009.py',
        'ReusedNN161Stage_core_preparation_v62_20261009.json','ReusedNN161Quality19_round161_plan_v1_20261009.json',
        'ReusedNN161Full17_train_only_proposal_v1_20261009.json','ReusedNN161Full17_synthetic17_cold51_v1_20261009.json',
        'ReusedNN161Stage_storage_v1_20261009.py','ReusedNN161Stage_D_scoring_scope_v1_20261009.json',
        'verify_ReusedNN161Stage_D_scoring_scope_v1_20261009.py','BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',
        'BF16_complete_parent_rank_CDF_v1_20261008.py','ReusedNN161Stage_complete_parent_native_stage_v1_20261009.py',
        'predict_ReusedNN161Stage_complete_parent_scheme_v1_20261009.py','ReusedNN161Stage_complete_native_predictor_preparation_v58_20261009.json',
        'run_ReusedNN161Quality19_official_comparison_v3_20261009.py','prepare_ReusedNN161Quality19_selected_candidate_v1_20261009.py',
        'seal_ReusedNN161Quality19_selected_candidate_v1_20261009.py','run_ReusedNN161Quality19_round161_full_registration_v1_20261009.py',
        'run_ReusedNN161Stage_safe_registration_v1_20261010.py','publish_ReusedNN161Quality19_evidence_v1_20261009.py',
        'verify_ReusedNN161Quality19_prospective_routes_v2_20261010.py','ReusedNN161Quality19_prospective_routes_v2_20261010.json',
        'verify_ReusedNN161Quality19_round161_sources_v1_20261010.py','ReusedNN161Quality19_round161_source_admission_v1_20261009.json',
        'ReusedNN161Quality19_actual_controls_index_v1_20261009.json','ReusedNN161Quality19_round161_source_preparation_v1_20261009.json',
        'ReusedNN161Quality19_selected_release_v1_20261009/selected_candidate_ready_for_registration.json',
        'ReusedNN161Quality19_scores_github_v1_20261009/receipt.json',
        'actual_ReusedNN161Full17_full_training_location_v1_20261009.json','actual_ReusedNN161Stage_native14_calendar_location_v1_20261009.json',
        'actual_BF16Huber010161_full5_independent_location_v1_20261009.json','actual_BF16_medium2048_huber010_seed09_e64_bank6_location_v1_20261009.json',
        'neural_BF16_medium2048_huber010_seed09_e64_native_v1_20261009.py','neural_BF16_medium2048_huber010_seed09_independent_forward_v1_20261009.py',
        'lossless_chunked_safe_main_runtime_v1_20261009.py','serial_main_publication_mutex_v1_20261009.py',
        'verified_TLS_Git_retry_runtime_v2_20261008.py','short_content_addressed_native_storage_v2_20261008.py',
        'resolve_sealed_scientific_protocol_v2_20261007.py','publish_explicit_parent_training_round_v2_20261005.py',
    ]
    return list(dict.fromkeys([Path(__file__),Path(previous.__file__),*(A/n for n in names),*(A/n for n in NAMES.values())]))

def main():
    ready_path=A/'ReusedNN161Quality19_selected_release_v1_20261009/selected_candidate_ready_for_registration.json'
    ready=read(ready_path);assert ready['sealed_candidate_complete']
    pilot=read(A/'ReusedNN161Quality19_official_comparison_v1_20261009/verification.json')
    assert pilot['status']==STATUS and len(pilot['records'])==19 and pilot['best']==ready['best']
    admission=A/'ReusedNN161Quality19_round161_source_admission_v1_20261009.json';proof=read(admission)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    parent=pilot['actual_comparison_parent_round'];generated=generate(parent)
    expected=proof['generated_source_sha256'][str(parent)]
    for name,s in generated.items():assert not (A/name).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[name]
    for name,s in generated.items():(A/name).write_text(s,encoding='utf8',newline='\n')
    create(A/'ReusedNN161Quality19_round161_source_preparation_v1_20261009.json',{
        'status':'passed_actual19_sealed_candidate_and_admitted_full161_QA72_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},
        'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()

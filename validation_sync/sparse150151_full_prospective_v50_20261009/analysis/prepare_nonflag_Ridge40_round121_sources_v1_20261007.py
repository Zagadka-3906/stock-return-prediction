"""Eight complete publication sources for one frozen Ridge winner, with recursive aliases."""
from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from prepare_nonflag_Ridge40_science_routes_20261007 import mapping
import prepare_nonflag_HGB40_round120_sources_v4_20261007 as original_generator
NAMES={name:name.replace('nonflag_HGB40','nonflag_Ridge40').replace('round120','round121').replace('qa31','qa32') for name in original_generator.NAMES.values()}

def generate(parent):
    assert parent in (112,119,120)
    m=mapping()
    m.update({old[:-3]:new[:-3] for old,new in NAMES.items()})
    m.update({'optimization_20261003_r120':'optimization_20261003_r121',
        'round120_full_scope':'round121_full_scope','original_inference_selection_round120':'original_inference_selection_round121',
        'original_registry_alias_round120':'original_registry_alias_round121','round120_receipt':'round121_receipt',
        'validation_sync/round120':'validation_sync/round121','round120/':'round121/',"'round120'":"'round121'",
        'NUMBER = 120':'NUMBER = 121','number == 120':'number == 121','WAVES = (403,)':'WAVES = (404,)',
        'wave=403':'wave=404','wave403_results':'wave404_results',"'waves': [403]":"'waves': [404]","'round': 120":"'round': 121",
        'lossless_ranking_display_qa_v31_20261007':'lossless_ranking_display_qa_v32_20261007',
        'ranking_display_qa_v31_20261007':'ranking_display_qa_v32_20261007',
        '(120, 31, 40)':'(121, 32, 40)',"namespace['snapshot'](120)":"namespace['snapshot'](121)",
        'actual_complete_QA_version=31':'actual_complete_QA_version=32',"'actual_full_QA_version': 31":"'actual_full_QA_version': 32",
        '_r112':f'_r{parent}','round112_receipt.json':f'round{parent}_receipt.json','PREVIOUS_NUMBER = 112':f'PREVIOUS_NUMBER = {parent}',
        'explicit_comparison_parent_round=112':f'explicit_comparison_parent_round={parent}',"'explicit_parent_round': 112":f"'explicit_parent_round': {parent}",
        'existing_CPU_HGB_native_bank_fits':'existing_CPU_Ridge_native_bank_fits',
        'actual20_conditional_CPU_HGB_native_bank_source':'actual10_nonflag_CPU_Ridge_native_bank_source'})
    result={}
    for old,text in original_generator.generate(112).items():
        new=NAMES[old]; text=substitute(text,m)
        if new.startswith('register_'):
            needle="            if cfg['model'] == 'remove_nonflag_Ridge':"
            assert text.count(needle)==1
            text=text.replace(needle,"            graph.pop('nonflag_CPU_HGB_residual_CDF',None)\n"+needle)
            needle="        A / 'collect_full_lossless_round121_qa32_20261007.py',"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\n        A / 'nonflag_residual_Ridge_codec_20261007.py',\n        A / 'nonflag_residual_Ridge_bank10_20261007/verification.json',\n        A / 'verify_nonflag_residual_Ridge37_transform_20261007.py',\n        A / 'nonflag_residual_Ridge37_transform_preflight_20261007/verification.json',")
        elif new.startswith('publish_'):
            start=text.index("    payload[(prefix / 'README.md').as_posix()] += ("); end=text.index('    previous = sync.git',start)
            text=text[:start]+"""    payload[(prefix / 'README.md').as_posix()] += (
        '\\n本轮40项完整官方比较：112、119、120合格锚点，两组非涨停残差Ridge及等权集成乘12幅度，以及消融。'
        '实际10年度成熟模型，教师106；替换已有非涨停HGB，保留完整涨停分支和2020输出。'
        '37项5635800行CDF与111冷前缀核对；官方八指标选优后冻结，选中新方案执行原生重载、独立线性解码、两次完整重放及冷80。'
        '完整榜六视图和45秒QA32保留，全部源码参数核对。仅main，未读取真实测试标签。有限网格不证明优化穷尽。\\n').encode('utf8')
"""+text[end:]
        compile(text,str(A/new),'exec'); result[new]=text
    assert len(result)==8
    return result

def main():
    ready_path=A/'nonflag_Ridge40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json'; ready=read(ready_path)
    assert ready['status']=='passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'nonflag_Ridge40_official_comparison_v1_20261007/verification.json'); assert len(pilot['records'])==40 and pilot['best']==ready['best']
    parent=pilot['actual_comparison_parent_round']; proof_path=A/'nonflag_Ridge40_round121_source_admission_v1_20261007.json'; proof=read(proof_path)
    assert proof['status']=='passed_actual37_controls_and24_prospective121_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(parent)
    for name,text in generated.items():
        assert not (A/name).exists(),name
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name]
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(A/'nonflag_Ridge40_round121_source_preparation_v1_20261007.json',{'status':'passed_actual40_sealed_candidate_and_admitted_full121_QA32_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':121,'scored_records':40,'actual_comparison_parent_round':parent,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()

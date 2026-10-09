"""Prepare complete 76-case routes with a signed residual persisted in every native graph."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from nonflag_RFF128125_route_mapping_20261007 import convert
def main():
    names=['run_nonflag_RFFRidge40_official_comparison_v1_20261007.py',
      'prepare_nonflag_RFFRidge40_selected_candidate_v1_20261007.py','seal_nonflag_RFFRidge40_selected_candidate_v1_20261007.py',
      'run_nonflag_RFFRidge40_admitted_comparison_v2_20261007.py','run_nonflag_RFFRidge40_round122_full_registration_v2_20261007.py',
      'publish_nonflag_RFFRidge40_evidence_v2_20261007.py','verify_nonflag_RFFRidge40_round122_sources_v2_20261007.py',
      'verify_nonflag_RFFRidge40_prospective_routes_v2_20261007.py','predict_nonflag_residual_RFFRidge_complete_scheme_20261007.py']
    originals=[];generated={}
    for name in names:
        old=A/name;originals.append(old);new=A/convert(name);assert not new.exists(),new
        text=convert(old.read_text(encoding='utf8'))
        if name.startswith('run_nonflag_RFFRidge40_official'):
            needle="'model':name,'weight':weight,'universe':plan['universe']}\n        for name in [*plan['single_native_heads'],*plan['ensembles']] for weight in plan['weights']]";assert text.count(needle)==1
            text=text.replace(needle,"'model':name,'weight':weight,'universe':plan['universe'],'residual_sign':sign}\n        for name in [*plan['single_native_heads'],*plan['ensembles']] for sign in plan['residual_signs'] for weight in plan['weights']]")
            text=text.replace("'model':'remove_nonflag_RFF128','weight':0.,'universe':plan['universe']}","'model':'remove_nonflag_RFF128','weight':0.,'universe':plan['universe'],'residual_sign':1}")
            text=text.replace("flags,head[cfg['model']],cfg['weight'],prepared)","flags,head[cfg['model']]*cfg['residual_sign'],cfg['weight'],prepared)")
            text=text.replace("valid[:n],head[cfg['model']][:n],cfg['weight'],","valid[:n],head[cfg['model']][:n]*cfg['residual_sign'],cfg['weight'],")
        if name.startswith('prepare_'):
            text=text.replace("info['parameters']['n_components']==32","info['parameters']['n_components']==128")
            text=text.replace("valid,residual,cfg['weight'],cfg['universe'])","valid,residual*cfg['residual_sign'],cfg['weight'],cfg['universe'])")
            needle="            graph['nonflag_CPU_RFF128_residual_CDF']={**cfg";assert text.count(needle)==1
            text=text.replace(needle,"            assert cfg['residual_sign'] in (-1,1)\n"+needle)
        if name.startswith('verify_'):
            text=text.replace("len(native['records'])==3","len(native['records'])==6")
            text=text.replace("len(controls['controls'])==37","len(controls['controls'])==73")
            text=text.replace('len(graph_controls)==12','len(graph_controls)==24')
            text=text.replace("'actual_full_transform_controls':37,'actual_cold_prefix_controls':111,'actual_historical_native_hook_cases':3",
              "'actual_full_transform_controls':73,'actual_cold_prefix_controls':219,'actual_historical_native_hook_cases':6")
            text=text.replace("'cfg':{'model':model,","'cfg':{'residual_sign':sign,'model':model,")
            needle="        for model,weight,";assert text.count(needle)==1
            if 'for model,weight,names in examples:' in text:
                text=text.replace('for model,weight,names in examples:','for model,weight,names,sign in [(m,w,c,s) for m,w,c in examples for s in (-1,1)]:')
            else:text=text.replace('for model,weight,components in examples:','for model,weight,components,sign in [(m,w,c,s) for m,w,c in examples for s in (-1,1)]:')
            marker="graph['nonflag_CPU_RFF128_residual_CDF']['ordered_equal_mean_components']=="
            text=text.replace(marker,"graph['nonflag_CPU_RFF128_residual_CDF']['residual_sign']==sign and "+marker)
            text=text.replace('passed_actual24_prospective_sources_and12_graph_controls','passed_actual24_prospective_sources_and24_graph_controls')
        if name.startswith('run_nonflag_RFFRidge40_admitted'):
            text=text.replace("len(proof['graph_metadata_controls'])==12","len(proof['graph_metadata_controls'])==24")
        if name.startswith('publish_'):
            text=text.replace("(37 if phase=='controls' else 76)","(73 if phase=='controls' else 76)")
            text=text.replace("'actual_full_control_cases':37,'actual_cold_prefix_cases':111","'actual_full_control_cases':73,'actual_cold_prefix_cases':219")
            text=text.replace('两组样本数归一化L2','两组128维随机傅里叶与样本数归一化L2')
            text=text.replace('各12幅度','各12幅度与两个方向').replace('实际10年度成熟模型；37全量、111冷前缀和3历史原生核对','实际10年度成熟模型；73全量、219冷前缀和6历史原生核对')
        text=text.replace("('nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_rff128_')","('nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_rffridge_','nonflag_cpu_rff128_')")
        text=text.replace("('nonflag_residual_hgb','nonflag_residual_ridge','nonflag_residual_rff128')","('nonflag_residual_hgb','nonflag_residual_ridge','nonflag_residual_rffridge','nonflag_residual_rff128')")
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');generated[str(new)]=sha(new)
    paths=[Path(__file__),A/'nonflag_RFF128125_route_mapping_20261007.py',A/'prepare_nonflag_RFF12876_round125_sources_v1_20261007.py',*originals]
    create(A/'nonflag_RFF12876_science_route_preparation_20261007.json',
      {'status':'compiled_fresh_complete_RFF128125_both_signs_scoring_freeze_replay_and_publication_routes',
       'input_sha256':{**generated,**{str(p):sha(p) for p in paths}},'actual_official_scores':0,
       'actual_full125_admission_not_yet_claimed':True,'test_labels_read':False})
    import verify_nonflag_RFF12876_prospective_routes_v1_20261007 as verifier
    verifier.main()
if __name__=='__main__':main()

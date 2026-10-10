"""Correct prospective QA number and admit compiled sources without reading future READY."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_StockForward20Embedding179_complete48_pipeline_v1_20261010 as prototype
OLD=prototype.NAMES+[n for n in prototype.EXTRAS if n.endswith('.py') and ('179' in n or 'after178_v4' in n or 'selected_native14_v4' in n)]
def new_name(n):
    if n in prototype.NAMES:
        if 'qa90_' in n:return n.replace('qa90_','qa90_v3_')
        if '_v2_' in n:return n.replace('_v2_','_v3_')
        return n.replace('.py','_v3.py')
    if '_v4_' in n:return n.replace('_v4_','_v5_')
    if '_v5_' in n:return n.replace('_v5_','_v6_')
    return n.replace('_v1_','_v2_')
NAMES=[new_name(n) for n in prototype.NAMES]
EXTRAS=[new_name(n) if n in OLD else n.replace('179_candidate_sources_preparation_v4','179_candidate_sources_preparation_v5').replace('179_full_registry_sources_preparation_v2','179_full_registry_sources_preparation_v3') for n in prototype.EXTRAS]
def source_paths():
    from prepare_StockForward5Embedding178_complete48_pipeline_v1_20261010 import source_paths as older
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*older()]))
def main():
    assert allowed();mapping={Path(n).stem:Path(new_name(n)).stem for n in OLD}
    mapping.update({'prepare_StockForward20Embedding179_complete48_pipeline_v1_20261010':Path(__file__).stem,'stock_forward20_embedding179_candidate_sources_preparation_v4':'stock_forward20_embedding179_candidate_sources_preparation_v5','stock_forward20_embedding179_full_registry_sources_preparation_v2':'stock_forward20_embedding179_full_registry_sources_preparation_v3','StockForward20Embedding179_complete48_family_v5':'StockForward20Embedding179_complete48_family_v6','StockForward20Embedding48_selected_native14_v4':'StockForward20Embedding48_selected_native14_v5','actual_stock_forward20_embedding48_after178_normalization_queue_v4':'actual_stock_forward20_embedding48_after178_normalization_queue_v5'})
    pattern='|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True));outputs=[]
    for n in OLD:
        source=A/n;text=re.sub(pattern,lambda m:mapping[m.group()],source.read_text(encoding='utf8'))
        text=re.sub(r'\b89\b','90',text).replace('forward5_return','forward20_return')
        p=A/new_name(n);assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p)
    pins={str(p):sha(p) for p in [Path(__file__),A/prototype.__file__ if False else Path(prototype.__file__),*[A/n for n in OLD],*outputs]}
    for name in [EXTRAS[9],EXTRAS[10]]:create(A/name,{'status':'compiled48_correct_QA90_before_future_no_READY_or_scientific_output_read','input_sha256':pins,'expected_records':48,'expected_full_board':17014,'new_quality_scores':0,'test_labels_read':False})
    for p in source_paths():assert p.is_file(),p
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(179,178,(462,))
    for n in [EXTRAS[0],EXTRAS[1],EXTRAS[2],EXTRAS[3],EXTRAS[4],EXTRAS[5],EXTRAS[6],EXTRAS[7],EXTRAS[8]]:importlib.import_module(Path(n).stem)
    for n in [EXTRAS[0],EXTRAS[6]]:assert "closed('StockForward5Embedding178_complete48_family_v5_20261010')" in (A/n).read_text(encoding='utf8')
    assert '(179, 90, 48)' in (A/NAMES[-1]).read_text(encoding='utf8')
    proof=A/'stock_forward20_embedding179_full_execution_sources_admission_v2_20261010.json';create(proof,{'status':'compiled_exact48_QA90_mean20_identity_cross120_sources_before_future_dispatch','input_sha256':pins,'parent_rounds':[173,178],'actual_parent_service':'StockForward5Embedding178_complete48_family_v5_20261010','expected_full_board':17014,'new_quality_scores':0,'future_inference_pending':True,'test_labels_read':False})
    for name,n in [('actual_stock_forward20_embedding48_after178_normalization_queue_v5_20261010',EXTRAS[0]),('StockForward20Embedding48_selected_native14_v5_20261010',EXTRAS[1]),('StockForward20Embedding179_complete48_family_v6_20261010',EXTRAS[5])]:
        assert allowed();row=start_service(name,n,[],{str(A/n):sha(A/n),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'actual48_family_queued':True,'QA':90,'future_inference_pending':True},flush=True)
if __name__=='__main__':main()

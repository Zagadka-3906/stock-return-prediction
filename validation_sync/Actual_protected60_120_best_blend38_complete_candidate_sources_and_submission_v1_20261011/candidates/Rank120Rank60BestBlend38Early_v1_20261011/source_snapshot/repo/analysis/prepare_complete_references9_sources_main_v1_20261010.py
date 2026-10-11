from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    route=A/'PairTop184185_complete_reference_routes_v9_20261010.json';proof=read(route)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    template=A/'publish_PairTop185_native_admission_sources_main_v1_20261010.py'
    text=template.read_text(encoding='utf8')
    extra=[str(Path(__file__)),str(route),str(A/'PairTop184185_six_verified_idle_helpers_reference_recovery_v9_20261010.json'),*[str(A/n) for n in proof['driver_wrappers'].values()],*proof['input_sha256']]
    marker='    import publish_classifier_consensus_workflows_20261006 as h'
    assert text.count(marker)==1;text=text.replace(marker,'    paths += [Path(p) for p in '+repr(list(dict.fromkeys(extra)))+']\n'+marker)
    text=text.replace('PairTop185_native_admission_sources_v1_20261010','PairTop185_complete_references_v9_20261010').replace('PairTop185_native_admission_sources_main_v1_20261010','PairTop185_complete_references_main_v9_20261010').replace('PairTop185_native_admission_sources_main_receipt_v1_20261010','PairTop185_complete_references_main_receipt_v9_20261010')
    text=text.replace("'actual_top_parent_callbacks_CPU': 14", "'actual_top_parent_callbacks_CPU': 14, 'actual_recursive_local_import_references_checked':33, 'exact_new_source_reference_copies':9")
    text,count=re.subn(r"'保留同日排序六模型与完整五年度独立推理[^']*'",repr('保存已完成排序模型及原生42检查；递归补齐185轮9处源码引用、验证33处导入并恢复真实闲置依赖；权重与分数不变'),text);assert count==1
    p=A/'publish_PairTop185_complete_references_main_v9_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    assert allowed();name='actual_PairTop185_complete_references_sources_main_v9_20261010';row=start_service(name,p.name,[],{str(p):sha(p),str(route):sha(route)})
    create(A/(name+'_activation.json'),row);print({'actual_reference_proof':'passed','new_model_fits':0,'publication':row},flush=True)
if __name__=='__main__':main()

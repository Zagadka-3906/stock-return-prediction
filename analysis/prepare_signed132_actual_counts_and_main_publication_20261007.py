"""Actually check prospective132 record guards and publish the completed source preparation."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    original=A/'verify_future129_130_131_administrative_count_routes_20261007.py';fresh=A/'verify_future132_administrative_count_routes_20261007.py';text=original.read_text(encoding='utf8')
    begin=text.index('    entries=');end=text.index('    results=[];',begin)
    text=text[:begin]+"    entries=[(132,40,'nonflag_ReverseBayes40','prepare_nonflag_ReverseBayes40_round132_sources_v1_20261007')]\n"+text[end:]
    text=text.replace('future129_130_131_administrative_count_routes_actual_20261007.json','future132_administrative_count_routes_actual_20261007.json').replace('passed_actual72_prospective_sources','passed_actual24_prospective_sources').replace("'actual_compiled_sources':72","'actual_compiled_sources':24")
    compile(text,str(fresh),'exec');assert not fresh.exists();fresh.write_text(text,encoding='utf8',newline='\n')
    import importlib.util
    spec=importlib.util.spec_from_file_location('actual_signed132_count_controls',fresh);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.main()
    old=A/'publish_reverse_Bayes_actual_controls_main_20261007.py';new=A/'publish_signed132_actual_routes_main_20261007.py';text=old.read_text(encoding='utf8')
    text=text.replace('reverse_Bayes_actual_controls_github_20261007','signed132_actual_routes_github_20261007').replace('validation_sync/reverse_Bayes_actual_controls_20261007','validation_sync/signed132_actual_routes_20261007')
    begin=text.index('    proof_path=');end=text.index('    sources=list(dict.fromkeys(sources));',begin)
    sources=sorted(set(A.glob('*ReverseBayes*20261007.py'))|set(A.glob('*ReverseBayes*20261007.json')))
    sources=[p for p in sources if p.is_file() and not p.name.endswith('dispatch_deferred_until_manual_continue_20261007.json')]
    lines='\n'.join('      A/'+repr(p.name)+',' for p in sources)
    replacement="    proof_path=A/'future132_administrative_count_routes_actual_20261007.json';proof=read(proof_path)\n    assert proof['status']=='passed_actual24_prospective_sources_all_administrative_record_counts' and not proof['issues']\n    sources=[Path(__file__),A/'prepare_signed132_actual_counts_and_main_publication_20261007.py',A/'verify_future132_administrative_count_routes_20261007.py',proof_path,\n"+lines+"\n    ]\n"
    text=text[:begin]+replacement+text[end:]
    text=text.replace('published_actual_reverse_Bayes_native3_full37_cold111_controls','published_actual_signed132_24_sources12_graph_controls_and_all_record_count_guards')
    note="反向自适应收缩实际预检查：复用已验证的标量先验、对角先验及等权均值，明确负残差方向；3项原生重载与独立解码、37项5635800行独立CDF、111项冷前缀全部通过。尚未进行40项官方比较、选中方案冻结、真实完整候选推理或完整榜登记；没有新增模型训练或官方评分。另附本机资源事实及仍可行的交叉模型集成、稀疏线性模型等方向，未宣称优化穷尽。仅main；今晚23:55停工，明早须用户实际发送继续。"
    replacementnote="已实际预生成第132轮反向自适应收缩40项方案的24份完整登记源码，执行12项原生方案结构控制，并核对每一处记录项数。此前3项原生、37全量与111冷前缀控制已通过。40项官方比较仍须等待第131轮真实完整榜及main结束、再通过九项真实父分数回归与完整源码准入；23:12仍不具备条件则今晚不启动，明早等待用户继续。没有新增模型或官方分数，也没有宣称候选已正式采用。仅main。"
    assert note in text;text=text.replace(note,replacementnote).replace('记录负向自适应收缩实际3/37/111控制与未穷尽方向和资源证据','记录反向收缩完整132源码的实际24/12结构与全部项数检查')
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    create(A/'signed132_actual_routes_main_publication_preparation_20261007.json',{'status':'compiled_actual_signed132_source_preparation_main_publication',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,fresh,old,new,*sources]},'new_quality_scores':0})

if __name__=='__main__':main()

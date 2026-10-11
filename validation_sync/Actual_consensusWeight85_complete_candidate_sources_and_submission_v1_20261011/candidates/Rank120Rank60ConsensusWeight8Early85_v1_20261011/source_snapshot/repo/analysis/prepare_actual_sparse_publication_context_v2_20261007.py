"""Add measured resource/timing limits to the prepared, unexecuted publication."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'publish_actual_sparse_and_isolated_scoring_controls_main_20261007.py';new=A/'publish_actual_sparse_and_isolated_scoring_controls_main_v2_20261007.py'
    extra=[old,Path(__file__),A/'record_actual_scoring_latency_limitations_20261007.py',A/'actual_two_process_scoring_latency_interpretation_20261007.json']
    text=old.read_text(encoding='utf8');needle='    sources=list(dict.fromkeys(sources));';assert text.count(needle)==1
    text=text.replace(needle,"    sources += ["+','.join('A/'+repr(p.name) for p in extra)+"]\n"+needle)
    needle='后台负载会改变，不能视为通用提速保证';assert text.count(needle)==1
    text=text.replace(needle,'总耗时包含内存门槛等待与进程准备，串行阶段系统可用内存曾降至3.32GiB；后台GPU与完整榜检查负载会改变，不能把总耗时比视为通用或因果隔离的提速保证')
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    proof=A/'actual_sparse_publication_context_v2_source_preparation_20261007.json'
    create(proof,{'status':'compiled_unexecuted_publication_with_actual_wall_latency_and_resource_limitations',
      'input_sha256':{str(p):sha(p) for p in [new,*extra]},'original_prepared_publisher_bytes_retained':True,'new_quality_scores':0})
    driver=A/'dispatch_actual_sparse_publication_after_actual130_and131_controls_20261007.py';assert driver.is_file()
    row=start('actual_sparse_and_isolated_scoring_main_publication_dependency_queue',driver.name,[],{**read(proof)['input_sha256'],str(proof):sha(proof),str(driver):sha(driver)})
    create(A/'actual_sparse_publication_waiting_safe_main_window_hidden_launch_20261007.json',{'status':'started_hidden_wait_for_real130_main_and131_controls_main_or131_dispatch_defer','identity':row})

if __name__=='__main__':main()

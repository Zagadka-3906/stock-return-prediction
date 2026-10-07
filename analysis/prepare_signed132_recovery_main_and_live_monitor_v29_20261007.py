"""Publish actual pre-score correction and extend live status without changing V1 sources."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    proof=A/'signed132_actual_import_and_publication_recovery_v2_20261007.json';p=read(proof)
    assert p['status']=='resolved_actual_signed132_executor_import_and_publication_metadata_before_any_scores'
    old=A/'publish_signed132_actual_routes_main_20261007.py';new=A/'publish_signed132_actual_import_recovery_main_20261007.py'
    text=old.read_text(encoding='utf8').replace('signed132_actual_routes_github_20261007','signed132_actual_import_recovery_github_20261007').replace('validation_sync/signed132_actual_routes_20261007','validation_sync/signed132_actual_import_recovery_20261007')
    begin=text.index('    proof_path=');end=text.index('    sources=list(dict.fromkeys(sources));',begin)
    replacement="    proof_path=A/"+repr(proof.name)+";proof=read(proof_path)\n    assert proof['status']=='resolved_actual_signed132_executor_import_and_publication_metadata_before_any_scores'\n    sources=[Path(__file__),A/"+repr(Path(__file__).name)+",proof_path,A/'signed132_recovered_actual_hidden_queue_launch_v2_20261007.json',*[Path(p) for p in proof['input_sha256']]]\n"
    text=text[:begin]+replacement+text[end:]
    begin=text.index("            payload[(prefix/'README.md').as_posix()]=");end=text.index('            scope.reverify()',begin)
    note='第132轮实际启动源码的导入路径修复：保留已上传V1，新增V2启动器与准入器；实际数学评分器仍为原V1。检查所有反向融合模块引用，预生成的登记模块按冻结生成器核对。只替换等待中的调度器，没有终止训练或评分。原失败检查及源文件完整保留。仍须第131轮完成main、实际准入及23:12前方可启动40项官方比较；当前新增官方分数为0。仅main，23:55停工，明早用户继续后恢复。'
    text=text[:begin]+"            payload[(prefix/'README.md').as_posix()]=("+repr(note+'\n')+").encode('utf8')\n"+text[end:]
    text=text.replace('published_actual_signed132_24_sources12_graph_controls_and_all_record_count_guards','published_actual_signed132_import_recovery_preserving_all_original_sources').replace('记录反向收缩完整132源码的实际24/12结构与全部项数检查','保存反向融合实际导入引用修复及原始失败记录')
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    pins={**p['input_sha256'],str(proof):sha(proof),str(new):sha(new),str(Path(__file__)):sha(Path(__file__))}
    launch=start('signed132_actual_import_recovery_main_publication',new.name,[],pins)
    create(A/'signed132_actual_import_recovery_main_hidden_launch_20261007.json',{'status':'started_corrected_source_main_publication','identity':launch,'input_sha256':pins})
    monitor=A/'monitor_full_actual_optimization_until2355_v29_20261007.py'
    assert monitor.is_file()
    launch=start('actual_full_optimization_live_monitor_v29',monitor.name,[],{str(monitor):sha(monitor)})
    create(A/'actual_full_live_monitor_v29_hidden_launch_20261007.json',{'status':'started_live_monitor_with_signed132_and_administrative_defer_state','identity':launch})

if __name__=='__main__':main()

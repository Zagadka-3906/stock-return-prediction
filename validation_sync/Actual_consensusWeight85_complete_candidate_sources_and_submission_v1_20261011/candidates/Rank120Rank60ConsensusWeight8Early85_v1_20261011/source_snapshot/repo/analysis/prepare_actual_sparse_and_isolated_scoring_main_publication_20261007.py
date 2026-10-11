"""Prepare truthful main publication for actual new native bank and execution controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    sparse=A/'nonflag_SparseGram64_actual_native3_full37_cold111_controls_20261007.json'
    parallel=A/'actual_two_process_uncached_scoring_controls_20261007/verification.json'
    serial=A/'actual_paired_serial_uncached_scoring_controls_20261007/verification.json'
    assert read(sparse)['status']=='passed_actual_sparse_native3_full37_independent_CDF_and111_cold_controls'
    assert read(parallel)['actual_uncached_official_calls']==4 and read(serial)['actual_serial_uncached_official_calls']==4
    old=A/'publish_signed132_actual_import_recovery_main_20261007.py';new=A/'publish_actual_sparse_and_isolated_scoring_controls_main_20261007.py'
    text=old.read_text(encoding='utf8').replace('signed132_actual_import_recovery_github_20261007','actual_sparse_and_isolated_scoring_controls_github_20261007').replace('validation_sync/signed132_actual_import_recovery_20261007','validation_sync/actual_sparse_and_isolated_scoring_controls_20261007')
    begin=text.index('    proof_path=');end=text.index('    sources=list(dict.fromkeys(sources));',begin)
    source_paths=set(A.glob('*SparseGram*20261007.py'))|set(A.glob('*SparseGram*20261007.json'))|set(A.glob('*sparse_Gram*20261007.py'))|set(A.glob('*two_process*20261007.py'))|set(A.glob('*two_process*20261007.json'))|set(A.glob('*paired_serial*20261007.py'))|set(A.glob('*paired_serial*20261007.json'))
    for folder in [A/'nonflag_sparse_Gram64_actual_solver_controls_20261007',A/'nonflag_residual_SparseGram64_bank10_20261007',A/'nonflag_residual_SparseGram64_native_hook3_preflight_20261007',A/'nonflag_residual_SparseGram37_transform_preflight_20261007',parallel.parent,serial.parent]:
        source_paths.update(folder.rglob('*.json'))
        if 'SparseGram64_bank10' in folder.name:source_paths.update(folder.rglob('*.joblib'))
    for name in ['nonflag_residual_SparseGram64_native_bank10','nonflag_SparseGram64_actual_native3_full37_controls','actual_two_process_uncached_scoring_controls_queue','actual_isolated_official_worker2_slot0','actual_isolated_official_worker2_slot1','actual_paired_serial_official_controls_queue','actual_paired_serial_official_worker2_slot0','actual_paired_serial_official_worker2_slot1']:
        folder=A/'service_owned_workflows_20261006'/name
        assert read(folder/'service_execution.json')['status']=='passed',name
        source_paths.update(folder.glob('*.json'));source_paths.update(folder.glob('*.log'))
    source_paths={p for p in source_paths if p.is_file()}
    lines='\n'.join('      A/'+repr(p.relative_to(A).as_posix())+',' for p in sorted(source_paths))
    replacement="    proof_path=A/'actual_sparse_and_isolated_scoring_controls_publication_scope_20261007.json';proof=read(proof_path)\n    assert proof['status']=='actual_new_sparse10_solver2_native3_full37_cold111_and_parallel4_serial4_controls_passed'\n    sources=[Path(__file__),A/"+repr(Path(__file__).name)+",proof_path,\n"+lines+'\n    ]\n'
    text=text[:begin]+replacement+text[end:]
    begin=text.index("            payload[(prefix/'README.md').as_posix()]=");end=text.index('            scope.reverify()',begin)
    measured=read(serial)
    note='新增非涨停残差稀疏回归：L1和L1/L2两种成熟年度配方，10个真实模型均通过完整历史原生重载、独立解码及前缀检查；另有2项与sklearn的求解目标/KKT对照、3项原生CDF、37全量和111冷前缀控制。尚未完成其官方40项比较、完整未来候选或正式入选，不赋予排名。双进程隔离评分和匹配串行评分各4次，8指标、映射数值与完整CSV字节均一致；并行总耗时'+str(measured['parallel_process_wall_seconds'])+'秒，串行'+str(measured['serial_process_wall_seconds'])+'秒。后台负载会改变，不能视为通用提速保证；跨进程共享缓存未准入，当前正式搜索保留原顺序流程。只上传源码、模型参数和证明，不重复上传大特征与预测缓存。仅main，23:55停工，明早须实际用户继续。'
    text=text[:begin]+"            payload[(prefix/'README.md').as_posix()]=("+repr(note+'\n')+").encode('utf8')\n"+text[end:]
    text=text.replace('published_actual_signed132_import_recovery_preserving_all_original_sources','published_actual_sparse10_and_isolated_parallel4_serial4_controls').replace('保存反向融合实际导入引用修复及原始失败记录','保存稀疏残差实际10模型控制和隔离双进程串行评分对照')
    text=text.replace("'residual_sign':-1","'sparse_residual_sign':1,'actual_historical_execution_control_calls':8").replace("'completed_native_annual_fits_added':0","'completed_native_annual_fits_added':10")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),old,new,*sorted(source_paths)]}
    create(A/'actual_sparse_and_isolated_scoring_controls_publication_scope_20261007.json',{
      'status':'actual_new_sparse10_solver2_native3_full37_cold111_and_parallel4_serial4_controls_passed',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'new_native_fits':10,
      'new_quality_scores':0,'new_uncached_historical_official_execution_calls':8,
      'official_sparse_comparison_and_future_candidate_not_yet_claimed':True,'test_labels_read':False})
    print('Prepared actual sparse native and paired scoring publication; wait for safe main-publisher window',flush=True)

if __name__=='__main__':main()

"""Preserve measured GPU memory evidence and unexecuted manual benchmark plan on main."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'publish_signed132_actual_import_recovery_main_20261007.py';new=A/'publish_actual_GPU_shared_memory_and_manual_bench_plan_main_20261007.py'
    text=old.read_text(encoding='utf8').replace('signed132_actual_import_recovery_github_20261007','actual_GPU_shared_memory_and_manual_bench_plan_github_20261007').replace('validation_sync/signed132_actual_import_recovery_20261007','validation_sync/actual_GPU_shared_memory_and_manual_bench_plan_20261007')
    begin=text.index('    proof_path=');end=text.index('    sources=list(dict.fromkeys(sources));',begin)
    sources=[Path(__file__),A/'record_actual_GPU_memory_boundary_and_manual_bench_plan_20261007.py',A/'actual_neural_GPU_shared_memory_snapshot_20261007.json',A/'actual_GPU_shared_allocation_resource_boundary_20261007.json',A/'manual_next_run_GPU_speed_and_epoch_checkpoint_bench_plan_20261007.json',A/'actual_two_process_scoring_latency_interpretation_20261007.json',A/'record_actual_scoring_latency_limitations_20261007.py']
    replacement="    dependency=A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v2'\n    while not (dependency/'native_launch.json').exists() or owned(read(dependency/'native_launch.json')):\n        assert time.time()<datetime.fromisoformat('2026-10-07T23:35:00+08:00').timestamp();time.sleep(5)\n    assert read(dependency/'service_execution.json')['status']=='passed'\n    proof_path=A/'actual_GPU_shared_allocation_resource_boundary_20261007.json';proof=read(proof_path)\n    assert proof['status']=='measured_original16384_recipe_uses_Windows_shared_GPU_allocation_on_this_host'\n    sources=[Path(__file__),\n"+'\n'.join('      A/'+repr(p.name)+',' for p in sources)+'\n    ]\n'
    text=text[:begin]+replacement+text[end:]
    begin=text.index("            payload[(prefix/'README.md').as_posix()]=");end=text.index('            scope.reverify()',begin)
    note='强所有权核对后采样Windows WDDM GPU进程计数：原16384/8192/4096网络使用约10.53GiB专用与5.52GiB共享GPU内存。支持当前配方已使用共享分配；未测定其造成的时间惩罚、PCIe流量或CUDA峰值。原2021成熟年度实际拟合约40小时，旧训练器仅年度末落盘；已完成2020/2021参数保留，未落盘年度关机后不能恢复。预声明明早手动GPU检查：较小微批与梯度累积、BF16、TF32及逐epoch持久化，均属于新的浮点配方，GPU等价性与速度收益尚未测试，不混作原FP32权重。后台负载变化下的双进程/串行评分总耗时也不构成保证提速证据。没有新模型分数，没有声称可行方向穷尽。仅main，23:55停工，明早用户实际继续后执行。'
    text=text[:begin]+"            payload[(prefix/'README.md').as_posix()]=("+repr(note+'\n')+").encode('utf8')\n"+text[end:]
    text=text.replace('published_actual_signed132_import_recovery_preserving_all_original_sources','published_measured_GPU_shared_allocation_and_manual_unexecuted_speed_bench_plan').replace('保存反向融合实际导入引用修复及原始失败记录','保存原大网络GPU共享分配实测及明早手动提速检验计划')
    text=text.replace("'residual_sign':-1","'original_training_not_modified':True,'GPU_new_recipe_qualification_not_claimed':True")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [new,*sources]}
    row=start('actual_GPU_shared_allocation_and_manual_bench_main_publication',new.name,[],pins)
    create(A/'actual_GPU_resource_main_hidden_publication_launch_20261007.json',{'status':'started_hidden_resource_evidence_publication_after_sparse_controls_main','identity':row,'input_sha256':pins})

if __name__=='__main__':main()

"""Include the declined R97 adoption and its original failure in full publication."""
from pathlib import Path
import sys

A = Path(__file__).resolve().parent
sys.path.insert(0, str(A))


def main():
    original = A / 'publish_serial_cache_worker_controls_20261006.py'
    source = original.read_text(encoding='utf-8')
    old = '    sync = helpers.sync\n'
    assert source.count(old) == 1
    source = source.replace(old,
        "    sources += [A / 'publish_serial_cache_worker_controls_20261006.py',\n"
        "        A / 'prepare_root_cached_round97_dispatch_20261006.py',\n"
        "        A / 'handoff_root_cached_round97_dispatch_20261006.py',\n"
        "        A / 'root_cached_round97_dispatch_preparation_20261006.json',\n"
        "        A / 'root_cached_round97_dispatch_admission_20261006.json',\n"
        "        A / 'run_dependency_queue_v11_20261006.py',\n"
        "        A / 'monitor_actual_optimization_progress_v35_20261006.py',\n"
        "        A / 'run_joint_goss_quality_with_root_and_rank_cache_v4_20261006.py',\n"
        "        *(A / 'service_owned_workflows_20261006/root_cached_round97_dispatch_handoff').glob('*.json'),\n"
        "        *(A / 'service_owned_workflows_20261006/root_cached_round97_dispatch_handoff').glob('*.log')]\n"
        "    admission = read(A / 'root_cached_round97_dispatch_admission_20261006.json')\n"
        "    assert admission['runtime_adopted'] is False\n"
        "    assert not admission['new_queue11_started'] and not admission['new_observer35_started']\n"
        "    sync = helpers.sync\n")
    old = "            'launch证明实际等待进程、身份和空闲预约，execution保存自然结束后的完整结果或失败。'\n"
    assert source.count(old) == 1
    source = source.replace(old,
        "            '第97轮已于控制结束后按原队列自然启动，随后尝试的缓存接入被未启动检查拒绝。'\n"
        "            '原AssertionError、服务终态、准备源码与当前真实第97轮身份均保留；新队列11、观察器35未启动。'\n"
        "            '本结果证明实际控制通过，并不宣称第97轮已经采用根缓存；原151项继续执行，未停止或重启科学进程。\\n\\n'\n"
        "            'launch证明实际等待进程、身份和空闲预约，execution保存自然结束后的完整结果或失败。'\n")
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'serial_cache_worker_full_publication_v2'}
    exec(compile(source, str(Path(__file__).resolve()), 'exec'), namespace)
    namespace['main']('execution')


if __name__ == '__main__':
    main()

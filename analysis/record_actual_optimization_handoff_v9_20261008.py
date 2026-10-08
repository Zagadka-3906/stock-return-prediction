"""Immutable current four-round checkpoint; final qualification and feasible-direction bounds remain open."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    previous_path=A/'actual_optimization_handoff_v8_20261008.json';state=read(previous_path)
    progress=read(A/'actual_neural135_CrossFamily136_progress_v6_20261008.json')
    files=[Path(__file__),previous_path,A/'BF16reverse138_complete_hidden_launches_v1_20261008.json',
        A/'BF16reverse138_complete_dependency_plan_v1_20261008.json',A/'BF16reverse40_prospective_routes_v1_20261008.json',
        A/'BF16reverse138_model_count_contract_v1_20261008.json',A/'BF16reverse138_D_scoring_scope_v1_20261008.json',
        A/'BF16reverse138_prospective_scope_reference_recovery_v1_20261008.json',
        A/'actual_BF16reverse138_completed_CSV_archivist_hidden_launch_v1_20261008.json',
        A/'actual_optimization135136137138_progress_hidden_launch_v6_20261008.json',
        A/'monitor_neural135_CrossFamily136_Huber137_BF16reverse138_v6_20261008.py',
        A/'reverse_BF16_plan_handoff_main_v1_20261008/receipt.json']
    prospective=read(files[4]);assert prospective['prospective_sources']==24 and len(prospective['graph_controls'])==444
    assert len(prospective['baseline_gain_regressions'])==9 and len(prospective['model_count_sort_controls'])==6
    launches=read(files[2]);assert len(launches['launches'])==7
    services=state['actual_owned_live_services']
    for name,row in launches['launches'].items():
        assert owned(row) and row['actual_native_console_handle']==0,name
        services[name]={'round':138,'identity':row,'live':True}
        folder=A/'service_owned_workflows_20261006'/name;files += [folder/'native_launch.json',folder/'job_definition.json']
    for name,item in services.items():assert owned(item['identity']),name
    pins={str(p):sha(p) for p in files}
    state.update(status='active_four_complete_owned135v4_136v4_137v3_138v1_queues_after_actual_prospective_controls',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),input_sha256={**state['input_sha256'],**pins},
        actual_progress_at_checkpoint=progress,actual_owned_live_services=services,
        actual138_controls={'synthetic_CDF':39,'synthetic_day_prefixes':78,'prospective_sources':24,'complete_parent_graphs':444,
            'baseline_regressions':9,'same_score_unique_model_sort':6,'physical_model_reuse_expressions':8,
            'official_scope_paths':9,'new_official_scores':0,'actual_future_X_calls':0},
        still_required138=['Current seven-step138 queue1 is live; actual job names and future artifact names identify round138/QA49.',
            'Wait complete137 and exact best135136137 parent, then37 full5635800 transforms/111 cold and3 historical saved-neural native hooks.',
            'Admit all40 original official full8 scores; control and score evidence each publish main.',
            'Selected graph/config/Python source/return calibration frozen before new future features; final2025 model predicts2025 and2026.',
            'Two full1599600 native/independent replays and cold80 or honest exact qualified anchor reuse.',
            'Count distinct native payloadSHA union; reverse and positive branches can reuse the same neural model.',
            'Original six complete leaderboard views,45seconds QA49 and actual main fullboard receipt.'],
        remaining_uncovered_directions=['Huber+Ridge/RFF/Bayes mixtures are not yet predeclared or evaluated.'],
        actual138_launch_metadata={'actual_round':138,'actual_QA_version':49,
            'authoritative_job_names':list(launches['launches']),'legacy_launch_status_string':launches['status'],
            'future_canonical_registration':'analysis/optimization_20261003_r138/full_registration_execution.json'})
    output=A/'actual_optimization_handoff_v9_20261008.json';create(output,state)
    best=progress['best_fully_qualified'];epoch=progress['latest_actual_epoch']
    lines=['# 实际优化交接 v9','',f"记录时间：{state['at_local']}；截止：2026年10月10日23:59（UTC+8）。",'',
        f"当前完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；完整榜{progress['latest_fully_qualified']['connected_records']:,}条。",'',
        f"神经年度完成{len(progress['annual_models_complete'])}/6；当前已保存{epoch['year']}的{epoch['saved_epoch']}/{epoch['total_epochs']}轮。",'',
        '当前完整队列：135版本4；136版本4；137版本3、完整父控制版本4；138负向神经版本1。四轮全部评分、冻结、候选、完整榜QA和main流程已启动。',
        '这些队列的官方新分当前均为零；依赖完成后按顺序推进。训练损失和流程检查不记为官方质量提升。','',
        '第138轮实际通过：39合成/78单日前缀，24接收器/444完整父图，9基准/6同分排序，8模型SHA去重及9原始D/E评分范围检查。',
        '37完整5635800行/111冷前缀、3真实历史原生神经接入仍在等待合格137；它们和官方40比较、两次实际候选复核、QA49均未冒充完成。','',
        '实时进度：actual_neural135_CrossFamily136_progress_v6_20261008.md；大文件和输出在E，原官方缓存评分临时目录保留D。所有工作进程无原生控制台窗口。','',
        '继续完成135→136→137→138和仍未覆盖的Huber跨模型组合方向。当前目标继续进行，没有方向/资源穷尽证据；过期停工和被替代版本不恢复。','']
    target=A/'actual_optimization_handoff_v9_20261008.md';assert not target.exists();target.write_text('\n'.join(lines),encoding='utf8',newline='\n')
    for p,d in state['input_sha256'].items():assert sha(p)==d,p
    print('Current handoff9 records four live complete pipelines and their remaining scientific qualifications.',flush=True)


if __name__=='__main__':main()

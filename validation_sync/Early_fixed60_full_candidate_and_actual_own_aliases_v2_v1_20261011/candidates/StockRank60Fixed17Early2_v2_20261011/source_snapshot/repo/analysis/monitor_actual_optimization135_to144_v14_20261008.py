"""Observe corrected143 sealing, true latest publication chronology and actual eight-alpha progress."""
from pathlib import Path
from datetime import datetime
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write
from monitor_actual_optimization135_to143_v13_20261008 import services
def main():
    fixes=read(A/'ConeRidgeFine143_E_snapshot_sealing_hidden_launches_v2_20261008.json')['launches']
    alpha=read(A/'ConeRidgeAlpha8_actual_controls_hidden_launches_v2_20261008.json')['launches']
    while True:
        state=read(A/'actual_optimization135_to143_progress_v13_20261008.json')
        state.update(observer_version=14,at_local=datetime.now().isoformat(timespec='seconds'))
        state['actual143_registration_recovery_services']=services(fixes)
        state['actual143_passed_inference_preserved_during_E_evidence_path_recovery']=True
        state['actual_alpha8_services']=services(alpha)
        population=Path('E:/赛题五_本机临时/nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008')
        q={'actual_synthetic_native_fits':24,'actual_synthetic_prefix_controls':144,
            'actual200003_probe_fits':8,'actual200003_prefix_controls':48,
            'actual_completed_annual_fits':len(list(population.glob('*/info_*.json'))),'expected_annual_fits':40,
            'actual_completed_causal_refits':0,'expected_causal_refits':40,'new_official_scores':0}
        if (population/'actual_stage.json').exists():q['stage']=read(population/'actual_stage.json')
        if (population/'verification.json').exists():q['full_bank_passed']=read(population/'verification.json')['actual_native_fits']==40
        causal=Path('E:/赛题五_本机临时/ConeRidgeAlpha40_causal_refit_v2_20261008')
        q['actual_completed_causal_refits']=len(list(causal.glob('control*.json')))
        if (causal/'verification.json').exists():q['full_causal_controls_passed']=read(causal/'verification.json')['actual_causal_same_configuration_refit_controls']==40
        state['actual_alpha8_controls']=q
        state['actual144_plan']={'expected_records':100,'expected_new_cases':96,'current_quality_scores':0,
            'distinct_outer_alpha_stage_preserves_complete_inner_Cone143_parent':True,'actual_adapter_contracts':9,
            'actual40_bank40_causal_current_parent97full291cold48native48calendar_and_complete100_queue_still_required':True}
        qualified=[]
        for n in range(128,145):
            full=A/f'optimization_20261003_r{n}/full_registration_execution.json';receipt=A/f'github_validation_sync_main_20261005/round{n}_receipt.json'
            if not (full.exists() and receipt.exists()):continue
            r=read(receipt)
            if read(full)['status']!='passed' or r['status']!='pushed_and_remote_head_verified' or r['branch']!='main':continue
            proof=read(ROOT/f'candidates/optimization_20261003_r{n}/verification.json')
            physical=len({p['sha256'] for p in proof['models'].values()})
            qualified.append({'round':n,'official_score':r['official_score'],'connected_records':r['connected_records'],
                'main_commit':r['commit'],'publication_at_local':r['at_local'],'physical_models':physical})
        if qualified:
            state['best_fully_qualified']=min(qualified,key=lambda x:(-x['official_score'],x['physical_models'],x['round']))
            state['latest_fully_qualified']=max(qualified,key=lambda x:(x['publication_at_local'],x['round']))
        state['all_fully_qualified_rounds_at_observation']=qualified
        write(A/'actual_optimization135_to144_progress_v14_20261008.json',state)
        best=state['best_fully_qualified'];e=state['latest_actual_epoch'];f=state['actual143_quality']
        lines=['# 本机优化实际进度','',f"更新：{state['at_local']}；截止2026-10-10 23:59。",'',
          f"完整合格最佳：第{best['round']}轮，S={best['official_score']:.12f}；最近完成的榜单{state['latest_fully_qualified']['connected_records']:,}条。",'',
          f"神经年度完成{len(state['annual_models_complete'])}/6，最终年度{e['completed_epoch']}/{e['total_epochs']}轮。",'',
          f"第143轮官方评分{f['completed_records']}/68；最高S={f.get('best_score_so_far',0):.12f}。完整合格：{f['fully_qualified']}。",
          '原生/独立两次1,599,600行与冷80已经通过；E盘冻结元数据的封装路径用来源2修复，旧失败保留。', '',
          f"新增8个参数头：24合成/144前缀、8真实200003行探针/48前缀通过；完整年度拟合{q['actual_completed_annual_fits']}/40，因果重训{q['actual_completed_causal_refits']}/40。",
          '第144轮计划100项，保留第143轮完整图再追加独立参数阶段；9个实际接入合同通过。实际100项评分尚未执行。', '',
          '第135至141继续既有队列，第137至141的来源11登记修复已经通过完整预演。',
          '所有选模只用TRAIN、连续向前验证和官方八指标。大文件E、原评分目录D。目标active，未证明全局穷尽。','']
        p=A/'actual_optimization135_to144_progress_v14_20261008.md';part=p.with_suffix('.md.part');part.write_text('\n'.join(lines),encoding='utf8',newline='\n');part.replace(p);time.sleep(10)
if __name__=='__main__':main()

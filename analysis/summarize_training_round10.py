"""Publish the completed retention-priority experiment and reproducibility evidence."""
from pathlib import Path
import sys
import json
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from optimize_training_round10 import OUT,PREVIOUS,WAVES,read,dump,sha


def main():
    selection=read(OUT/'selection.json');winner=selection['winner']
    validation=read(OUT/'causal_validation.json');csv=read(OUT/'calibrated_csv_official.json')
    candidate=ROOT/'candidates/optimization_20261003_r10';prediction=read(candidate/'verification.json')
    nonzero=read(OUT/'nonzero_priority_causal_checks.json')
    assert validation['status']==csv['status']==prediction['status']==nonzero['status']=='passed'
    assert sha(candidate/'submission.csv')==prediction['csv_sha256'] and prediction['old_delivery_pointer_unchanged']
    baseline=read(PREVIOUS/'selection.json')['winner']['metrics']
    changes={k:winner['metrics'][k]-baseline[k] for k in ('ic_mean','annual_excess','mean_turnover')}
    contributions={'RankIC':.4*changes['ic_mean'],'annual_excess':.3*changes['annual_excess'],'turnover':-.3*changes['mean_turnover']}
    assert abs(sum(contributions.values())-selection['score_gain'])<1e-12
    counts={str(w):len(read(OUT/f'wave{w}_results.json')['results']) for w in WAVES}
    total=sum(counts.values());assert total==35
    unique=len({tuple(r[k] for k in ('add_priority_weight','drop_priority_weight','retention','limit_up_delta'))
                for r in selection['ranking']})
    coarse=read(OUT/'wave68_results.json')['results']
    mode_best={mode:max((dict(arm=k,**v) for k,v in coarse.items() if k.startswith(mode)),
                       key=lambda r:r['connected_final_score']) for mode in ('add','drop','both')}
    result={'status':'complete','scope':'waves68–70','winner':winner,'baseline_score':selection['baseline_score'],
            'score_gain':selection['score_gain'],'scored_records':total,'records_per_wave':counts,
            'distinct_output_configurations':unique,'repeat_records':total-unique,
            'total_scored_records_including_repeats':1265+total,'new_fold_models_trained':0,
            'retention_priority_signal':'top_orderer_daily_rank',
            'add_priority_weight':winner['add_priority_weight'],'drop_priority_weight':winner['drop_priority_weight'],
            'coarse_best_by_mode':mode_best,'pruned_member_excluded':True,
            'metric_change_vs_baseline':changes,'score_contributions_vs_baseline':contributions,
            'component_audit':read(OUT/'component_audit.json'),'validation':validation,'nonzero_priority_causal_checks':nonzero,
            'calibrated_written_csv':csv,'prediction':prediction,'candidate_submission':str(candidate/'submission.csv'),
            'test_labels_read_this_round':False,'test_score_of_this_candidate':None,
            'candidate_matches_previous_csv':prediction['csv_sha256']==read(ROOT/'candidates/optimization_20261003_r9/verification.json')['csv_sha256'],
            'old_deliveries_preserved':True,'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
            'followup_directions':['Refine the learned priority signal separately for additions and removals.',
                                  'Refine member weights separately inside each selected role ensemble.',
                                  'Evaluate new TopK checkpoints against the selected role pipeline.']}
    dump(ROOT/'results/optimization_20261003_r10.json',result)
    dump(ROOT/'results/optimization_ranking_20261003_r10.json',{'status':'complete','ranking':selection['ranking']})
    dump(candidate/'manifest.json',{'status':'passed','files':{p.relative_to(candidate).as_posix():
         {'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(candidate.rglob('*')) if p.is_file() and p.name!='manifest.json'}})
    readme=ROOT/'README.md';heading='### 第十轮：留存补入与剔除独立优先级（波68–70）'
    text=readme.read_text(encoding='utf-8-sig')
    if heading not in text:
        outcome=f"提高 **{selection['score_gain']:.12f}**" if selection['score_gain']>0 else '本轮没有获得提升，原方案仍为最高分'
        note=f'''\n\n{heading}\n\n本轮完成{total}条完整方案评分，测试只改变留存补入、只改变新股票剔除、同时改变两者，以及局部权重和留存参数细调。前轮基准{selection['baseline_score']:.12f}，最高连续验证分 **{winner['connected_final_score']:.12f}**，{outcome}。补入优先级收益排序权重{winner['add_priority_weight']:g}，剔除优先级权重{winner['drop_priority_weight']:g}，留存{winner['retention']:g}，涨停偏移{winner['limit_up_delta']:g}。\n\n零优先级权重完整复现R9输出，每日Top组大小、股票唯一性和留存下限均检查。成熟过去标签收益校准、实际CSV官方评分、三个日期前缀不变性、测试X模型重载和全管线重放、CSV键值和秩往返检查均通过。候选为 `candidates/optimization_20261003_r10/submission.csv`；本轮未读取测试标签，未产生新测试分，正式交付指针和历史候选保留。完整榜包含1,300条评分记录，含重复对照，并分别披露旧管线已知限制。\n'''
        readme.write_text(text.rstrip()+note,encoding='utf-8')
    print(json.dumps({'score':winner['connected_final_score'],'gain':selection['score_gain'],'records':total,
                      'add':winner['add_priority_weight'],'drop':winner['drop_priority_weight'],
                      'candidate':str(candidate/'submission.csv')},ensure_ascii=False,indent=2))


if __name__=='__main__':main()

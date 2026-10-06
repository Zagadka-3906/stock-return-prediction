"""Publish completed independent-role optimization evidence."""
from pathlib import Path
import sys
import json
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from optimize_training_round9 import OUT,PREVIOUS,WAVES,read,dump,sha


def main():
    selection=read(OUT/'selection.json');winner=selection['winner']
    validation=read(OUT/'causal_validation.json');csv=read(OUT/'calibrated_csv_official.json')
    candidate=ROOT/'candidates/optimization_20261003_r9';prediction=read(candidate/'verification.json')
    assert validation['status']==csv['status']==prediction['status']=='passed'
    assert sha(candidate/'submission.csv')==prediction['csv_sha256'] and prediction['old_delivery_pointer_unchanged']
    baseline=read(PREVIOUS/'selection.json')['winner']['metrics']
    changes={k:winner['metrics'][k]-baseline[k] for k in ('ic_mean','annual_excess','mean_turnover')}
    contributions={'RankIC':.4*changes['ic_mean'],'annual_excess':.3*changes['annual_excess'],'turnover':-.3*changes['mean_turnover']}
    assert abs(sum(contributions.values())-selection['score_gain'])<1e-12
    counts={str(w):len(read(OUT/f'wave{w}_results.json')['results']) for w in WAVES}
    total=sum(counts.values());assert total==33
    result={'status':'complete','scope':'waves65–67','winner':winner,'baseline_score':selection['baseline_score'],
            'score_gain':selection['score_gain'],'scored_records':total,'records_per_wave':counts,
            'total_scored_records_including_repeats':1232+total,'new_fold_models_trained':0,
            'role_ensembles_split':winner['role_ensembles_split'],'top_ensemble_weights':winner['top_ensemble_weights'],
            'rest_ensemble_weights':winner['ensemble_weights'],'pruned_member_excluded':True,
            'metric_change_vs_baseline':changes,'score_contributions_vs_baseline':contributions,
            'component_audit':read(OUT/'component_audit.json'),'validation':validation,
            'calibrated_written_csv':csv,'prediction':prediction,'candidate_submission':str(candidate/'submission.csv'),
            'test_labels_read_this_round':False,'test_score_of_this_candidate':None,
            'old_deliveries_preserved':True,'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
            'followup_directions':['Test causal hold/drop/add selection rules without altering the official objective.',
                                  'Refine member weights separately inside each selected role ensemble.',
                                  'Evaluate new TopK checkpoints against the selected role pipeline.']}
    dump(ROOT/'results/optimization_20261003_r9.json',result)
    dump(ROOT/'results/optimization_ranking_20261003_r9.json',{'status':'complete','ranking':selection['ranking']})
    dump(candidate/'manifest.json',{'status':'passed','files':{p.relative_to(candidate).as_posix():
         {'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(candidate.rglob('*')) if p.is_file() and p.name!='manifest.json'}})
    readme=ROOT/'README.md';heading='### 第九轮：Top与其余股票独立排序集成（波65–67）'
    text=readme.read_text(encoding='utf-8-sig')
    if heading not in text:
        note=f'''\n\n{heading}\n\n本轮完成{total}条完整方案评分，全部排除旧剪枝成员。前轮基准{selection['baseline_score']:.12f}，最高连续验证分 **{winner['connected_final_score']:.12f}**，提高 **{selection['score_gain']:.12f}**。Top组成员相对权重 `{winner['top_ensemble_weights']}`，其余股票权重 `{winner['ensemble_weights']}`；slow16排序权重为{winner['top_slow_weight']:g}/{winner['slow16_weight']:g}，留存{winner['retention']:g}，涨停偏移{winner['limit_up_delta']:g}。\n\n原R8完整输出逐元素复现。成熟过去标签收益校准、实际CSV官方评分、三个日期前缀不变性、测试X模型重载和全管线重放、CSV键值和秩往返检查均通过。新候选为 `candidates/optimization_20261003_r9/submission.csv`；本轮未读取测试标签，未产生新测试分，正式交付指针和历史候选保留。\n'''
        readme.write_text(text.rstrip()+note,encoding='utf-8')
    print(json.dumps({'score':winner['connected_final_score'],'gain':selection['score_gain'],'records':total,
                      'candidate':str(candidate/'submission.csv')},ensure_ascii=False,indent=2))


if __name__=='__main__':main()

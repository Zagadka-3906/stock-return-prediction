"""Publish sequential independent-membership optimization and final artifacts."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from optimize_training_round12 import OUT,PREVIOUS,WAVES,signature,read,dump,sha


def main():
    selection=read(OUT/'selection.json');winner=selection['winner']
    validation=read(OUT/'causal_validation.json');csv=read(OUT/'calibrated_csv_official.json')
    checks=read(OUT/'independent_membership_causal_checks.json')
    candidate=ROOT/'candidates/optimization_20261003_r12';prediction=read(candidate/'verification.json')
    assert validation['status']==csv['status']==checks['status']==prediction['status']=='passed'
    assert sha(candidate/'submission.csv')==prediction['csv_sha256'] and prediction['old_delivery_pointer_unchanged']
    prior=read(PREVIOUS/'selection.json')['winner']['metrics']
    changes={k:winner['metrics'][k]-prior[k] for k in ('ic_mean','annual_excess','mean_turnover')}
    contributions={'RankIC':.4*changes['ic_mean'],'annual_excess':.3*changes['annual_excess'],'turnover':-.3*changes['mean_turnover']}
    assert abs(sum(contributions.values())-selection['score_gain'])<1e-12
    counts={str(w):len(read(OUT/f'wave{w}_results.json')['results']) for w in WAVES}
    total=sum(counts.values());assert total==70
    unique=len({signature(r) for r in selection['ranking']});stages=[];running=selection['baseline_score']
    labels=('持仓融合权重粗搜与细搜','独立持仓排序器及其slow16权重','TopK轮次配比与后处理','排序、融合、留存和涨停偏移细调')
    for wave,label in zip(WAVES,labels):
        payload=read(OUT/f'wave{wave}_results.json');key,row=max(payload['results'].items(),key=lambda p:p[1]['connected_final_score'])
        previous_score=running;running=max(running,row['connected_final_score'])
        stages.append({'wave':wave,'stage':label,'scored_records':len(payload['results']),'best_arm':key,
                       'best_scored_configuration':row,'cumulative_best':running,'gain_from_previous_stage':running-previous_score})
    result={'status':'complete','scope':'waves77–80','winner':winner,'baseline_score':selection['baseline_score'],
            'score_gain':selection['score_gain'],'sequential_stage_results':stages,'scored_records':total,
            'records_per_wave':counts,'distinct_output_configurations':unique,'repeat_records':total-unique,
            'total_scored_records_including_repeats':1375+total,'new_fold_models_trained':0,
            'membership_independent_from_return_ordering':True,'pruned_member_excluded':True,
            'metric_change_vs_baseline':changes,'score_contributions_vs_baseline':contributions,
            'component_audit':read(OUT/'component_audit.json'),'validation':validation,
            'calibrated_written_csv':csv,'independent_membership_causal_checks':checks,'prediction':prediction,
            'candidate_submission':str(candidate/'submission.csv'),'test_labels_read_this_round':False,
            'test_score_of_this_candidate':None,'old_deliveries_preserved':True,
            'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True}
    dump(ROOT/'results/optimization_20261003_r12.json',result)
    dump(ROOT/'results/optimization_ranking_20261003_r12.json',{'status':'complete','ranking':selection['ranking']})
    dump(candidate/'manifest.json',{'status':'passed','files':{p.relative_to(candidate).as_posix():
         {'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(candidate.rglob('*')) if p.is_file() and p.name!='manifest.json'}})
    write_prose(result)
    print(json.dumps({'score':winner['connected_final_score'],'gain':selection['score_gain'],'records':total,
                      'distinct_configurations':unique,'membership_ensemble':winner['membership_ensemble_name'],
                      'membership_weight':winner['membership_w5a_weight']},ensure_ascii=False,indent=2))


def write_prose(result):
    winner=result['winner'];outcome=f"提升 **{result['score_gain']:.12f}**" if result['score_gain']>0 else '本轮未获得提升，原方案仍为最高分'
    rows='\n'.join(f"| {s['stage']} | {s['scored_records']} | {s['cumulative_best']:.9f} | {s['gain_from_previous_stage']:+.9f} |" for s in result['sequential_stage_results'])
    detail=f'''# 第十二轮：独立持仓排序器与TopK细调\n\nR11基准为 {result['baseline_score']:.12f}。本轮完成{result['distinct_output_configurations']}种不同配置、{result['scored_records']}条评分记录；最高连续验证分 **{winner['connected_final_score']:.12f}**，{outcome}。\n\n各阶段沿用此前最高分设置。以下为截至阶段结束的最高分，阶段差异不应解释为独立因果贡献。\n\n| 阶段 | 评分记录 | 累计最高分 | 相比前阶段变化 |\n| --- | ---: | ---: | ---: |\n{rows}\n\n选中持仓模型权重 `{winner['membership_ensemble_weights']}`，持仓排序中slow16权重{winner['membership_slow_weight']:g}，持仓融合权重{winner['membership_w5a_weight']:g}。Top收益排序权重 `{winner['top_ensemble_weights']}`，其余股票排序权重 `{winner['ensemble_weights']}`；两者slow16权重为{winner['top_slow_weight']:g}/{winner['slow16_weight']:g}。TopK 90轮占比{winner['recipe']['components'][0]['weight']:g}，后处理 `{winner['recipe']['postprocessing']}`；留存{winner['retention']:g}，涨停偏移{winner['limit_up_delta']:g}。\n\n采用2020—2024逐年向前验证，连接1,212日、5,635,800行，年度边界换手连续计算。完整基准逐元素复现、成熟过去标签收益映射、实际验证CSV官方评分、重新构建的TopK日期前缀、独立持仓规则标签置空、模型重载、预测重放及CSV键值和秩检查全部通过。未读取测试标签、未打新测试分；所用验证年份此前均已查看，反复选模偏差未校正。\n\n完整参数及逐条评分见 `optimization_20261003_r12.json` 与 `optimization_ranking_20261003_r12.json`。候选为 `candidates/optimization_20261003_r12/submission.csv`。正式交付指针和历史候选保留，完整榜已更新至{result['total_scored_records_including_repeats']:,}条评分。\n'''
    baseline=read(PREVIOUS/'selection.json')['winner']['metrics'];metrics=winner['metrics']
    metric_rows=f"| Rank IC | {baseline['ic_mean']:.9f} | {metrics['ic_mean']:.9f} | {metrics['ic_mean']-baseline['ic_mean']:+.9f} |\n"
    for key,label in (('annual_excess','年化超额收益'),('mean_turnover','平均换手率')):
        metric_rows+=f"| {label} | {baseline[key]:.6%} | {metrics[key]:.6%} | {100*(metrics[key]-baseline[key]):+.6f}个百分点 |\n"
    detail=detail.replace('\n选中持仓模型权重', '\n本轮复用已经审计的样本外模型预测，未重新训练基础模型。\n\n| 指标 | R11基准 | 本轮选中方案 | 变化 |\n| --- | ---: | ---: | ---: |\n'+metric_rows+'\n选中持仓模型权重')
    (ROOT/'results/optimization_20261003_r12.md').write_text(detail,encoding='utf-8')
    readme=ROOT/'README.md';heading='### 第十二轮：独立持仓排序器与TopK细调（波77–80）';current=readme.read_text(encoding='utf-8-sig')
    if heading not in current:
        note=f'''\n\n{heading}\n\n本轮分离持仓与收益排序器，搜索持仓融合权重、独立模型组合、TopK轮次配比和后处理及输出参数。完成{result['distinct_output_configurations']}种配置、70条评分；前轮基准{result['baseline_score']:.12f}，最高连续验证分 **{winner['connected_final_score']:.12f}**，{outcome}。\n\n重建TopK前缀与因果检查、实际CSV官方评分、测试X预测重放和CSV秩检查均通过。本轮未读取测试标签，正式交付指针保留。详见 [第十二轮报告](results/optimization_20261003_r12.md)，候选为 `candidates/optimization_20261003_r12/submission.csv`。\n'''
        readme.write_text(current.rstrip()+note,encoding='utf-8')


if __name__=='__main__':main()

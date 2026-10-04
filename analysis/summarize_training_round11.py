"""Report four independently tested methods, their interactions and final artifacts."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from optimize_training_round11 import OUT,PREVIOUS,WAVES,FIELDS,baseline,signature,best,read,dump,sha


def main():
    selection=read(OUT/'selection.json');winner=selection['winner']
    validation=read(OUT/'causal_validation.json');csv=read(OUT/'calibrated_csv_official.json')
    checks=read(OUT/'nonzero_method_causal_checks.json')
    candidate=ROOT/'candidates/optimization_20261003_r11';prediction=read(candidate/'verification.json')
    assert validation['status']==csv['status']==checks['status']==prediction['status']=='passed'
    assert sha(candidate/'submission.csv')==prediction['csv_sha256'] and prediction['old_delivery_pointer_unchanged']
    prior=read(PREVIOUS/'selection.json')['winner']['metrics']
    changes={k:winner['metrics'][k]-prior[k] for k in ('ic_mean','annual_excess','mean_turnover')}
    contributions={'RankIC':.4*changes['ic_mean'],'annual_excess':.3*changes['annual_excess'],'turnover':-.3*changes['mean_turnover']}
    assert abs(sum(contributions.values())-selection['score_gain'])<1e-12
    methods=[]
    labels=('Top/其余股票分别细调模型权重','Top/其余股票分别调整slow16排序权重','更换留存补入与剔除信号','持仓信号融合')
    for wave,label in zip((71,72,73,74),labels):
        rows=list(read(OUT/f'wave{wave}_results.json')['results'].values())
        selected=best(rows);alternatives=[r for r in rows if signature(r)!=signature(baseline())]
        alternative=best(alternatives)
        methods.append({'wave':wave,'method':label,'scored_records':len(rows),'best_including_control':selected,
                        'best_changed_configuration':alternative,
                        'best_changed_gain':alternative['connected_final_score']-selection['baseline_score'],
                        'best_gain':selected['connected_final_score']-selection['baseline_score']})
    counts={str(w):len(read(OUT/f'wave{w}_results.json')['results']) for w in WAVES}
    total=sum(counts.values());unique=len({signature(r) for r in selection['ranking']})
    result={'status':'complete','scope':'waves71–76','winner':winner,'baseline_score':selection['baseline_score'],
            'score_gain':selection['score_gain'],'methods_independently_compared_to_same_baseline':methods,
            'combination_protocol':read(OUT/'combination_protocol.json'),
            'scored_records':total,'records_per_wave':counts,'distinct_output_configurations':unique,
            'repeat_records':total-unique,'total_scored_records_including_repeats':1300+total,
            'new_fold_models_trained':0,'pruned_member_excluded':True,
            'metric_change_vs_baseline':changes,'score_contributions_vs_baseline':contributions,
            'component_audit':read(OUT/'component_audit.json'),'validation':validation,
            'calibrated_written_csv':csv,'nonzero_method_causal_checks':checks,'prediction':prediction,
            'candidate_submission':str(candidate/'submission.csv'),'test_labels_read_this_round':False,
            'test_score_of_this_candidate':None,'old_deliveries_preserved':True,
            'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True}
    dump(ROOT/'results/optimization_20261003_r11.json',result)
    dump(ROOT/'results/optimization_ranking_20261003_r11.json',{'status':'complete','ranking':selection['ranking']})
    dump(candidate/'manifest.json',{'status':'passed','files':{p.relative_to(candidate).as_posix():
         {'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(candidate.rglob('*')) if p.is_file() and p.name!='manifest.json'}})
    text='\n'.join(f"| {m['method']} | {m['scored_records']} | {m['best_changed_configuration']['connected_final_score']:.9f} | {m['best_changed_gain']:+.9f} |" for m in methods)
    outcome=f"提升 **{selection['score_gain']:.12f}**" if selection['score_gain']>0 else '本轮未获得提升，保留原最高分方案'
    detail=f'''# 第十一轮：四方向优化与实测\n\n基准为R10/R9连续验证分 {selection['baseline_score']:.12f}。本轮共{unique}种不同配置、{total}条评分记录，含{total-unique}条重复对照。最高分 **{winner['connected_final_score']:.12f}**，{outcome}。\n\n四个方向均独立从相同基准出发。下表展示每个方向最佳变更配置，排除原设置对照。\n\n| 方法 | 评分记录 | 最佳变更配置得分 | 对基准变化 |\n| --- | ---: | ---: | ---: |\n{text}\n\n组合搜索将四个方向最佳设置按开/关组合，删除配置完全相同的重复组合；随后微调留存与涨停偏移。具体参数、指标和每条评分见 `optimization_20261003_r11.json` 与 `optimization_ranking_20261003_r11.json`。\n\n采用2020—2024逐年向前验证，连接1,212个交易日、5,635,800行，年度边界换手连续计算。重建对照、成熟过去标签收益校准、实际验证CSV官方评分、未来日期追加前缀不变性、非零规则标签置空、模型重载、完整预测重放与CSV键值和秩往返检查均通过。未读取测试标签，未产生新测试分；所用验证年份此前均已查看，反复选模偏差未校正。\n\n候选：`candidates/optimization_20261003_r11/submission.csv`。正式交付指针与历史候选保留。完整榜现包含{1300+total:,}条评分记录。\n'''
    (ROOT/'results/optimization_20261003_r11.md').write_text(detail,encoding='utf-8')
    readme=ROOT/'README.md';heading='### 第十一轮：四方向优化与组合测试（波71–76）'
    current=readme.read_text(encoding='utf-8-sig')
    if heading not in current:
        note=f'''\n\n{heading}\n\n本轮分别测试两组模型权重、slow16排序权重、留存优先级信号和持仓信号融合，再测试各方向最优设置的组合及留存、涨停偏移细调。完成{unique}种不同配置、{total}条评分记录；前轮基准{selection['baseline_score']:.12f}，最高连续验证分 **{winner['connected_final_score']:.12f}**，{outcome}。\n\n因果检查、实际验证CSV官方评分和测试X预测重放全部通过；未读取测试标签，未产生新测试分，正式交付指针保留。各方向比较见 [第十一轮报告](results/optimization_20261003_r11.md)，候选为 `candidates/optimization_20261003_r11/submission.csv`。\n'''
        readme.write_text(current.rstrip()+note,encoding='utf-8')
    print(json.dumps({'score':winner['connected_final_score'],'gain':selection['score_gain'],'records':total,
                      'distinct_configurations':unique,'methods':[{'method':m['method'],'gain':m['best_gain']} for m in methods]},ensure_ascii=False,indent=2))


if __name__=='__main__':main()

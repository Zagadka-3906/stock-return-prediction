"""Publish a completed, causally checked round without reading test labels."""
from pathlib import Path
import argparse
import importlib
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def publish(number,label,check_name,stage_labels):
    module=importlib.import_module(f'optimize_training_round{number}')
    release=importlib.import_module(f'finalize_training_round{number}')
    parent_number=module.PREVIOUS_NUMBER
    selection=release.selected();winner=selection['winner'];folder=module.OUT
    read,dump,sha=module.read,module.dump,module.sha
    validation=read(folder/'causal_validation.json');written=read(folder/'calibrated_csv_official.json')
    checks=read(folder/check_name);candidate=ROOT/f'candidates/optimization_20261003_r{number}'
    prediction=read(candidate/'verification.json')
    assert all(p['status']=='passed' for p in (validation,written,checks,prediction))
    assert prediction['old_delivery_pointer_unchanged'] and not prediction['test_labels_read']
    assert sha(candidate/'submission.csv')==prediction['csv_sha256']
    waves=list(module.WAVES);counts={str(w):len(read(folder/f'wave{w}_results.json')['results']) for w in waves}
    total=sum(counts.values());assert total==read(folder/'protocol.json')['expected_scored_records']
    unique=len({module.signature(row) for row in selection['ranking']})
    cached_rows=[row for row in selection['ranking'] if 'official_score_cache' in row]
    cache_hits=sum(row['official_score_cache']['cache_hit'] for row in cached_rows)
    for row in cached_rows:
        source=Path(row['official_score_cache']['official_metrics_source'])
        key=source.relative_to(ROOT).as_posix() if source.is_relative_to(ROOT) else str(source)
        frozen=selection['frozen_sha256'] if source.is_relative_to(ROOT) else selection['frozen_external_input_sha256']
        assert key in frozen and sha(source)==frozen[key],source
        assert read(source)['metrics']==row['metrics']
    score_reuse={'records_with_cache_provenance':len(cached_rows),'identical_csv_reuse_records':cache_hits,
                 'fresh_official_evaluations_in_scored_records':len(cached_rows)-cache_hits,
                 'distinct_csv_scoring_input_capsules':len({row['official_score_cache']['cache_key'] for row in cached_rows})}
    recovery=read(folder/'calibration_cache_recovery.json') if (folder/'calibration_cache_recovery.json').exists() else None
    if recovery:
        assert recovery['status']=='passed' and recovery['frozen_recipe_and_source_files_unchanged']
        assert recovery['original_selection_sha256']==sha(folder/'selection.json')
        assert recovery['selected_forecast_sha256']==sha(folder/'selected_validation.npy')
    previous=read(module.PREVIOUS/'selection.json')['winner']['metrics']
    change={k:winner['metrics'][k]-previous[k] for k in ('ic_mean','annual_excess','mean_turnover')}
    contributions={'RankIC':.4*change['ic_mean'],'annual_excess':.3*change['annual_excess'],'turnover':-.3*change['mean_turnover']}
    assert abs(sum(contributions.values())-selection['score_gain'])<1e-12
    assert abs(written['metrics']['final_score']-winner['connected_final_score'])<1e-12
    assert len(stage_labels)==len(waves)
    stages=[];running=selection['baseline_score']
    for wave,name in zip(waves,stage_labels):
        payload=read(folder/f'wave{wave}_results.json');assert payload['status']=='complete'
        arm,row=max(payload['results'].items(),key=lambda kv:kv[1]['connected_final_score'])
        before=running;running=max(running,row['connected_final_score'])
        stages.append({'wave':wave,'stage':name,'scored_records':len(payload['results']),
                       'best_arm':arm,'best_scored_configuration':row,'cumulative_best':running,'gain_from_previous_stage':running-before})
    new_training=read(folder/'protocol.json').get('new_model_training',False)
    result={'status':'complete','round':number,'explicit_parent_round':parent_number,'independent_comparison_branch':True,'round_label':label,'waves':waves,'winner':winner,
            'baseline_score':selection['baseline_score'],'score_gain':selection['score_gain'],
            'sequential_stage_results':stages,'scored_records':total,'records_per_wave':counts,
            'distinct_output_configurations':unique,'repeat_records':total-unique,
            'official_score_reuse':score_reuse,
            'calibration_cache_recovery':recovery,
            'new_fold_model_training':new_training,'metric_change_vs_baseline':change,
            'score_contributions_vs_baseline':contributions,'component_audit':read(folder/'component_audit.json'),
            'validation':validation,'calibrated_written_csv':written,'method_causal_checks':checks,
            'prediction':prediction,'candidate_submission':str(candidate/'submission.csv'),
            'test_labels_read_this_round':False,'test_score_of_this_candidate':None,
            'old_deliveries_preserved':True,'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True}
    dump(candidate/'manifest.json',{'status':'passed','files':{p.relative_to(candidate).as_posix():
         {'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(candidate.rglob('*')) if p.is_file() and p.name!='manifest.json'}})
    dump(ROOT/f'results/optimization_20261003_r{number}.json',result)
    dump(ROOT/f'results/optimization_ranking_20261003_r{number}.json',{'status':'complete','ranking':selection['ranking']})
    outcome=f"提升 **{selection['score_gain']:.12f}**" if selection['score_gain']>0 else '未获得提升，最高分仍由原方案取得'
    stage_table='\n'.join(f"| {s['stage']} | {s['scored_records']} | {s['cumulative_best']:.9f} | {s['gain_from_previous_stage']:+.9f} |" for s in stages)
    metric_rows=f"| Rank IC | {previous['ic_mean']:.9f} | {winner['metrics']['ic_mean']:.9f} | {change['ic_mean']:+.9f} |\n"
    for key,name in (('annual_excess','年化超额收益'),('mean_turnover','平均换手率')):
        metric_rows+=f"| {name} | {previous[key]:.6%} | {winner['metrics'][key]:.6%} | {100*change[key]:+.6f}个百分点 |\n"
    configuration=json.dumps(module.configuration(winner),ensure_ascii=False,indent=2)
    cache_note=(f"本轮评分记录中，{len(cached_rows)-cache_hits}次重新调用官方评分，{cache_hits}次复用完全相同CSV及验证输入的已有官方结果。CSV、验证数据、评分代码和运行库版本共同确定缓存；对应证据已随选定方案冻结。" if cached_rows else '')
    recovery_note=('首次校准遇到冷缓存日期前缀尺寸错误；通过单独的缓存切片适配器恢复，原始冻结源文件、模型参数、评分记录与选中预测数组均保留。完整输出逐位一致、冷缓存日期前缀、校准CSV官方评分和候选复放重新通过；适配器证据见本轮 `calibration_cache_recovery.json`。' if recovery else '')
    detail=f'''# 第{number}轮：{label}

本轮完成{unique}种不同输出配置、{total}条评分记录。R{parent_number}基准 **{selection['baseline_score']:.12f}**，最高连续验证分 **{winner['connected_final_score']:.12f}**，{outcome}。

| 阶段 | 评分记录 | 截至阶段结束的最高分 | 相比前阶段变化 |
| --- | ---: | ---: | ---: |
{stage_table}

具体方法的起点和自适应细搜规则已在评分前冻结。累计最高分是选模过程记录，阶段差异不表示独立因果贡献；重复基准不计作新的模型训练。

{cache_note}

{recovery_note}

| 指标 | R{parent_number}基准 | 本轮选中方案 | 变化 |
| --- | ---: | ---: | ---: |
{metric_rows}
所选配置：

```json
{configuration}
```

采用2020—2024逐年向前验证，连接1,212日、5,635,800行，年度边界换手连续计算。基准逐元素复现、成熟过去标签收益映射、实际验证CSV官方评分、所选方法标签置空和日期前缀检查、模型重载、预测重放、CSV键值及秩检查均通过。基础模型重新训练：{new_training}。

本轮未读取测试标签、未打新测试分；各验证年份此前均已查看，反复选模偏差未校正。候选单独保存于 `candidates/optimization_20261003_r{number}/submission.csv`，正式交付指针和历史候选保留。逐条评分见同目录的 `optimization_ranking_20261003_r{number}.json`。
'''
    (ROOT/f'results/optimization_20261003_r{number}.md').write_text(detail,encoding='utf-8')
    readme=ROOT/'README.md';current=readme.read_text(encoding='utf-8-sig');heading=f'### 第{number}轮：{label}'
    if heading not in current:
        current=current.rstrip()+f"\n\n{heading}\n\n{unique}种配置、{total}条评分；验证最高分 **{winner['connected_final_score']:.12f}**，{outcome}。收益映射后CSV官方评分、方法因果检查及候选复核通过；未读取测试标签。详见 [本轮报告](results/optimization_20261003_r{number}.md)。\n"
        readme.write_text(current,encoding='utf-8')
    plot(result)
    print(json.dumps({'round':number,'explicit_parent_round':parent_number,'independent_comparison_branch':True,'score':winner['connected_final_score'],'gain':selection['score_gain'],
                      'records':total,'distinct_configurations':unique},ensure_ascii=False,indent=2))
    return result


def plot(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':11})
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,5.7),gridspec_kw={'width_ratios':[1.4,1]})
    scores=[result['baseline_score']]+[s['cumulative_best'] for s in result['sequential_stage_results']]
    labels=['基准']+[s['stage'] for s in result['sequential_stage_results']]
    ax.plot(range(len(scores)),scores,color='#1975b7',marker='o',linewidth=2)
    ax.axhline(result['baseline_score'],color='#ba7143',linestyle='--',label=f"前轮基准 {result['baseline_score']:.9f}")
    ax.set_xticks(range(len(scores)),labels,rotation=18,fontsize=9)
    ax.ticklabel_format(axis='y',style='plain',useOffset=False)
    ax.set(title=f"最高分 {result['winner']['connected_final_score']:.9f}",ylabel='截至该阶段的最高连接验证分')
    ax.grid(alpha=.16);ax.legend(loc='lower right',fontsize=9)
    values=list(result['score_contributions_vs_baseline'].values())
    bx.bar(['Rank IC','年化超额收益','换手率'],values,color=['#1975b7' if v>=0 else '#b35c3e' for v in values]);bx.axhline(0,color='#7b8ba0')
    span=max(max(abs(v) for v in values),1e-6);bx.set_ylim(min(0,min(values))-.2*span,max(0,max(values))+.2*span)
    bx.set(title=f"相比前轮 {result['score_gain']:+.9f}",ylabel='官方综合分贡献变化')
    for i,v in enumerate(values):bx.annotate(f'{v:+.7f}',(i,v),xytext=(0,8 if v>=0 else -17),textcoords='offset points',ha='center',fontsize=9)
    fig.suptitle(f"赛题五 · R{result['round']} {result['round_label']}",fontsize=16,y=1.01)
    fig.text(.02,.015,f"{result['distinct_output_configurations']}种配置，{result['scored_records']}条评分；2020–2024连接1,212日；本轮未读取测试标签。",color='#526178',fontsize=10)
    fig.tight_layout(rect=(0,.055,1,.97));fig.savefig(ROOT/f"results/optimization_20261003_r{result['round']}.png",dpi=150,bbox_inches='tight');plt.close(fig)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('number',type=int);parser.add_argument('--label',required=True)
    parser.add_argument('--check',required=True);parser.add_argument('--stages',nargs='+',required=True)
    args=parser.parse_args();publish(args.number,args.label,args.check,args.stages)


if __name__=='__main__':main()

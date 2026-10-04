"""Record the completed checkpoint-ensemble optimization and its candidate."""
from pathlib import Path
import csv
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/optimization_20261003_r6'
CANDIDATE=ROOT/'candidates/optimization_20261003_r6'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):
            value.update(block)
    return value.hexdigest()


def dump(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def daily_diagnostics(path):
    with Path(path).open(encoding='utf-8',newline='') as stream:
        rows=list(csv.DictReader(stream))
    output={}
    for year in range(2020,2025):
        group=[r for r in rows if int(r['trade_date'])//10000==year]
        values={key:[float(r[key]) for r in group if math.isfinite(float(r[key]))]
                for key in ('rank_ic','excess','turnover')}
        metric={'ic_mean':sum(values['rank_ic'])/len(values['rank_ic']),
                'annual_excess':252*sum(values['excess'])/len(values['excess']),
                'mean_turnover':sum(values['turnover'])/len(values['turnover'])}
        metric['score']=0.4*metric['ic_mean']+0.3*metric['annual_excess']+0.3*(1-metric['mean_turnover'])
        output[str(year)]={'days':len(group),'finite_days':{k:len(v) for k,v in values.items()},**metric}
    return output


def main():
    selection=read(OUT/'selection.json')
    validation=read(OUT/'causal_validation.json')
    prediction=read(CANDIDATE/'verification.json')
    prior=read(ROOT/'results/optimization_20261003_r5.json')
    assert validation['status']==prediction['status']=='passed'
    assert sha(CANDIDATE/'submission.csv')==prediction['csv_sha256']
    assert prediction['old_delivery_pointer_unchanged']
    assert selection['scored_records']==26
    audits=[read(path) for path in (OUT/'raw').glob('*.json')]
    assert len(audits)==10 and len({a['source_model'] for a in audits})==5
    assert all(a['inherited_model_reload_bit_identical'] and a['same_training_keys_and_labels'] for a in audits)
    winner=selection['winner']
    baseline=prior['winner']['metrics']
    delta={k:winner['metrics'][k]-baseline[k] for k in ('ic_mean','annual_excess','mean_turnover')}
    contributions={'IC':0.4*delta['ic_mean'],'excess':0.3*delta['annual_excess'],'turnover':-0.3*delta['mean_turnover']}
    assert abs(sum(contributions.values())-selection['score_gain'])<1e-12
    sources=[ROOT/'analysis/optimize_training_round6.py',ROOT/'analysis/finalize_training_round6.py',Path(__file__)]
    earlier=daily_diagnostics(ROOT/'analysis/optimization_20261003_r5/selected_validation_daily.csv')
    current=daily_diagnostics(OUT/'selected_validation_daily.csv')
    for key,field,scale in (('rank_ic','ic_mean',1),('excess','annual_excess',1),('turnover','mean_turnover',1)):
        total=sum(r['finite_days'][key] for r in current.values())
        recombined=sum(r[field]*r['finite_days'][key] for r in current.values())/total
        assert abs(recombined-winner['metrics'][field])<1e-12
    coarse=read(OUT/'wave56_results.json')['results']
    alternatives=[dict(arm=name,**row) for name,row in coarse.items() if name!='membership_w5a0']
    result={'status':'complete','scope':'waves56-58','winner':winner,'baseline_score':selection['baseline_score'],
        'score_gain':selection['score_gain'],'scored_records':selection['scored_records'],
        'total_scored_records_including_repeats':prior['total_scored_records_including_repeats']+selection['scored_records'],
        'new_fold_models_trained':0,'saved_fold_models_used':5,'source_checkpoint_arrays':10,
        'new_checkpoint_predictions':0,'baseline_bit_identical':read(OUT/'wave56_results.json')['baseline_bit_identical'],
        'official_metric_change':delta,'score_contribution_change':contributions,
        'validation':validation,'prediction':prediction,'candidate_submission':str(CANDIDATE/'submission.csv'),
        'selection_rule':selection['selection_rule'],'test_labels_read_this_round':False,'test_score_of_this_candidate':None,
        'historical_test_best':{'arm':'wave13','score':0.417099224},
        'historical_test_best_scope':'previously disclosed written-CSV results; not used for selection',
        'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'previous_complete_deliveries_and_pointers_preserved':True,
        'boundary_label_maturity_audit':read(ROOT/'analysis/optimization_20261003_r2/boundary_maturity.json'),
        'source_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in sources},'consensus_prefix_controls':read(OUT/'consensus_prefix_controls.json'),
        'consensus_reranking_comparison':{'scored_alternatives':len(alternatives),
            'best':max(alternatives,key=lambda row:row['connected_final_score']),
            'improving_alternatives':sum(row['connected_final_score']>selection['baseline_score'] for row in alternatives)},
        'yearly_diagnostics':{'scope':'Year subsets of connected daily metrics; January boundary turnover retained; diagnostic only, not a selection gate.',
            'previous':earlier,'selected':current,
            'score_delta':{year:current[year]['score']-earlier[year]['score'] for year in current}}}
    dump(ROOT/'results/optimization_20261003_r6.json',result)
    dump(ROOT/'results/optimization_ranking_20261003_r6.json',{'status':'complete','ranking':selection['ranking']})
    dump(CANDIDATE/'manifest.json',{'status':'passed','files':{p.relative_to(CANDIDATE).as_posix():
        {'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(CANDIDATE.rglob('*')) if p.is_file() and p.name!='manifest.json'}})
    heading='### 第六轮继续优化（波56–58）'
    end='<!-- optimization20261003r6 end -->'
    recipe=winner['recipe']
    post=recipe['postprocessing']
    components=recipe['components'] if recipe['type']=='raw_rank_mix' else [dict(recipe,weight=1.0)]
    detail='、'.join(f'种子{c["seed"]}/{c["rounds"]}轮×{c["weight"]:.1%}' for c in components)
    section=(f'{heading}\n\n'
        f'复用5个年度Top-K模型的10组预测，完成{selection["scored_records"]}条完整方案评分记录。'
        '保持90/180轮日排名集成及促进入选股票池，比较以0%至100%权重融合slow16与W5a的当日排名用于成员重排，再细调领先方案的权重、排序和留存参数。'
        '原始预测文件及训练标签成熟边界核对通过，当前基准逐位复现，使用相同官方连接验证口径。\n\n'
        f'本轮最高连接验证分 **{winner["connected_final_score"]:.9f}**，相对上一轮 **{selection["score_gain"]:+.9f}**。'
        f'原始日排名集成：{detail}；平滑alpha={post["alpha"]:g}、bonus={post["bonus"]:g}；'
        f'成员重排W5a权重{winner["membership_w5a_weight"]:.2%}；排序slow16权重{winner["slow16_weight"]:.1%}、留存{winner["retention"]:.2%}、涨停排序偏移{winner["limit_up_delta"]:+g}。'
        '完整方案冻结后，因果收益映射、官方评分复核、历史前缀重放、最终模型重载及CSV逐字节重放均通过。\n\n'
        '未读取测试标签，候选无新增测试评分；历史测试回顾最佳仍为波13的0.417099224。'
        '新候选位于`candidates/optimization_20261003_r6/submission.csv`，'
        '详细结果见[第六轮优化记录](results/optimization_20261003_r6.json)。原交付及版本指针保留。'
        '验证年份已多次参与研究，未校正搜索选择偏差。\n\n'
        '复现顺序：`analysis/optimize_training_round6.py`的freeze、provenance、rerank、fine、refine；'
        '再运行`analysis/finalize_training_round6.py`的select、calibrate、predict。\n\n'+end+'\n\n')
    path=ROOT/'README.md'
    original=path.read_text(encoding='utf-8')
    if heading in original:
        start=original.index(heading)
        stop=original.index(end,start)+len(end)
        original=original[:start]+original[stop:].lstrip('\n')
    anchor='以下内容保留原67特征16种子基准的研究和运行说明。'
    assert anchor in original
    path.write_text(original.replace(anchor,section+anchor,1),encoding='utf-8')
    print(json.dumps({'score':winner['connected_final_score'],'gain':selection['score_gain'],
                     'records':selection['scored_records'],'candidate':str(CANDIDATE/'submission.csv')},ensure_ascii=False))


if __name__=='__main__':
    main()

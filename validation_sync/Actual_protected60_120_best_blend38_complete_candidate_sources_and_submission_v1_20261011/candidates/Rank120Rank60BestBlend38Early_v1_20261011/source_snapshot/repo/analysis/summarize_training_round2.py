"""Write the round2 result record and update the repository's research summary."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'analysis/optimization_20261003_r2'
CANDIDATE = ROOT/'candidates/optimization_20261003_r2'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''): h.update(block)
    return h.hexdigest()


def dump(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    selected = read(OUT/'selection.json')
    validation = read(OUT/'causal_validation.json')
    prediction = read(CANDIDATE/'verification.json')
    assert validation['status'] == prediction['status'] == 'passed'
    assert prediction['old_delivery_pointer_unchanged']
    assert sha(CANDIDATE/'submission.csv') == prediction['csv_sha256']
    prior = read(ROOT/'results/optimization_20261003.json')
    best = selected['winner']
    baseline = prior['winner']['metrics']
    count_models = len(list((OUT/'models').glob('*.txt')))
    count_checkpoints = len(list((OUT/'raw').glob('*.json')))
    assert count_models == 20 and count_checkpoints == 40
    maturity = read(OUT/'boundary_maturity.json')
    assert maturity['status'] == 'passed'
    checkpoint_audits = [read(path) for path in (OUT/'raw').glob('*.json')]
    assert all(item['model_reload_bit_identical'] and item['same_training_keys_and_labels'] for item in checkpoint_audits)
    assert sum(item['original_180_round_control'] is True for item in checkpoint_audits) == 5
    sources = [ROOT/'analysis/optimize_training_round2.py',ROOT/'analysis/finalize_training_round2.py',Path(__file__)]
    result = {'status':'complete','scope':'waves44-46','winner':best,'baseline_score':selected['baseline_score'],
        'score_gain':selected['score_gain'],'scored_records':selected['scored_records'],
        'total_scored_records_including_repeats':prior['total_scored_records_including_repeats']+selected['scored_records'],
        'fold_models':count_models,'checkpoint_predictions':count_checkpoints,
        'original_180_round_controls_passed':5,'boundary_label_maturity_audit':maturity,
        'official_metric_change':{k:best['metrics'][k]-baseline[k] for k in ('ic_mean','annual_excess','mean_turnover')},
        'score_contribution_change':{'IC':0.4*(best['metrics']['ic_mean']-baseline['ic_mean']),
            'excess':0.3*(best['metrics']['annual_excess']-baseline['annual_excess']),
            'turnover':-0.3*(best['metrics']['mean_turnover']-baseline['mean_turnover'])},
        'selection_rule':selected['selection_rule'],'validation':validation,'prediction':prediction,
        'candidate_submission':str(CANDIDATE/'submission.csv'),'test_labels_read_this_round':False,
        'test_score_of_this_candidate':None,'historical_test_best':{'arm':'wave13','score':0.417099224},
        'historical_test_best_scope':'previously disclosed written-CSV scoring results; not used for selection',
        'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'previous_complete_delivery_and_pointers_preserved':True,
        'source_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in sources}}
    assert abs(sum(result['score_contribution_change'].values())-selected['score_gain']) < 1e-12
    dump(ROOT/'results/optimization_20261003_r2.json',result)
    dump(ROOT/'results/optimization_ranking_20261003_r2.json',{'status':'complete','ranking':selected['ranking']})
    manifest = {'status':'passed','files':{p.relative_to(CANDIDATE).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size}
                  for p in sorted(CANDIDATE.rglob('*')) if p.is_file() and p.name != 'manifest.json'}}
    dump(CANDIDATE/'manifest.json',manifest)
    heading = '### 第二轮继续优化（波44–46）'
    end = '<!-- optimization20261003r2 end -->'
    text = (f'{heading}\n\n'
        f'新增{count_models}个年度训练模型、{count_checkpoints}组检查点预测及{selected["scored_records"]}条完整方案评分记录。'
        '比较原始分数先集成再平滑、训练轮数、学习率、叶节点数量与正则化。'
        '原配置180轮的五年检查点逐位复现旧预测，所有候选保留相同年度边界、样本及官方评分公式。\n\n'
        f'本轮最高连接验证分 **{best["connected_final_score"]:.9f}**，相对上一轮 **{selected["score_gain"]:+.9f}**。'
        f'成员来源`{best["donor"]}`，排序slow16权重{best["slow16_weight"]:.0%}，留存{best["retention"]:.1%}，'
        f'收益映射前的涨停行内部排序分数偏移{best["limit_up_delta"]:+.2f}。'
        '选择冻结后，因果收益映射、历史前缀重放、模型重载及实际CSV逐字节重放均通过。\n\n'
        '本轮未读取测试标签，没有新增候选测试评分；历史测试回顾最佳仍为波13的0.417099224。'
        '最高分候选位于`candidates/optimization_20261003_r2/submission.csv`，'
        '详细结果见[第二轮优化记录](results/optimization_20261003_r2.json)。旧交付包与版本指针保留。\n\n'
        '复现顺序：`analysis/optimize_training_round2.py`的freeze、rawmix、train（互不重叠的A/B组）、models、refine；'
        '再运行`analysis/finalize_training_round2.py`的select、calibrate、predict。\n\n'+end+'\n\n')
    path = ROOT/'README.md'
    original = path.read_text(encoding='utf-8')
    if heading in original:
        start = original.index(heading)
        stop = original.index(end,start)+len(end)
        original = original[:start]+original[stop:].lstrip('\n')
    anchor = '以下内容保留原67特征16种子基准的研究和运行说明。'
    assert anchor in original
    path.write_text(original.replace(anchor,text+anchor,1),encoding='utf-8')
    print(json.dumps({'score':best['connected_final_score'],'gain':selected['score_gain'],'records':selected['scored_records'],
                     'candidate':str(CANDIDATE/'submission.csv')},ensure_ascii=False))


if __name__ == '__main__':
    main()

"""Publish compact, training-only research results without rewriting old releases."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'analysis/optimization_20261003'
CANDIDATE = ROOT/'candidates/optimization_20261003'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def dump(path, value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as s:
        for block in iter(lambda:s.read(8*1024*1024),b''): h.update(block)
    return h.hexdigest()


def main():
    selection = read(OUT/'selection.json')
    causal = read(OUT/'causal_validation.json')
    candidate = read(CANDIDATE/'verification.json')
    assert causal['status'] == candidate['status'] == 'passed'
    assert candidate['old_delivery_pointer_unchanged']
    assert sha(CANDIDATE/'submission.csv') == candidate['csv_sha256']
    winner = selection['winner']
    assert abs(causal['metrics']['final_score']-winner['connected_final_score']) < 1e-12
    baseline = read(ROOT/'results/connected_selection_20261003.json')['winner']['metrics']
    old_rank = read(ROOT/'results/connected_all_model_ranking_20261003.json')
    mlp = read(ROOT/'analysis/connected_validation_20261002/mlp_connected_bound.json')
    scores = {}
    for wave in (40,41,42,43):
        r = read(OUT/f'wave{wave}_results.json')
        scores[str(wave)] = {'records':len(r['results']),
            'best':max(r['results'].items(),key=lambda pair:pair[1]['connected_final_score'])}
    manifest = {'status':'passed','files':{}}
    for p in sorted(CANDIDATE.rglob('*')):
        if p.is_file() and p.name != 'manifest.json':
            manifest['files'][p.relative_to(CANDIDATE).as_posix()] = {'sha256':sha(p),'bytes':p.stat().st_size}
    dump(CANDIDATE/'manifest.json',manifest)
    record = {'status':'complete','scope':'training-only optimization waves40-43',
              'winner':winner,'baseline_score':selection['baseline_score'],
              'score_gain':selection['score_gain'],'new_scored_records':selection['new_scored_records'],
              'total_scored_records_including_repeats':old_rank['scored_records']+selection['new_scored_records'],
              'new_fold_models':10,'training_cutoffs_verified':True,'year_boundary_turnover_included':True,
              'selection_rule':selection['selection_rule'],'waves':scores,
              'score_contribution_gain':{'IC':0.4*(winner['metrics']['ic_mean']-baseline['ic_mean']),
                  'excess':0.3*(winner['metrics']['annual_excess']-baseline['annual_excess']),
                  'turnover':-0.3*(winner['metrics']['mean_turnover']-baseline['mean_turnover'])},
              'historical_mlp_complete_scheme_bounds':{k:{n:v[n] for n in ('connected_score_lower','connected_score_upper')} for k,v in mlp['arms'].items()},
              'causal_calibration':causal,'candidate_submission':str(CANDIDATE/'submission.csv'),
              'candidate_verification':candidate,'test_labels_read_this_round':False,
              'test_score_for_new_candidate':None,'prior_test_best_disclosure':{'arm':'wave13','score':0.417099224},
              'selection_bias':'The same historical five validation years were repeatedly searched; this is not independent blind evidence.',
              'previous_complete_delivery_and_pointers_preserved':True,'prior_immutable_files_checked':369,
              'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'analysis/continue_optimization.py',ROOT/'analysis/optimize_fraction_mix.py',ROOT/'analysis/finalize_optimization.py',Path(__file__))}}
    assert abs(sum(record['score_contribution_gain'].values())-selection['score_gain']) < 1e-12
    dump(ROOT/'results/optimization_20261003.json',record)
    dump(ROOT/'results/optimization_ranking_20261003.json',{'status':'complete','ranking':selection['ranking']})
    start = '### 继续优化（波40–43）'
    end = '<!-- optimization20261003 end -->'
    text = (f'{start}\n\n'
        f'依照后续选模标准，又完成{selection["new_scored_records"]}条完整方案评分记录、10个年度模型训练。'
        f'本轮训练期最高分为 **{winner["connected_final_score"]:.9f}**，相对现有交付基准提升 **{selection["score_gain"]:+.9f}**。'
        f'成员来源为`{winner["donor"]}`，slow16排序权重{winner["slow16_weight"]:.1%}，留存比例{winner["retention"]:.1%}，'
        f'在收益映射前对涨停行的内部排序分数偏移{winner["limit_up_delta"]:+.2f}。\n\n'
        '完整候选经过因果前缀重放、各折训练标签边界核验及年度收益映射校验；'
        '2020年映射采用前期训练收益分布的仿射回退，2021—2024采用此前已成熟OOF标签的单调回归。'
        '映射后官方连接总分完全保持。后续日期收益映射仅使用全部历史OOF标签。\n\n'
        '已冻结本轮最高分方案并生成独立候选CSV，保存模型重载及CSV逐字节重放通过。'
        '本轮未读取测试标签，尚无新候选测试评分。旧报告、提交包和版本指针保留；'
        '最新研究候选见[优化结果](results/optimization_20261003.json)，预测文件在本地`candidates/optimization_20261003/submission.csv`。\n\n'
        '复现顺序：`analysis/continue_optimization.py`的freeze、joint、train、models、refine，及`analysis/optimize_fraction_mix.py`；'
        '再运行`analysis/finalize_optimization.py`的select、calibrate、predict。重跑复用冻结证据，所有选择仍只使用训练期。\n\n'+end+'\n\n')
    path = ROOT/'README.md'
    original = path.read_text(encoding='utf-8')
    if start in original:
        begin = original.index(start)
        finish = original.index(end,begin)+len(end)
        original = original[:begin]+original[finish:].lstrip('\n')
    anchor = '以下内容保留原67特征16种子基准的研究和运行说明。'
    assert anchor in original
    path.write_text(original.replace(anchor,text+anchor,1),encoding='utf-8')
    print(json.dumps({'best_score':winner['connected_final_score'],'gain':selection['score_gain'],
                      'new_records':selection['new_scored_records'],'candidate':str(CANDIDATE/'submission.csv')},ensure_ascii=False))


if __name__ == '__main__':
    main()

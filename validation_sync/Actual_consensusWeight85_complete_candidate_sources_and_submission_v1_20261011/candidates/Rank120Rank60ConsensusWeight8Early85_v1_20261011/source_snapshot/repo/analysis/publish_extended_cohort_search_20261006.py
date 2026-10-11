"""Publish finished extended phases, preserving all scores and source evidence."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
SOURCE = A / 'publish_cohort_rank_calibration_evidence_20261006.py'


def main(phase):
    text = SOURCE.read_text(encoding='utf-8')
    text = text.replace('cohort_rank_calibration_full_controls_20261006', 'extended_cohort_rank_calibration_full_controls_20261006')
    text = text.replace('cohort_rank_calibration_official_pilot_20261006', 'extended_cohort_rank_calibration_official_pilot_20261006')
    text = text.replace('full17_', 'full66_').replace('actual17_', 'actual66_').replace('all17_', 'all66_')
    text = text.replace('记录17项', '记录66项')
    text = text.replace("f'cohort_rank_calibration_{phase}_github_20261006'", "f'extended_cohort_rank_calibration_{phase}_github_20261006'")
    text = text.replace("f'validation_sync/cohort_rank_calibration_{phase}_20261006'", "f'validation_sync/extended_cohort_rank_calibration_{phase}_20261006'")
    start = "    service = A / ('service_owned_workflows_20261006/cohort_rank_calibration_controls'"
    end = "    out = A /"
    left, right = text.index(start), text.index(end)
    text = text[:left] + "    service = A / 'service_owned_workflows_20261006/extended_cohort_controls_and_scores'\n" + text[right:]
    # Phase proof is written only after all full assertions succeed. This
    # synchronous caller may continue into scoring; no process completion is claimed.
    text = text.replace('sources = [Path(__file__),',
        "sources = [Path(__file__), SOURCE, A / 'cohort_rank_calibration_v2_20261006.py',\n"
        "        A / 'prepare_extended_cohort_search_20261006.py', A / 'extended_cohort_search_preparation_20261006.json',\n"
        "        A / 'run_extended_cohort_controls_and_scores_20261006.py',\n"
        "        * (A / 'extended_cohort_search_execution_20261006').glob('*.json'),")
    # Supply the actual wider grid documentation instead of the original17 grid.
    start = "        targets[(prefix / 'README.md').as_posix()] = ("
    end = '        for name, data in targets.items():'
    left, right = text.index(start), text.index(end)
    description = ('# 扩展成熟训练涨停分组排名校准\n\n'
        '分箱8/16/64/256，每箱收缩伪样本0/50/200/1000，混合权重0.25/0.5/0.75/1，'
        '共64个扩展方案，加原95轮和已完整验证99轮两个锚点，共66条比较记录。'
        '68次年度成对曲线拟合，包括独立复现32箱、零收缩锚点；新增基础模型训练0。'
        '沿用原fold_cutoff及5,635,800行训练OOF，每年仅使用成熟过去标签。'
        '所有完整排序、冷前缀和标签污染检查保留；官方原脚本评估过去收益映射后的完整CSV。'
        '不读取测试标签，试评分尚须冻结候选及完整榜检查才具备正式选用资格。\n\n'
        'controls是完成的因果阶段；拥有进程可接着运行pilot，并不声称整个进程已结束。'
        '所有方案、原始分数、源码与失败证据仅发布main。\n')
    text = text[:left] + "        targets[(prefix / 'README.md').as_posix()] = " + repr(description.encode('utf-8')) + '\n' + text[right:]
    namespace = {'__name__': 'extended_cohort_publication', '__file__': __file__, 'SOURCE': SOURCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main'](phase)


if __name__ == '__main__':
    main(sys.argv[1])

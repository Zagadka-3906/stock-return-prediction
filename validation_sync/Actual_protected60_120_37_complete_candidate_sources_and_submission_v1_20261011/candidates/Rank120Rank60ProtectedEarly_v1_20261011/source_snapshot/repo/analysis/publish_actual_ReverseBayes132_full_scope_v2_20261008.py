"""Preserve admitted generated mathematical sources and correct actual132 publishing text."""
from pathlib import Path


def main():
    source = Path(__file__).with_name('publish_nonflag_ReverseBayes40_round132_full_validation_20261007.py')
    text = source.read_text(encoding='utf8')
    first = text.index("    payload[(prefix / 'README.md').as_posix()] += (")
    last = text.index("    previous = sync.git('rev-parse', 'HEAD')", first)
    actual = ('\n本轮实际40项反向经验贝叶斯残差比较：112、130、131三个合格锚点，标量先验、对角先验及等权均值各12个幅度（36项），加一个消融。'
        '复用10个年度成熟原生模型，先完成有序均值再乘负号；37项全量变换、111冷前缀及3个历史原生核对通过。'
        '按完整官方八指标及综合S选优；选中新方案后冻结并进行完整候选重放、独立解码、冷80及原始六视图45秒QA43，完全相同锚点仅在所有位、指标、参数与完整图一致时复用。'
        '保留原始生成器及旧模板文字作为历史源码，本说明按实际40项范围更正。仅main，不读取真实测试标签，不声称优化穷尽。\n')
    text = text[:first] + "    payload[(prefix / 'README.md').as_posix()] += " + repr(actual) + ".encode('utf8')\n" + text[last:]
    text = text.replace('登记第119轮88项非涨停残差HGB与完整父方案组合验证并发布完整榜与全量QA',
        '登记第132轮40项反向经验贝叶斯完整方案与原始QA43')
    namespace = {'__file__': str(Path(__file__)), '__name__': 'actual_negative132_explanatory_publication'}
    exec(compile(text, str(source), 'exec'), namespace)
    namespace['main']()

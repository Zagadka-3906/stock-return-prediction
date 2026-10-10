"""Use the correct model-family labels in actual published GOSS validation records."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main():
    source = (A / 'run_gradient_sampling_round_20261005.py').read_text(encoding='utf-8-sig')
    source = source.replace('因子分解模型三种用途对照', 'GOSS梯度采样模型三种用途对照')
    source = source.replace('匹配参数的成熟特征因子分解机完整方案', '匹配参数的成熟特征GOSS梯度采样完整方案')
    source = source.replace('factorization', 'gradient sampling')
    source = source.replace('gradient_sampling_quality_run_20261005.json', 'gradient_sampling_quality_run_v2_20261005.json')
    for path, text in [(A / 'run_gradient_sampling_round_v2_20261005.py', source),
        *[(A / f'run_training_round{n}_v2_pipeline.py',
           f'from run_gradient_sampling_round_v2_20261005 import main\nif __name__ == "__main__": main({n})\n') for n in (75, 76)]]:
        compile(text, str(path), 'exec')
        with path.open('x', encoding='utf-8', newline='') as stream:
            stream.write(text)


if __name__ == '__main__':
    main()

"""Standalone plots of the completed training-only model comparison."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'analysis/optimization_20261003_r2'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    result = read(ROOT/'results/optimization_20261003_r2.json')
    checkpoint = read(OUT/'wave45_results.json')['results']
    mixture = read(OUT/'wave44_results.json')['results']
    baseline = result['baseline_score']
    fig,axes = plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    ax = axes[0]
    labels = {'round_curve31':'31 leaves, LR0.05','slow_lr31':'31 leaves, LR0.025',
              'leaves63':'63 leaves, LR0.05','regularized31':'31 leaves, stronger regularization'}
    for family,label in labels.items():
        records = sorted([r for r in checkpoint.values() if r['recipe']['family'] == family],key=lambda r:r['recipe']['rounds'])
        ax.plot([r['recipe']['rounds'] for r in records],[(r['connected_final_score']-baseline)*1e3 for r in records],
                marker='o',label=label,lw=1.5,ms=5)
    ax.axhline(0,color='#5b6876',ls='--',lw=1,label='Previous best')
    ax.set(xlabel='Boosting rounds',ylabel='Official score change / 0.001',title='Wave45: complete checkpoint schemes')
    ax.grid(alpha=.2)
    ax.legend(fontsize=8,loc='best')
    ax = axes[1]
    entries = [(name,r['connected_final_score']) for name,r in mixture.items() if name != 'baseline']
    names = [name.replace('raw_','').replace('seed','').replace('_equal',' mean').replace('frac','K ').replace('_w025',' (25%)').replace('_w050',' (50%)') for name,_ in entries]
    scores = [(score-baseline)*1e3 for _,score in entries]
    scores.append((result['winner']['connected_final_score']-baseline)*1e3)
    names.append('Selected complete scheme')
    ax.barh(np.arange(len(scores)),scores,color=['#4c83ad']*len(entries)+['#cc923d'])
    ax.set_yticks(np.arange(len(scores)),names,fontsize=8)
    ax.invert_yaxis()
    ax.axvline(0,color='#5b6876',lw=1)
    ax.grid(axis='x',alpha=.2)
    ax.set(xlabel='Official score change / 0.001',title='Waves44-46: raw mixtures and final selection')
    fig.suptitle(f'Connected 2020-2024 validation: {baseline:.6f} -> {result["winner"]["connected_final_score"]:.6f}',fontsize=12)
    path = ROOT/'results/optimization_20261003_r2.png'
    fig.savefig(path,dpi=170,facecolor='white')
    plt.close(fig)
    print(path)


if __name__ == '__main__':
    main()

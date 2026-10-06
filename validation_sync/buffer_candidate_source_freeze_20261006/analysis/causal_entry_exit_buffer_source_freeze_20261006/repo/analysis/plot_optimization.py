"""A standalone research figure from finalized training-only scores."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'analysis/optimization_20261003'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    summary = read(ROOT/'results/optimization_20261003.json')
    joint = read(OUT/'wave40_results.json')['results']
    models = read(OUT/'wave41_results.json')['results']
    mixes = read(OUT/'wave43_results.json')['results']
    baseline = summary['baseline_score']
    weights = sorted({r['slow16_weight'] for r in joint.values()})
    keeps = sorted({r['retention'] for r in joint.values()})
    values = np.empty((len(keeps),len(weights)))
    for r in joint.values():
        values[keeps.index(r['retention']),weights.index(r['slow16_weight'])] = 1e3*(r['connected_final_score']-baseline)
    fig,axes = plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    ax = axes[0]
    colors = ax.imshow(values,cmap='RdBu_r',vmin=-max(abs(values.min()),abs(values.max())),vmax=max(abs(values.min()),abs(values.max())),aspect='auto')
    ax.set_xticks(range(len(weights)),[f'{v:.0%}' for v in weights])
    ax.set_yticks(range(len(keeps)),[f'{v:.1%}' for v in keeps])
    ax.set(xlabel='slow16 ordering weight',ylabel='Minimum retained fraction',title='Wave40: joint search')
    for i,j in np.ndindex(values.shape):
        ax.text(j,i,f'{values[i,j]:+.2f}',ha='center',va='center',fontsize=9,
                color='white' if abs(values[i,j])>2.5 else '#172635')
    fig.colorbar(colors,ax=ax,label='Official score gain (x0.001)',shrink=.82)
    ax = axes[1]
    best_mix = max(mixes.values(),key=lambda r:r['connected_final_score'])
    entries = [('Original',baseline)] + [(name,r['connected_final_score']) for name,r in models.items()] + [('Best fraction mix',best_mix['connected_final_score']),('Selected',summary['winner']['connected_final_score'])]
    labels = [name.replace('_equal',' mean').replace('_half_others_quarter',' 50/25/25').replace('seed','Seed ') for name,_ in entries]
    gain = [1e3*(score-baseline) for _,score in entries]
    ax.barh(range(len(entries)),gain,color=['#68788a']+['#4d87b8']*(len(models)+1)+['#d49135'])
    ax.annotate(f'+{gain[-1]:.4f}',(gain[-1],len(entries)-1),xytext=(-32,0),
                textcoords='offset points',ha='right',va='center',fontsize=9,color='#885416')
    ax.axvline(0,color='#3e4854',lw=1)
    ax.set_yticks(range(len(entries)),labels,fontsize=9)
    ax.invert_yaxis()
    ax.set(xlabel='Official score gain (x0.001)',title='Waves41-43: complete output schemes')
    ax.grid(axis='x',alpha=.2)
    fig.suptitle(f'Training-only connected 2020-2024 validation: {baseline:.6f} -> {summary["winner"]["connected_final_score"]:.6f}',fontsize=12)
    target = ROOT/'results/optimization_20261003.png'
    fig.savefig(target,dpi=170,facecolor='white')
    plt.close(fig)
    print(target)


if __name__ == '__main__':
    main()

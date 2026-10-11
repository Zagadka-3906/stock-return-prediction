"""Standalone comparison of seed diversity and output parameters."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/optimization_20261003_r5'

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def main():
    result=read(ROOT/'results/optimization_20261003_r5.json')
    coarse=read(OUT/'wave53_results.json')['results']
    output=read(OUT/'wave55_results.json')['results']
    baseline=result['baseline_score']
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    groups={}
    for row in coarse.values():
        parts=row['recipe']['components']
        if len(parts)!=3:continue
        c=parts[-1]
        groups.setdefault((c['seed'],c['rounds']),[]).append(row)
    ax=axes[0]
    for (seed,rounds),rows in sorted(groups.items()):
        rows.sort(key=lambda r:r['recipe']['components'][-1]['weight'])
        ax.plot([r['recipe']['components'][-1]['weight'] for r in rows],
                [(r['connected_final_score']-baseline)*1e3 for r in rows],
                marker='o',lw=1.5,ms=4,label=f'seed{seed}, {rounds} rounds')
    ax.axhline(0,color='#5b6876',ls='--',lw=1)
    ax.set(xlabel='Added seed weight',ylabel='Official score change / 0.001',title='Wave53: seed diversity')
    ax.grid(alpha=.2)
    ax.legend(fontsize=8)
    weights=(0.20,0.22,0.24,0.26,0.28)
    retention=(0.983,0.9845,0.986)
    values=np.array([[(output[f'order_w{w:g}_m{m:g}']['connected_final_score']-baseline)*1e3 for m in retention] for w in weights])
    ax=axes[1]
    bound=max(float(np.abs(values).max()),1e-6)
    chart=ax.imshow(values,cmap='RdBu',vmin=-bound,vmax=bound,aspect='auto')
    for i in range(len(weights)):
        for j in range(len(retention)):
            ax.text(j,i,f'{values[i,j]:+.3f}',ha='center',va='center',fontsize=10,
                    color='white' if abs(values[i,j])>0.55*bound else '#202b33')
    ax.set_xticks(range(len(retention)),[f'{m:.2%}' for m in retention])
    ax.set_yticks(range(len(weights)),[f'{w:.0%}' for w in weights])
    ax.set(xlabel='Member retention',ylabel='slow16 ordering weight',title='Wave55: complete-output refinement')
    fig.colorbar(chart,ax=ax,label='Official score change / 0.001',fraction=.045)
    fig.suptitle(f'Connected 2020-2024 validation: {baseline:.9f} -> {result["winner"]["connected_final_score"]:.9f}\n'
                 f'Selected limit-up shift {result["winner"]["limit_up_delta"]:g}; score gain {result["score_gain"]:+.3e}',fontsize=11)
    path=ROOT/'results/optimization_20261003_r5.png'
    fig.savefig(path,dpi=170,facecolor='white')
    plt.close(fig)
    print(path)

if __name__=='__main__':main()

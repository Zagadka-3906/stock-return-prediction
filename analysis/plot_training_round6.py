"""Standalone comparison of membership consensus reranking."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/optimization_20261003_r6'
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def main():
    result=read(ROOT/'results/optimization_20261003_r6.json')
    coarse=read(OUT/'wave56_results.json')['results']
    fine=read(OUT/'wave57_results.json')['results']
    output=read(OUT/'wave58_results.json')['results']
    baseline=result['baseline_score']
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    ax=axes[0]
    for rows,label,color in ((list(coarse.values()),'Initial weights','#4c83ad'),
                             (list(fine.values()),'Fine weights','#cc923d')):
        rows.sort(key=lambda r:r['membership_w5a_weight'])
        ax.plot([r['membership_w5a_weight'] for r in rows],
                [(r['connected_final_score']-baseline)*1e3 for r in rows],
                marker='o',lw=1.5,ms=5,label=label,color=color)
    ax.axhline(0,color='#5b6876',ls='--',lw=1)
    ax.set(xlabel='W5a weight in membership reranking',ylabel='Official score change / 0.001',
           title='Waves56-57: membership consensus')
    ax.grid(alpha=.2)
    ax.legend(fontsize=9)
    weights=(0.23,0.24,0.25)
    retention=(0.984,0.9845,0.985)
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
    ax.set(xlabel='Member retention',ylabel='slow16 ordering weight',title='Wave58: complete-output refinement')
    fig.colorbar(chart,ax=ax,label='Official score change / 0.001',fraction=.045)
    winner=result['winner']
    fig.suptitle(f'Connected 2020-2024 validation: {baseline:.9f} -> {winner["connected_final_score"]:.9f}\n'
                 f'Selected membership W5a weight {winner["membership_w5a_weight"]:g}; score gain {result["score_gain"]:+.3e}',fontsize=11)
    path=ROOT/'results/optimization_20261003_r6.png'
    fig.savefig(path,dpi=170,facecolor='white')
    plt.close(fig)
    print(path)

if __name__=='__main__':main()

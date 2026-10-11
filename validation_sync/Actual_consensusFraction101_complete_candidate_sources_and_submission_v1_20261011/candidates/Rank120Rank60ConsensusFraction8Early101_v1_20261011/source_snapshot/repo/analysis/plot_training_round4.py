"""Standalone figures of the round4 connected official score comparison."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/optimization_20261003_r4'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    result=read(ROOT/'results/optimization_20261003_r4.json')
    coarse=read(OUT/'wave50_results.json')['results']
    fine=read(OUT/'wave51_results.json')['results']
    baseline=result['baseline_score']
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    ax=axes[0]
    groups={}
    for row in coarse.values():
        parts=row['recipe']['components']
        if len(parts)!=2:continue
        key=tuple(c['rounds'] for c in parts)
        groups.setdefault(key,[]).append(row)
    for rounds,rows in sorted(groups.items()):
        rows.sort(key=lambda r:r['recipe']['components'][-1]['weight'])
        ax.plot([r['recipe']['components'][-1]['weight'] for r in rows],
                [(r['connected_final_score']-baseline)*1e3 for r in rows],marker='o',lw=1.5,ms=4,
                label=f'{rounds[0]}/{rounds[1]} rounds')
    ax.axhline(0,color='#5b6876',ls='--',lw=1,label='Previous best')
    ax.set(xlabel='Weight of later checkpoint',ylabel='Official score change / 0.001',title='Wave50: checkpoint mixtures')
    ax.grid(alpha=.2)
    ax.legend(fontsize=8)
    ax=axes[1]
    rows=sorted(fine.values(),key=lambda r:r['connected_final_score'],reverse=True)[:7]
    names=[]
    for row in rows:
        post=row['recipe']['postprocessing']
        weight=row['recipe']['components'][-1]['weight']
        names.append(f'w{weight:g} a{post["alpha"]:g} b{post["bonus"]:g}')
    scores=[(r['connected_final_score']-baseline)*1e3 for r in rows]
    names.append('Selected complete scheme')
    scores.append((result['winner']['connected_final_score']-baseline)*1e3)
    ax.barh(np.arange(len(scores)),scores,color=['#4c83ad']*len(rows)+['#cc923d'])
    ax.set_yticks(np.arange(len(scores)),names,fontsize=9)
    ax.invert_yaxis()
    ax.axvline(0,color='#5b6876',lw=1)
    ax.grid(axis='x',alpha=.2)
    ax.set(xlabel='Official score change / 0.001',title='Waves51-52: fine mixtures and output')
    ax.margins(x=.22)
    for index,value in enumerate(scores):
        ax.annotate(f'{value:+.3f}',(value,index),xytext=(4 if value>=0 else -4,0),textcoords='offset points',
                    va='center',ha='left' if value>=0 else 'right',fontsize=8)
    fig.suptitle(f'Connected 2020-2024 validation: {baseline:.6f} -> {result["winner"]["connected_final_score"]:.6f}',fontsize=12)
    path=ROOT/'results/optimization_20261003_r4.png'
    fig.savefig(path,dpi=170,facecolor='white')
    plt.close(fig)
    print(path)


if __name__=='__main__':
    main()

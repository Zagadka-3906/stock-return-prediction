"""Standalone comparison of the completed round3 official validation scores."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'analysis/optimization_20261003_r3'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    result = read(ROOT/'results/optimization_20261003_r3.json')
    models = read(OUT/'wave47_results.json')['results']
    smoothing = read(OUT/'wave48_results.json')['results']
    baseline = result['baseline_score']
    fig,axes = plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    ax = axes[0]
    for seed in (2026,2027,2028):
        records = sorted([v for v in models.values() if v['recipe']['type']=='model' and v['recipe']['seed']==seed],key=lambda r:r['recipe']['rounds'])
        ax.plot([r['recipe']['rounds'] for r in records],[(r['connected_final_score']-baseline)*1e3 for r in records],marker='o',lw=1.5,ms=5,label=f'Seed {seed}')
    ax.axhline(0,color='#5b6876',ls='--',lw=1,label='Previous best')
    ax.set(xlabel='Boosting rounds',ylabel='Official score change / 0.001',title='Wave47: complete checkpoint schemes')
    ax.legend(fontsize=9)
    ax.grid(alpha=.2)
    ax = axes[1]
    rows = sorted(smoothing.values(),key=lambda r:r['connected_final_score'],reverse=True)[:7]
    names = [f'a{r["recipe"]["postprocessing"]["alpha"]:g} b{r["recipe"]["postprocessing"]["bonus"]:g} aux{r["recipe"]["postprocessing"]["weight"]:g}' for r in rows]
    scores = [(r['connected_final_score']-baseline)*1e3 for r in rows]
    names.append('Selected complete scheme')
    scores.append((result['winner']['connected_final_score']-baseline)*1e3)
    ax.barh(np.arange(len(scores)),scores,color=['#4c83ad']*len(rows)+['#cc923d'])
    ax.set_yticks(np.arange(len(scores)),names,fontsize=9)
    ax.invert_yaxis()
    ax.axvline(0,color='#5b6876',lw=1)
    ax.grid(axis='x',alpha=.2)
    ax.set(xlabel='Official score change / 0.001',title='Waves48-49: smoothing and final selection')
    ax.margins(x=.20)
    for index,value in enumerate(scores):
        ax.annotate(f'{value:+.3f}',(value,index),xytext=(4 if value>=0 else -4,0),textcoords='offset points',va='center',ha='left' if value>=0 else 'right',fontsize=8)
    fig.suptitle(f'Connected 2020-2024 validation: {baseline:.6f} -> {result["winner"]["connected_final_score"]:.6f}',fontsize=12)
    path = ROOT/'results/optimization_20261003_r3.png'
    fig.savefig(path,dpi=170,facecolor='white')
    plt.close(fig)
    print(path)


if __name__=='__main__':
    main()

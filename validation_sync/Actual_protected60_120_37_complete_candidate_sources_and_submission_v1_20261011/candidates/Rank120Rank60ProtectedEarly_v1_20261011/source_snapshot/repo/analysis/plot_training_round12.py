"""Standalone score evolution for independent membership and TopK refinement."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]


def main():
    result=json.loads((ROOT/'results/optimization_20261003_r12.json').read_text(encoding='utf-8'))
    plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':11})
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,5.7),gridspec_kw={'width_ratios':[1.4,1]})
    scores=[result['baseline_score']]+[s['cumulative_best'] for s in result['sequential_stage_results']]
    ax.plot(range(5),scores,color='#1975b7',marker='o',linewidth=2)
    ax.axhline(result['baseline_score'],color='#ba7143',linestyle='--',label=f"R11基准 {result['baseline_score']:.9f}")
    ax.set_xticks(range(5),['基准','融合权重','独立持仓排序','TopK细调','输出细调'],rotation=15)
    ax.ticklabel_format(axis='y',style='plain',useOffset=False)
    ax.set(title=f"最高分 {result['winner']['connected_final_score']:.9f}",ylabel='截至该阶段的最高连接验证分')
    ax.grid(alpha=.16);ax.legend(loc='lower right',fontsize=9)
    values=list(result['score_contributions_vs_baseline'].values())
    bx.bar(['Rank IC','年化超额收益','换手率'],values,color=['#1975b7' if v>=0 else '#b35c3e' for v in values])
    bx.axhline(0,color='#7b8ba0',linewidth=1)
    span=max(max(abs(v) for v in values),1e-6)
    bx.set_ylim(min(0,min(values))-.2*span,max(0,max(values))+.2*span)
    bx.set(title=f"对R11基准变化 {result['score_gain']:+.9f}",ylabel='官方综合分贡献变化')
    for i,v in enumerate(values):
        bx.annotate(f'{v:+.7f}',(i,v),xytext=(0,8 if v>=0 else -17),textcoords='offset points',ha='center',fontsize=9)
    fig.suptitle('赛题五 · 独立持仓排序器与TopK细调',fontsize=17,y=1.01)
    fig.text(.02,.015,f"{result['distinct_output_configurations']}种配置，70条评分；2020–2024连接1,212日；本轮未读取测试标签。",color='#526178',fontsize=10)
    fig.tight_layout(rect=(0,.055,1,.97));fig.savefig(ROOT/'results/optimization_20261003_r12.png',dpi=150,bbox_inches='tight');plt.close(fig)


if __name__=='__main__':main()

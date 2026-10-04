"""Render the complete, repaired official-score comparison as a standalone figure."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/optimization_20261003_r7'


def main():
    result=json.loads((ROOT/'results/optimization_20261003_r7.json').read_text(encoding='utf-8-sig'))
    rows=json.loads((OUT/'selection.json').read_text(encoding='utf-8-sig'))['ranking']
    plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':11})
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,5.7),gridspec_kw={'width_ratios':[2,1]})
    x=list(range(1,len(rows)+1));values=[r['connected_final_score'] for r in rows]
    ax.scatter(x,values,c=['#1674b8' if r['ensemble_name']=='four_no_pruning' else '#95a5bd' for r in rows],s=42)
    ax.axhline(result['baseline_score'],color='#ba7143',linestyle='--',label=f"修正后同设置基准 {result['baseline_score']:.9f}")
    ax.set(xlabel='本轮完整方案分序（含重复对照）',ylabel='连接验证官方综合分',title=f"{len(rows)}条方案 · 最优 {rows[0]['connected_final_score']:.9f}")
    ax.grid(alpha=.18);ax.legend(loc='lower left',fontsize=9)
    changes=result['score_contributions_vs_repaired_baseline'];labels=['Rank IC','年化超额收益','换手率']
    delta=list(changes.values());bx.bar(labels,delta,color=['#1674b8' if v>=0 else '#b85c40' for v in delta])
    bx.set_ylim(min(0,min(delta)*1.2),max(delta)*1.17)
    bx.axhline(0,color='#75869c',linewidth=1);bx.set(title=f"对修正后基准提升 {result['score_gain']:+.9f}",ylabel='官方分数贡献变化')
    for i,v in enumerate(delta):bx.annotate(f'{v:+.7f}',(i,v),xytext=(0,8 if v>=0 else -17),textcoords='offset points',ha='center',fontsize=9)
    fig.suptitle('赛题五 · 剪枝来源修正与无剪枝集成优化',fontsize=17,y=1.01)
    fig.text(.02,.015,'2020–2024逐年向前验证，连接1,212日；本轮未读取测试标签。旧未修正验证分单列为历史诊断。',color='#526178',fontsize=10)
    fig.tight_layout(rect=(0,.055,1,.97));fig.savefig(ROOT/'results/optimization_20261003_r7.png',dpi=150,bbox_inches='tight');plt.close(fig)


if __name__=='__main__':main()

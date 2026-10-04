"""Standalone comparison of four tested directions and cumulative best output."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]


def main():
    result=json.loads((ROOT/'results/optimization_20261003_r11.json').read_text(encoding='utf-8'))
    plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':11})
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,5.7),gridspec_kw={'width_ratios':[1,1.2]})
    methods=result['methods_independently_compared_to_same_baseline'];changes=[m['best_changed_gain'] for m in methods]
    ax.bar(['模型权重','排序权重','留存信号','持仓融合'],changes,color=['#1975b7' if x>=0 else '#b35c3e' for x in changes])
    ax.axhline(0,color='#7b8ba0',linewidth=1)
    span=max(max(abs(v) for v in changes),1e-6)
    ax.set_ylim(min(0,min(changes))-.22*span,max(0,max(changes))+.20*span)
    ax.set(title='各方向独立测试：最佳变更配置',ylabel='相对相同R10基准的综合分变化')
    ax.grid(axis='y',alpha=.15)
    for i,v in enumerate(changes):
        ax.annotate(f'{v:+.7f}',(i,v),xytext=(0,8 if v>=0 else -17),textcoords='offset points',ha='center',fontsize=9)
    labels=['基准','模型权重','排序权重','留存信号','持仓融合','组合','细调']
    scores=[result['baseline_score']]
    for wave in range(71,77):
        payload=json.loads((ROOT/f'analysis/optimization_20261003_r11/wave{wave}_results.json').read_text(encoding='utf-8'))
        scores.append(max(scores[-1],max(r['connected_final_score'] for r in payload['results'].values())))
    bx.plot(range(len(scores)),scores,color='#1975b7',marker='o',linewidth=2)
    bx.axhline(result['baseline_score'],color='#ba7143',linestyle='--',label=f"基准 {result['baseline_score']:.9f}")
    bx.set_xticks(range(len(scores)),labels,rotation=20)
    bx.ticklabel_format(axis='y',style='plain',useOffset=False)
    bx.set(title=f"最终 {result['winner']['connected_final_score']:.9f} · 提升 {result['score_gain']:+.9f}",ylabel='截至该阶段的最高连接验证分')
    bx.grid(alpha=.15);bx.legend(loc='lower right',fontsize=9)
    fig.suptitle('赛题五 · 四方向优化与组合实测',fontsize=17,y=1.01)
    fig.text(.02,.015,f"{result['distinct_output_configurations']}种配置，{result['scored_records']}条评分记录；2020–2024连接1,212日；本轮未读取测试标签。",color='#526178',fontsize=10)
    fig.tight_layout(rect=(0,.055,1,.97));fig.savefig(ROOT/'results/optimization_20261003_r11.png',dpi=150,bbox_inches='tight');plt.close(fig)


if __name__=='__main__':main()

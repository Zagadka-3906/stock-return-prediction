"""Standalone comparison of retention-priority output schemes."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]


def main():
    result=json.loads((ROOT/'results/optimization_20261003_r10.json').read_text(encoding='utf-8'))
    rows=json.loads((ROOT/'analysis/optimization_20261003_r10/selection.json').read_text(encoding='utf-8'))['ranking']
    plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':11})
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,5.7),gridspec_kw={'width_ratios':[2,1]})
    for changed,color,label in ((True,'#1674b8','改变补入或剔除规则'),(False,'#95a5bd','原规则及参数对照')):
        points=[(i,r['connected_final_score']) for i,r in enumerate(rows,1)
                if bool(r['add_priority_weight'] or r['drop_priority_weight'])==changed]
        ax.scatter([p[0] for p in points],[p[1] for p in points],s=40,c=color,label=label)
    ax.axhline(result['baseline_score'],color='#ba7143',linestyle='--',label=f"R9基准 {result['baseline_score']:.9f}")
    ax.set(xlabel='本轮完整方案分序（含重复对照）',ylabel='连接验证官方综合分',
           title=f"{len(rows)}条评分记录 · {result['distinct_output_configurations']}种配置 · 最优 {rows[0]['connected_final_score']:.9f}")
    ax.grid(alpha=.18);ax.legend(loc='lower left',fontsize=9)
    groups=[lambda r:r['add_priority_weight']>0 and r['drop_priority_weight']==0,
            lambda r:r['add_priority_weight']==0 and r['drop_priority_weight']>0,
            lambda r:r['add_priority_weight']>0 and r['drop_priority_weight']>0]
    delta=[max(r['connected_final_score'] for r in rows if match(r))-result['baseline_score'] for match in groups]
    bx.bar(['只改补入','只改剔除','同时改变'],delta,color=['#1674b8' if x>=0 else '#b85c40' for x in delta])
    bx.axhline(0,color='#75869c',linewidth=1)
    bx.set(title='各方向最佳非零权重方案',ylabel='相对R9基准的综合分变化')
    span=max(max(abs(v) for v in delta),1e-6)
    bx.set_ylim(min(0,min(delta))-.12*span,max(0,max(delta))+.20*span)
    for i,v in enumerate(delta):
        label='0.0000000' if v==0 else f'{v:+.7f}'
        bx.annotate(label,(i,v),xytext=(0,8 if v>=0 else -17),textcoords='offset points',ha='center',fontsize=9)
    fig.suptitle('赛题五 · 留存补入与剔除优先级优化',fontsize=17,y=1.01)
    fig.text(.02,.015,'2020–2024逐年向前验证，连接1,212日；本轮未读取测试标签，未新增独立模型训练。',color='#526178',fontsize=10)
    fig.tight_layout(rect=(0,.055,1,.97));fig.savefig(ROOT/'results/optimization_20261003_r10.png',dpi=150,bbox_inches='tight');plt.close(fig)


if __name__=='__main__':main()

"""Preserve signed-zero representative selection while vectorizing the independent oracle."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent

def main():
    source=A/'prepare_fast_quantization_controls_v2_20261010.py';s=source.read_text(encoding='utf8')
    s=s.replace('protected_lower_rank_quantization_v2_20261010','protected_lower_rank_quantization_v3_20261010').replace('protected_lower_rank_quantization_controls_v2_20261010','protected_lower_rank_quantization_controls_v3_20261010')
    old="""    new=\"\"\"        grouped=lower.groupby(buckets,sort=False)
        representatives=grouped.min() if representative=='minimum' else grouped.quantile(.5,interpolation='lower')
        result[lower.index.to_numpy()]=buckets.map(representatives).to_numpy()\"\"\""""
    new="""    new=\"\"\"        ordered=lower.sort_values(kind='mergesort')
        ordered_buckets=buckets.loc[ordered.index]
        grouped=ordered.groupby(ordered_buckets,sort=False)
        position=grouped.cumcount()
        target_position=position*0 if representative=='minimum' else (grouped.transform('size')-1)//2
        chosen=ordered[position==target_position]
        representatives=chosen.copy();representatives.index=ordered_buckets.loc[chosen.index].to_numpy()
        result[lower.index.to_numpy()]=buckets.map(representatives).to_numpy()\"\"\""""
    assert s.count(old)==1;s=s.replace(old,new)
    target=A/'run_fast_quantization_controls_v3_20261010.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    sys.path[:0]=[str(A),str(A.parent)]
    import runpy;runpy.run_path(str(target),run_name='__main__')

if __name__=='__main__':main()

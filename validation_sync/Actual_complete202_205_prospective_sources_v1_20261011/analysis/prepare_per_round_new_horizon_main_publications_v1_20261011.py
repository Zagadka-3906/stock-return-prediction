from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
    assert allowed()
    template=(A/'publish_actual_protected37_fraction38_completed75_main_v1_20261011.py').read_text(encoding='utf8')
    rows=[
      ('rank120_rank60_protected37',37,'actual_rank120_rank60_after183_protected37_screen_v2_20261011','StockRank120Rank60_after183_protected37_screen_v1_20261011'),
      ('rank60_seed10_pure33',33,'actual_stock_rank60seed10_embedding_after183_direct_allocation33_v1_20261011','StockRank60Seed10EmbeddingSmall512_after183_direct_allocation33_screen_v1_20261011'),
      ('rank60_two_seed_protected37',37,'actual_rank60_two_seed_after183_protected37_screen_v1_20261011','StockRank60TwoSeed_after183_protected37_screen_v1_20261011')]
    result=[]
    for label,count,service,folder in rows:
        target=f'Actual_{label}_completed_TRAIN_records'
        name=f'publish_actual_{label}_completed_main_v1_20261011.py'
        text=template.replace('Actual_protected37_and_fraction38_completed75_TRAIN_records',target)
        lines=text.splitlines()
        lines=[('    pairs='+repr([(service,folder,count)])) if line.strip().startswith('pairs=') else line for line in lines]
        text='\n'.join(lines)+'\n'
        text=text.replace("'actual_completed_official_records':75",f"'actual_completed_official_records':{count}")
        text=text.replace('actual37_mixed60_120_and38_fraction_weight_TRAIN_only_official_records_independent_full_and_prefix_controls',f'actual_{label}_TRAIN_only_official_records_independent_full_and_prefix_controls')
        text=text.replace('完成75项TRAIN验证：成熟60与120日目标组合及60日保护比例权重；全部官方评分与独立复算记录',f'完成{count}项TRAIN验证：{label}；全部官方评分与独立复算记录')
        ast.parse(text);p=A/name;assert not p.exists();p.write_text(text,encoding='utf8')
        assert allowed()
        row=start_service(f'actual_{label}_completed_main_v1_20261011',name,[],{str(p):sha(p),str(Path(__file__)):sha(__file__)})
        result.append({'label':label,'actual_launch':row,'expected_records':count,'completion_not_claimed':True})
    create(A/'actual_per_round_new_horizon_main_publications_admission_v1_20261011.json',{'status':'actual_three_conditional_main_only_publishers_launched','rows':result,'new_scientific_scores':0})
    print({'launched':len(result)},flush=True)
if __name__=='__main__':main()

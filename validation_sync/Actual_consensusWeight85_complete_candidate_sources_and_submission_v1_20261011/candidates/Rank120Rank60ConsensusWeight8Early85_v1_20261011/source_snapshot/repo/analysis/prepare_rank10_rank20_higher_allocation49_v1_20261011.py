from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();source=A/'run_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011.py';text=source.read_text(encoding='utf8')
 mapping={'rank5_rank20':'rank10_rank20','StockRank5Rank20':'StockRank10Rank20','rank5_weight':'rank10_weight','stock_rank5':'stock_rank10','StockRank5':'StockRank10','rank5mean':'rank10mean','Rank5Mean':'Rank10Mean'}
 for token in set(re.findall(r'[A-Za-z0-9_]*(?:stock_rank5|StockRank5)[A-Za-z0-9_]*',text)):
  if '202610' in token:mapping[token]=token.replace('stock_rank5','stock_rank10').replace('StockRank5','StockRank10').replace('20261010','20261011').replace('20261009','20261011')
 pat=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)));text=pat.sub(lambda m:mapping[m.group()],text)
 text=text.replace('mixed_horizon49_screen_v2_20261011','higher_allocation49_screen_v1_20261011')
 old='(.000078125,.00015625,.0003125,.000625,.00125,.0025,.005,.01)';new='(.00125,.005,.016,.064,.125,.25,.5,1.)';assert old in text;text=text.replace(old,new)
 text=text.replace('    assert allowed()\n    closed(',"    assert allowed()\n    closed('actual_stock_rank10_embedding_after175_large_allocation29_screen_v1_20261011')\n    closed(",1)
 target=A/'run_rank10_rank20_after175_higher_allocation49_screen_v1_20261011.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
 proof=A/'rank10_rank20_higher_allocation49_predeclared_sources_admission_v1_20261011.json'
 create(proof,{'status':'compiled_predeclared49_new_rank10_rank20_raw_mixtures_before_own_rank10_full5_completion_or_score','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target,A/'stock_rank10_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json']},'raw_rank10_weights':[.25,.5,.75],'CDF_weights':[.00125,.005,.016,.064,.125,.25,.5,1.],'signs':[-1,1],'expected_records':49,'expected_nonidentity_full_Pandas_controls':48,'expected_prefix_controls':144,'anchor':175,'test_labels_read':False,'future_X_read':False,'selected_native_stage_and_submission_qualification_pending':True,'new_fits':0,'new_scores':0})
 r=start_service('actual_rank10_rank20_after175_higher_allocation49_screen_v1_20261011',target.name,[],{str(target):sha(target),str(proof):sha(proof)});create(A/'actual_rank10_rank20_higher_allocation49_activation_v1_20261011.json',r)
 print({'actual_rank10_rank20_higher_allocation49_queued_after_rank10_46':True,'new_scores_not_yet_claimed':True},flush=True)
if __name__=='__main__':main()

"""Freeze tight CDF weights around the observed TRAIN complement gain; own bank is reused."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();original=A/'run_stock_rank20_embedding_after174_complement61_screen_v1_20261010.py'
    routepath=A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json';routes=read(routepath)
    parent175=routes['service_aliases']['StockTop10Embedding175_complete47_family_v3_20261010']
    outputs=[]
    for parent in (174,175):
        text=original.read_text(encoding='utf8').replace('high_impact61','tiny_CDF41')
        if parent==175:text=text.replace('StockRankDual174_verified_candidate_registration_recovery_v3_20261010',parent175).replace("release['scored_records']==44","release['scored_records']==47").replace('174','175')
        start=text.index('def cases():');end=text.index('\ndef main():',start)
        cases="""def cases():
    rows=[{'kind':'anchorPARENT','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for role in ('nonflag_valid','all_valid'):
        for sign in (-1.,1.):
            for weight in (.00003125,.0000625,.000125,.0001875,.00025,.0003125,.000375,.0005,.00075,.001):
                rows.append({'kind':'CDF','role':role,'weight':weight,'sign':sign,'protect_fraction':None})
    assert len(rows)==41;return rows

""".replace('PARENT',str(parent))
        text=text[:start]+cases+text[end:]
        text=text.replace('frozen61_','frozen41_').replace('rank20_mean61_training_only','rank20_mean41_training_only').replace("'expected_cases':61","'expected_cases':41").replace("'new_quality_score_records':61","'new_quality_score_records':41").replace("'actual_nonidentity_full_controls':60","'actual_nonidentity_full_controls':40").replace("'actual_nonidentity_prefix_controls':180","'actual_nonidentity_prefix_controls':120").replace('passed61_','passed41_')
        needle='    assert allowed()\n';assert text.count(needle)>=1
        text=text.replace(needle,needle+"    closed('actual_stock_rank20_embedding_after174_complement61_screen_v1_20261010')\n",1)
        needle='    paths=[actual_native_pointer';assert text.count(needle)==1
        text=text.replace(needle,"    paths=[A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json',A/'rank20_tiny_CDF82_after174175_predeclared_plan_v1_20261010.json',actual_native_pointer",1)
        path=A/f'run_stock_rank20_embedding_after{parent}_tiny_CDF41_screen_v1_20261010.py';assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');outputs.append(path)
    modules=[importlib.import_module(p.stem) for p in outputs]
    assert all(len(m.cases())==41 for m in modules)
    proof=A/'rank20_tiny_CDF82_after174175_predeclared_plan_v1_20261010.json'
    create(proof,{'status':'predeclared82_tiny_CDF_complement_comparisons_on_qualified174_and175_before_any_new_tight_weight_scores','input_sha256':{str(p):sha(p) for p in [Path(__file__),original,routepath,*outputs]},'families':[{'parent_round':parent,'cases':module.cases(),'actual_service':f'actual_stock_rank20_embedding_after{parent}_tiny_CDF41_screen_v1_20261010'} for parent,module in zip((174,175),modules)],'new_native_fits':0,'source_of_hypothesis':'observed_TRAIN_negativeCDF_00025_after174_gain_not_independent_selection','actual_future_X_read':False,'test_labels_read':False,'new_quality_scores':0})
    for parent,path in zip((174,175),outputs):
        name=f'actual_stock_rank20_embedding_after{parent}_tiny_CDF41_screen_v1_20261010';assert allowed();row=start_service(name,path.name,[],{str(path):sha(path),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'new_TRAIN_comparisons':82,'new_fits':0,'first_waits_current61_complete':True,'second_waits_qualified175':True,'actual_quality_pending':True},flush=True)
if __name__=='__main__':main()

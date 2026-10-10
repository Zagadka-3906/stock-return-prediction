"""Predeclare direct H60 large allocations on verified183, without fitting another bank."""
from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def save(name,text):
 p=A/name;ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8');return p

def main():
 assert allowed()
 oldstage=A/'stock_rank60_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py'
 s=oldstage.read_text(encoding='utf8');needle='spec[\'original_complete_parent_round\'] in (169,170,171,172,173,174,175,176)'
 assert s.count(needle)==1;s=s.replace(needle,needle[:-1]+',183)')
 stage=save('stock_rank60_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py',s)
 oldpred=A/'predict_stock_rank60_embedding_complete_qualified_parent_scheme_v1_20261011.py';s=oldpred.read_text(encoding='utf8')
 start=s.index('def parent_filename(graph):');end=s.index('\n\ndef prepared_parent(',start)
 s=s[:start]+"def parent_filename(graph):\n    from predict_stock_rank20class10_embedding_complete_qualified_parent_scheme_v2_20261011 import parent_filename as complete_parent\n    return complete_parent(graph)\n"+s[end:]
 s=s.replace('stock_rank60_embedding_after_complete_qualified_parent_native_stage_v1_20261011','stock_rank60_embedding_after_complete_qualified_parent_native_stage_v2_20261011')
 needle='spec[\'original_complete_parent_round\'] in (169,170,171,172,173,174,175,176,177,178,179)';assert s.count(needle)==1;s=s.replace(needle,needle[:-1]+',183)')
 predictor=save('predict_stock_rank60_embedding_complete_qualified_parent_scheme_v2_20261011.py',s)
 original_cpu=A/'verify_stock_rank20class10_actual_twelve_parent_callbacks_CPU_v2_20261011.py'
 s=original_cpu.read_text(encoding='utf8').replace('predict_stock_rank20class10_embedding_complete_qualified_parent_scheme_v2_20261011',predictor.stem).replace('stock_rank20class10_embedding_after_complete_qualified_parent_native_stage_v2_20261011',stage.stem).replace('stock_rank20class10_actual_twelve_parent_callbacks_CPU_controls_v2_20261011','stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011').replace('STOCK_RANK20CLASS10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT','STOCK_RANK10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT')
 cpu=save('verify_stock_rank60_actual_twelve_parent183_callbacks_CPU_v2_20261011.py',s)
 importlib.import_module(cpu.stem).main()
 cpu_proof=A/'stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json';assert len(read(cpu_proof)['records'])==12
 oldscreen=A/'run_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011.py'
 s=oldscreen.read_text(encoding='utf8').replace('Rank20Class10','Rank60').replace('rank20class10','rank60').replace('rank20mean','rank60mean')
 s=s.replace('high_impact17','direct_allocation33').replace('frozen17','frozen33').replace('return1d17','return1d33').replace('passed17','passed33').replace('expected_cases\':17','expected_cases\':33').replace('new_quality_score_records\':17','new_quality_score_records\':33').replace('actual_nonidentity_full_controls\':16','actual_nonidentity_full_controls\':32').replace('actual_nonidentity_prefix_controls\':48','actual_nonidentity_prefix_controls\':96')
 start=s.index('def cases():');end=s.index('\n\ndef main():',start)
 cases="""def cases():
    rows=[{'kind':'anchor183','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for sign in (1.,-1.):
        for weight in (.00015625,.000625,.0025,.01,.04,.16,.5,1.):
            rows.append({'kind':'CDF','role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':None})
    for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
        for sign in (1.,-1.):
            for weight in (.016,.064,.25,1.):
                rows.append({'kind':kind,'role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':.15})
    assert len(rows)==33;return rows
"""
 s=s[:start]+cases+s[end:]
 needle="    pins={str(p):sha(p) for p in paths};plan=cases()"
 assert s.count(needle)==1
 s=s.replace(needle,"    paths += [A/'stock_rank60_after183_direct33_predeclared_sources_v1_20261011.json',A/'stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json',A/'predict_stock_rank60_embedding_complete_qualified_parent_scheme_v2_20261011.py',A/'stock_rank60_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py']\n"+needle)
 assert 'expected_cases\':17' not in s and 'actual_nonidentity_full_controls\':16' not in s
 screen=save('run_stock_rank60_embedding_after183_direct_allocation33_v1_20261011.py',s)
 module=importlib.import_module(screen.stem);rows=module.cases();assert len(rows)==33 and len(set(repr(c) for c in rows))==33
 assert any(c['weight']==1. and c['kind']=='CDF' for c in rows)
 paths=[Path(__file__),oldstage,stage,oldpred,predictor,original_cpu,cpu,cpu_proof,oldscreen,screen,A/'optimization_20261003_r183/calibrated_csv_official.json',A/'github_validation_sync_main_20261005/round183_receipt.json',A/'stock_rank60_new60_horizon_source_pipeline_admission_v1_20261011.json']
 proof=A/'stock_rank60_after183_direct33_predeclared_sources_v1_20261011.json'
 create(proof,{'status':'compiled33_pure_mature60_on_qualified183_after_actual12_CPU_callbacks_before_scores','input_sha256':{str(p):sha(p) for p in paths},'parent_round':183,'cases':rows,'label_horizon_trading_days':60,'new_fits':0,'new_scores':0,'future_X_read':False,'test_labels_read':False,'native183_selected_stage_qualification_pending':True})
 # Keep original score stream ordering: direct33 starts after original H60 46.
 assert allowed();row=start_service('actual_stock_rank60_embedding_after183_direct_allocation33_v1_20261011',screen.name,[],{str(screen):sha(screen),str(proof):sha(proof)})
 create(A/'actual_stock_rank60_after183_direct33_activation_v1_20261011.json',row)
 oldpub=A/'run_publish_class10_after183_completed17_main_v1_20261011.py'
 s=oldpub.read_text(encoding='utf8').replace('actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011','actual_stock_rank60_embedding_after183_direct_allocation33_v1_20261011').replace('Rank20Class10','Rank60').replace('high_impact17','direct_allocation33').replace('stock_rank20class10_latest_qualified183_predeclared17_sources_v1_20261011','stock_rank60_after183_direct33_predeclared_sources_v1_20261011').replace('Class10_after183_actual17','Rank60_after183_actual33').replace('==17','==33').replace('==16','==32').replace('==48','==96').replace('actual17_continuous','actual33_continuous').replace("'actual_nonidentity_full_Pandas_controls':16","'actual_nonidentity_full_Pandas_controls':32").replace("'actual_prefix_controls':48","'actual_prefix_controls':96")
 pub=save('run_publish_rank60_after183_completed33_main_v1_20261011.py',s)
 assert allowed();row=start_service('actual_rank60_after183_completed33_main_v1_20261011',pub.name,[],{str(pub):sha(pub),str(proof):sha(proof)})
 create(A/'actual_rank60_after183_completed33_main_activation_v1_20261011.json',row)
 print({'actual_parent_CPU_checks':12,'pure_H60_cases_predeclared':33,'new_fits':0,'score_and_completed_publication_queued':True},flush=True)
if __name__=='__main__':main()

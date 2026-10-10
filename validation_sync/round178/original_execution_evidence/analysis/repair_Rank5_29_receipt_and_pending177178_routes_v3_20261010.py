"""Preserve every completed score; repair a terminal pointer and unstarted dependent routes."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def idle(name):
    f=A/'service_owned_workflows_20261006'/name;row=read(f/'native_launch.json');assert owned(row)
    retire(row,'Supersede exact childless unstarted helper after correcting large29 terminal pointer; preserve all scores/native models and original source bytes')
def main():
    assert allowed();closed('actual_Rank5_large29_verified_terminal_recovery_v1_20261010')
    recovery=A/'stock_rank5_embedding_actual29_terminal_pointer_recovery_v1_20261010.json';assert read(recovery)['new_quality_scores']==0
    assert not Path('E:/赛题五_本机临时/StockForward5EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010').exists()
    source=A/'run_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010.py';text=source.read_text(encoding='utf8')
    pointer='actual_StockForward5EmbeddingSmall512_after171_high_impact17_screen_location_v1_20261010';assert text.count(pointer)==1
    text=text.replace(pointer,'actual_StockForward5EmbeddingSmall512_after171_large_allocation29_screen_location_v1_20261010').replace('passed29_own_Top10_BCE_large_CDF_allocation','passed29_own_forward5_return_Huber_e64_large_CDF_allocation')
    large=save('run_stock_forward5_embedding_after171_large_allocation29_screen_v2_20261010.py',text)
    assert len(importlib.import_module(large.stem).cases())==29
    new_sources=[large];jobs=[];retire_jobs=['actual_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010','actual_stock_forward5_embedding_after171_large29_completion_main_v68_20261010']
    for namespace,number,previous,family_version in [('rank5',177,176,3),('forward5',178,177,4)]:
        kind='StockRank5Embedding' if namespace=='rank5' else 'StockForward5Embedding';prefix='stock_'+namespace+'_embedding'
        normal_old=A/f'normalize_completed_{prefix}_complete48_after{previous}_v2_20261010.py';normal_name=f'normalize_completed_{prefix}_complete48_after{previous}_v3_20261010.py'
        text=normal_old.read_text(encoding='utf8')
        if namespace=='rank5':aliases={'actual_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010':'actual_Rank5_large29_verified_terminal_recovery_v1_20261010'}
        else:aliases={'actual_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010':'actual_stock_forward5_embedding_after171_large_allocation29_screen_v2_20261010'}
        needle="        closed(family['actual_service']);receipt=A/family['main_receipt']";assert text.count(needle)==1
        text=text.replace(needle,"        actual_aliases="+repr(aliases)+"\n        closed(actual_aliases.get(family['actual_service'],family['actual_service']));receipt=A/family['main_receipt']")
        if namespace=='forward5':text=text.replace("closed('StockRank5Embedding177_complete48_family_v2_20261010')","closed('StockRank5Embedding177_complete48_family_v3_20261010')")
        normal=save(normal_name,text);new_sources.append(normal)
        qualifier_name=f'qualify_{prefix}48_selected_native14_v3_20261010.py';qualifier_old=A/f'qualify_{prefix}48_selected_native14_v2_20261010.py'
        old_queue=f'actual_{prefix}48_after{previous}_normalization_queue_v2_20261010';new_queue=old_queue.replace('_v2_','_v3_')
        q=save(qualifier_name,qualifier_old.read_text(encoding='utf8').replace(normal_old.stem,normal.stem).replace(old_queue,new_queue));new_sources.append(q)
        candidate_old=A/f'prepare_{kind}{number}_selected_candidate_v2_20261010.py';candidate_name=f'prepare_{kind}{number}_selected_candidate_v3_20261010.py'
        metadata_old=f'{prefix}{number}_candidate_sources_preparation_v2_20261010.json';metadata_new=metadata_old.replace('_v2_','_v3_')
        old_selected=f'{kind}48_selected_native14_v2_20261010';new_selected=old_selected.replace('_v2_','_v3_')
        text=candidate_old.read_text(encoding='utf8').replace(qualifier_old.stem,q.stem).replace(normal_old.stem,normal.stem).replace(old_selected,new_selected).replace(metadata_old,metadata_new)
        candidate=save(candidate_name,text);new_sources.append(candidate)
        pre_old=A/f'verify_{kind}{number}_full48_preflight_v2_20261010.py';pre_name=f'verify_{kind}{number}_full48_preflight_v3_20261010.py'
        family_old=A/f'run_{kind}{number}_complete_family_v2_20261010.py';actual_family_old=family_old if namespace=='rank5' else A/f'run_{kind}{number}_complete_family_v3_20261010.py'
        family_name=f'run_{kind}{number}_complete_family_v{family_version}_20261010.py';runtime_old=A/f'run_{kind}{number}_full_registration_v2_20261010.py';runtime_name=f'run_{kind}{number}_full_registration_v3_20261010.py'
        extras=[normal.name,q.name,candidate.name,metadata_new,recovery.name,Path(__file__).name]
        if namespace=='forward5':
            wrapper_old=A/'run_StockForward5Embedding178_selected_candidate_feature_cache_v3_20261010.py';wrapper_name='run_StockForward5Embedding178_selected_candidate_feature_cache_v4_20261010.py'
            wrapper=save(wrapper_name,wrapper_old.read_text(encoding='utf8').replace(candidate_old.name,candidate.name).replace('runtime_v3','runtime_v4'));new_sources.append(wrapper);extras.append(wrapper.name)
        text=pre_old.read_text(encoding='utf8').replace(metadata_old,metadata_new).replace(family_old.name,family_name).replace(runtime_old.name,runtime_name)
        marker="    for p in sources:\n";assert text.count(marker)==1;text=text.replace(marker,'    sources += [A/n for n in '+repr(extras)+']\n'+marker)
        pre=save(pre_name,text);new_sources.append(pre)
        text=runtime_old.read_text(encoding='utf8').replace(metadata_old,metadata_new).replace(family_old.name,family_name).replace(pre_old.name,pre.name)
        if namespace=='forward5':text=text.replace("closed('StockRank5Embedding177_complete48_family_v2_20261010')","closed('StockRank5Embedding177_complete48_family_v3_20261010')")
        needle='    sources=routes.source_paths();assert all(p.is_file() for p in sources)';assert text.count(needle)==1
        text=text.replace(needle,"    previous_routes=routes.source_paths\n    routes.source_paths=lambda:list(dict.fromkeys([*previous_routes(),*[A/n for n in "+repr(extras)+"]]))\n"+needle)
        runtime=save(runtime_name,text);new_sources.append(runtime)
        text=actual_family_old.read_text(encoding='utf8').replace(old_selected,new_selected).replace(pre_old.name,pre.name).replace(pre_old.stem,pre.stem).replace(runtime_old.name,runtime.name)
        if namespace=='rank5':text=text.replace(candidate_old.name,candidate.name)
        else:text=text.replace(wrapper_old.name,wrapper.name)
        needle='    pins={str(p):sha(p) for p in dict.fromkeys([*source_paths(),*extra])}';assert text.count(needle)==1
        text=text.replace(needle,'    extra += [A/n for n in '+repr(extras)+']\n'+needle)
        family=save(family_name,text);new_sources.append(family)
        for p in [normal,q,candidate,pre,runtime,family]:importlib.import_module(p.stem)
        assert not (A/f'{kind}{number}_complete_family_v1_20261010').exists() and not (A/f'{kind}{number}_selected_release_v1_20261010').exists()
        create(A/metadata_new,{'status':'compiled_same_complete48_actual29_receipt_and_prevented_future_pointer_collision_selected14_candidate_sources','input_sha256':{str(p):sha(p) for p in [Path(__file__),normal_old,qualifier_old,candidate_old,pre_old,runtime_old,actual_family_old,*new_sources,recovery]},'expected_records':48,'full_controls':44,'prefix_controls':132,'new_fits':0,'new_quality_scores':0,'actual_future_inference_pending':True,'test_labels_read':False})
        retire_jobs += [old_queue,old_selected,f'{kind}{number}_complete48_family_v'+('2' if namespace=='rank5' else '3')+'_20261010']
        jobs += [(new_queue,normal),(new_selected,q),(f'{kind}{number}_complete48_family_v{family_version}_20261010',family)]
    for old,new,old_service,new_service in [('publish_stock_rank5_embedding_after171_large29_completion_v65_20261010.py','publish_stock_rank5_embedding_after171_large29_completion_v69_20261010.py','actual_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010','actual_Rank5_large29_verified_terminal_recovery_v1_20261010'),('publish_stock_forward5_embedding_after171_large29_completion_v68_20261010.py','publish_stock_forward5_embedding_after171_large29_completion_v70_20261010.py','actual_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010','actual_stock_forward5_embedding_after171_large_allocation29_screen_v2_20261010')]:
        p=A/old;text=p.read_text(encoding='utf8').replace("closed('"+old_service+"')","closed('"+new_service+"')")
        if 'forward5' in new:text=text.replace('run_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010.py',large.name)
        needle='    bank=Path(';position=text.index(needle);text=text[:position]+'    paths += [A/n for n in '+repr([recovery.name,Path(__file__).name])+']\n'+text[position:]
        publisher=save(new,text);new_sources.append(publisher)
        jobs.append(('actual_stock_rank5_embedding_after171_large29_completion_main_v69_20261010' if 'rank5' in new else 'actual_stock_forward5_embedding_after171_large29_completion_main_v70_20261010',publisher))
    proof=A/'stock_rank5_forward5_actual29_pointer_and177178_routes_recovery_v3_20261010.json'
    create(proof,{'status':'compiled_actual29_preserved_recovery_main69_and_same48_scientific_routes_prevented_unstarted_forward5_location_collision','input_sha256':{str(p):sha(p) for p in [Path(__file__),*new_sources,recovery]},'retired_helpers_only':retire_jobs,'new_fits':0,'new_quality_scores':0,'no_completed_scores_or_pinned_sources_overwritten':True,'test_labels_read':False})
    for name in retire_jobs:idle(name)
    jobs.insert(0,('actual_stock_forward5_embedding_after171_large_allocation29_screen_v2_20261010',large))
    for name,p in jobs:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'actual_score29_not_rerun':True,'same48_177_family3_and178_family4_started':True,'forward5_terminal_pointer_fixed_before_scoring':True},flush=True)
if __name__=='__main__':main()

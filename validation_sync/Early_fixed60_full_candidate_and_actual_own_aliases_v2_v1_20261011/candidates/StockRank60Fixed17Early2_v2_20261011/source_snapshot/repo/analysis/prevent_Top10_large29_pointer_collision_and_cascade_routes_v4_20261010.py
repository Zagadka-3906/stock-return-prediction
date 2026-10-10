"""Correct an unstarted index writer and route all unchanged pending selection scopes."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();assert not Path('E:/赛题五_本机临时/StockTop10EmbeddingSmall512_after174_large_allocation29_screen_v1_20261010').exists()
    source=A/'run_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010.py';text=source.read_text(encoding='utf8');old='actual_StockTop10EmbeddingSmall512_after174_high_impact17_screen_location_v1_20261010'
    assert text.count(old)==1;text=text.replace(old,'actual_StockTop10EmbeddingSmall512_after174_large_allocation29_screen_location_v1_20261010')
    large=save('run_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010.py',text);assert len(importlib.import_module(large.stem).cases())==29
    source=A/'publish_stock_top10_embedding_after174_large_allocation29_completion_v60_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010','actual_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010').replace('run_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010.py',large.name)
    publisher=save('publish_stock_top10_embedding_after174_large_allocation29_completion_v72_20261010.py',text)
    sources=[large,publisher];jobs=[('actual_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010',large),('actual_stock_top10_embedding_after174_large_allocation29_completion_main_v72_20261010',publisher)]
    retire_jobs=['actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010','actual_stock_top10_embedding_after174_large_allocation29_completion_main_v60_20261010']
    parent_routes={'StockTop10Embedding175_complete47_family_v2_20261010':'StockTop10Embedding175_complete47_family_v3_20261010','StockTop10Embedding176_complete31_family_v2_20261010':'StockTop10Embedding176_complete31_family_v3_20261010','StockRank5Embedding177_complete48_family_v3_20261010':'StockRank5Embedding177_complete48_family_v4_20261010'}
    rows=[('top10','StockTop10Embedding',175,47,'after174','complete47_after174',2,3,2,3),('top10','StockTop10Embedding',176,31,'after175','followup31_after175',2,3,2,3),('rank5','StockRank5Embedding',177,48,'after176','complete48_after176',3,4,3,4),('forward5','StockForward5Embedding',178,48,'after177','complete48_after177',3,4,4,5)]
    for namespace,kind,number,count,after,normalpart,oldver,newver,oldfamilyver,newfamilyver in rows:
        prefix='stock_'+namespace+'_embedding';stem=f'normalize_completed_{prefix}_{normalpart}'
        normal_old=A/f'{stem}_v{oldver}_20261010.py';text=normal_old.read_text(encoding='utf8')
        for old,new in parent_routes.items():text=text.replace("closed('"+old+"')","closed('"+new+"')")
        if number==175:
            needle="        closed(family['actual_service']);receipt=A/family['main_receipt']";assert text.count(needle)==1
            text=text.replace(needle,"        service=family['actual_service']\n        if service=='actual_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010':service='actual_stock_top10_embedding_after174_large_allocation29_screen_v2_20261010'\n        closed(service);receipt=A/family['main_receipt']")
        normal=save(f'{stem}_v{newver}_20261010.py',text);sources.append(normal)
        qualifier_old=A/f'qualify_{prefix}{count}_selected_native14_v{oldver}_20261010.py'
        old_queue=f'actual_{prefix}{count}_{after}_normalization_queue_v{oldver}_20261010';new_queue=old_queue.replace(f'_v{oldver}_',f'_v{newver}_')
        qualifier=save(f'qualify_{prefix}{count}_selected_native14_v{newver}_20261010.py',qualifier_old.read_text(encoding='utf8').replace(normal_old.stem,normal.stem).replace(old_queue,new_queue));sources.append(qualifier)
        old_selected=f'{kind}{count}_selected_native14_v{oldver}_20261010';new_selected=old_selected.replace(f'_v{oldver}_',f'_v{newver}_')
        candidate_old=A/f'prepare_{kind}{number}_selected_candidate_v{oldver}_20261010.py';metadata_old=f'{prefix}{number}_candidate_sources_preparation_v{oldver}_20261010.json';metadata_new=metadata_old.replace(f'_v{oldver}_',f'_v{newver}_')
        text=candidate_old.read_text(encoding='utf8').replace(qualifier_old.stem,qualifier.stem).replace(normal_old.stem,normal.stem).replace(old_selected,new_selected).replace(metadata_old,metadata_new)
        candidate=save(f'prepare_{kind}{number}_selected_candidate_v{newver}_20261010.py',text);sources.append(candidate)
        pre_old=A/f'verify_{kind}{number}_full{count}_preflight_v{oldver}_20261010.py';pre_name=f'verify_{kind}{number}_full{count}_preflight_v{newver}_20261010.py'
        runtime_old=A/f'run_{kind}{number}_full_registration_v{oldver}_20261010.py';runtime_name=f'run_{kind}{number}_full_registration_v{newver}_20261010.py'
        family_old=A/f'run_{kind}{number}_complete_family_v{oldfamilyver}_20261010.py';family_name=f'run_{kind}{number}_complete_family_v{newfamilyver}_20261010.py'
        extras=[Path(__file__).name,normal.name,qualifier.name,candidate.name,metadata_new,large.name,publisher.name]
        if number==178:
            wrapper_old=A/'run_StockForward5Embedding178_selected_candidate_feature_cache_v4_20261010.py'
            wrapper=save('run_StockForward5Embedding178_selected_candidate_feature_cache_v5_20261010.py',wrapper_old.read_text(encoding='utf8').replace(candidate_old.name,candidate.name).replace('runtime_v4','runtime_v5'));sources.append(wrapper);extras.append(wrapper.name)
        text=pre_old.read_text(encoding='utf8').replace(metadata_old,metadata_new).replace(family_old.name,family_name).replace(runtime_old.name,runtime_name)
        marker='    for p in sources:\n';assert text.count(marker)==1;text=text.replace(marker,'    sources += [A/n for n in '+repr(extras)+']\n'+marker)
        pre=save(pre_name,text);sources.append(pre)
        text=runtime_old.read_text(encoding='utf8').replace(metadata_old,metadata_new).replace(family_old.name,family_name).replace(pre_old.name,pre.name)
        for old,new in parent_routes.items():text=text.replace("closed('"+old+"')","closed('"+new+"')")
        needle='    sources=routes.source_paths();assert all(p.is_file() for p in sources)';assert text.count(needle)==1
        text=text.replace(needle,'    inherited_routes=routes.source_paths\n    routes.source_paths=lambda:list(dict.fromkeys([*inherited_routes(),*[A/n for n in '+repr(extras)+']]))\n'+needle)
        runtime=save(runtime_name,text);sources.append(runtime)
        text=family_old.read_text(encoding='utf8').replace(old_selected,new_selected).replace(pre_old.stem,pre.stem).replace(pre_old.name,pre.name).replace(runtime_old.name,runtime.name)
        if number==178:text=text.replace(wrapper_old.name,wrapper.name)
        else:text=text.replace(candidate_old.name,candidate.name)
        needle='    pins={str(p):sha(p) for p in dict.fromkeys([*source_paths(),*extra])}';assert text.count(needle)==1;text=text.replace(needle,'    extra += [A/n for n in '+repr(extras)+']\n'+needle)
        family=save(family_name,text);sources.append(family)
        for p in (normal,qualifier,candidate,pre,runtime,family):importlib.import_module(p.stem)
        assert not (A/f'{kind}{number}_complete_family_v1_20261010').exists() and not (A/f'{kind}{number}_selected_release_v1_20261010').exists()
        create(A/metadata_new,{'status':'compiled_same_scientific_scope_fixed_unstarted29_index_and_exact_parent_service_routes','input_sha256':{str(p):sha(p) for p in [Path(__file__),normal_old,qualifier_old,candidate_old,pre_old,runtime_old,family_old,*sources]},'expected_records':count,'new_fits':0,'new_quality_scores':0,'actual_future_inference_pending':True,'test_labels_read':False})
        old_family_service=f'{kind}{number}_complete{count}_family_v{oldfamilyver}_20261010';new_family_service=old_family_service.replace(f'_v{oldfamilyver}_',f'_v{newfamilyver}_')
        retire_jobs += [old_queue,old_selected,old_family_service];jobs += [(new_queue,normal),(new_selected,qualifier),(new_family_service,family)]
    proof=A/'Top10_large29_pending_index_and_full175178_cascade_admission_v4_20261010.json'
    create(proof,{'status':'compiled_exact_large29_pointer_before_scoring_and_same47_31_48_48_pending_selection_schemes','input_sha256':{str(p):sha(p) for p in [Path(__file__),*sources]},'retired_childless_unstarted_helpers':retire_jobs,'new_quality_scores':0,'new_fits':0,'completed_scores_models_and_pinned_sources_preserved':True,'actual_future_X_read':False,'test_labels_read':False})
    for name in retire_jobs:
        row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json');assert owned(row);retire(row,'Correct prospective Top10 large29 terminal index and route unchanged downstream175178 scopes before any scientific output; childless helper only')
    for name,p in jobs:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'Top10_large29_pointer_fixed_before_scoring':True,'actual_full_families':[175,176,177,178],'scientific_scores_or_models_restarted':0},flush=True)
if __name__=='__main__':main()

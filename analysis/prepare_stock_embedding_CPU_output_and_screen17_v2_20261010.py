"""Separate cache-directory existence from scientific outputs; declare only17 useful trials."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,create,sha
def main():
    prototype=A/'verify_stock_embedding_mature_fixture_and_CPU_v1_20261010.py'
    text=prototype.read_text(encoding='utf8').replace("    assert not OUT.exists();OUT.mkdir(parents=True)","    assert not (OUT/'verification.json').exists() and not (OUT/'past_features121.npy').exists()\n    OUT.mkdir(parents=True,exist_ok=True)")
    cpu=A/'verify_stock_embedding_mature_fixture_and_CPU_v2_20261010.py';assert not cpu.exists();compile(text,str(cpu),'exec');cpu.write_text(text,encoding='utf8',newline='\n')
    original=A/'run_Cross120RecentReturn252_after169_high_impact81_screen_v2_20261010.py'
    text=original.read_text(encoding='utf8')
    begin=text.index('def cases():');end=text.index('\ndef main():',begin)
    cases="""def cases():
    rows=[{'kind':'anchor172','role':None,'weight':0.,'sign':1.,'protect_fraction':None}]
    for sign in (1.,-1.):
        for weight in (.00025,.001,.004,.016):rows.append({'kind':'CDF','role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':None})
    for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
        for weight in (.004,.016,.064,.25):rows.append({'kind':kind,'role':'nonflag_valid','weight':weight,'sign':1.,'protect_fraction':.15})
    assert len(rows)==17;return rows

"""
    text=text[:begin]+cases+text[end:]
    begin=text.index("    closed('Cross120170_complete132_family_v5_20261010')");end=text.index('    import numpy as np,polars as pl,psutil',begin)
    admission="""    closed('Frontier133172_complete133_family_v2_20261010')
    closed('actual_stock_embedding_small512_bank6_v1_20261010')
    closed('StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009')
    release=read(A/'github_validation_sync_main_20261005/round172_receipt.json')
    assert release['status']=='pushed_and_remote_head_verified' and release['scored_records']==133
"""
    text=text[:begin]+admission+text[end:]
    text=text.replace('Cross120RecentReturn252_after169_high_impact81_screen_v1_20261010','StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010')
    text=text.replace('neural_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009','stock_embedding_small512_BF16_bank6_v1_20261010')
    text=text.replace("fullpointer=A/'actual_BF16Cross120RecentReturn252Huber050175_full5_independent_location_v1_20261009.json';nativepointer=A/'actual_BF16Cross120RecentReturn252Huber050175_native42_calendar_location_v1_20261009.json'","fullpointer=A/'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json';nativepointer=fullpointer")
    text=text.replace("    assert read(native/'verification.json')['actual_saved_states']==6 and read(native/'verification.json')['actual_cold_cases']==42","    assert read(native/'verification.json')['actual_complete_bank_fits']==6\n    assert len(read(native/'verification.json')['records'])==5")
    text=text.replace('optimization_20261003_r169','optimization_20261003_r172').replace('anchor169','anchor172').replace('parent_round\':169','parent_round\':172').replace('complete_parent169','complete_parent172').replace('after169','after172')
    text=text.replace('cross120recent252returnhuber050','stock_embedding16_cross120_return1d_recent252_small512_BF16_e24')
    text=text.replace('81','17').replace("'actual_nonidentity_full_controls':80","'actual_nonidentity_full_controls':16").replace("'actual_nonidentity_prefix_controls':240","'actual_nonidentity_prefix_controls':48")
    #80-day control length is fixed scientifically and must survive only record-count edits.
    assert 'for days in (80,260,975)' in text
    text=text.replace('after_own6_full5_native42_qualification','after_own6_full5_independent_qualification_selected_six_state_stage_pending')
    text=text.replace('own120_one_day_return','own_stock_embedding_one_day_return').replace('own120_return1d','own_stock_embedding_return1d')
    screen=A/'run_stock_embedding_after172_high_impact17_screen_v1_20261010.py';assert not screen.exists();compile(text,str(screen),'exec');screen.write_text(text,encoding='utf8',newline='\n')
    plan=__import__(screen.stem).cases()
    create(A/'stock_embedding_after172_predeclared17_selection_plan_v1_20261010.json',{'status':'predeclared_before_any_stock_embedding_quality_scores','cases':plan,'configuration':__import__('stock_embedding_small512_BF16_native_v1_20261010').CONFIG,'expected_scores':17,'nonidentity_full_controls':16,'nonidentity_prefix_controls':48,'fully_qualified_parent_round':172,'physical_models_addition':1,'all_training_only_and_mature':True,'future_X_for_selection':False,'test_labels_read':False,'actual_GPU_restart_training_and_selected_stage_pending':True,'input_sha256':{str(p):sha(p) for p in [Path(__file__),prototype,cpu,original,screen,A/'stock_embedding_small512_sources_admission_v1_20261010.json',A/'stock_embedding_actual_full5_routes_admission_v2_20261010.json']}})
    print({'new_CPU_driver':cpu.name,'predeclared_quality_cases':len(plan)},flush=True)
if __name__=='__main__':main()

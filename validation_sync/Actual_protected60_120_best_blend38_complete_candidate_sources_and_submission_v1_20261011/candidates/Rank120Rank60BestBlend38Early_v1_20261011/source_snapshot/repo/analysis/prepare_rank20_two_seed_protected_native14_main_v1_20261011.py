"""Publish frozen selected-tail decoder sources and only actual completed selected controls."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    source=A/'publish_rank20_two_seed_protected37_stages_main_v1_20261011.py'
    text=source.read_text(encoding='utf8')
    old="[('sources',()),('official37',('actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011',))]"
    assert text.count(old)==1
    text=text.replace(old,"[('sources_selected14',()),('selected14',('actual_rank20_two_seed_protected_selected_native14_v1_20261011',))]")
    marker="paths=[Path(__file__),template,ROOT/'后续选模标准.md'"
    assert text.count(marker)==1
    extra=['prepare_rank20_two_seed_protected_native14_main_v1_20261011.py',
        'prepare_rank20_two_seed_protected_selected14_v1_20261011.py',
        'rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011.py',
        'verify_rank20_two_seed_protected_selected_native14_v1_20261011.py',
        'rank20_two_seed_protected_selected_native14_sources_admission_v1_20261011.json']
    text=text.replace(marker,"paths=[Path(__file__),*[A/n for n in "+repr(extra)+"],template,ROOT/'后续选模标准.md'")
    needle="        paths=list(dict.fromkeys(p for p in paths"
    assert text.count(needle)==1
    text=text.replace(needle,"        folder=Path('E:/赛题五_本机临时/rank20_two_seed_protected_selected_native14_v1_20261011')\n        if folder.exists():paths += list(folder.glob('*.json'))\n"+needle)
    start=text.index("        if stage=='official37':");end=text.index('        text=text[:start]',start)
    replacement="""        manifest['planned_selected_native_cases']=7
        manifest['planned_selected_cold_cases']=7
        if stage=='selected14':
            pointer=A/'actual_rank20_two_seed_protected_selected_native14_location_v1_20261011.json'
            verification=read(Path(read(pointer)['output'])/'verification.json')
            native=verification['actual_native_cases'];cold=verification['actual_cold_cases']
            assert (native,cold) in ((0,0),(7,7))
            manifest['actual_native_cases']=native;manifest['actual_cold_cases']=cold
            manifest['actual_prefit_refusals']=len(verification.get('prefit_rejections',[]))
            manifest['qualified_anchor_reuse_only']=native==0
            manifest['best_TRAIN_score']=verification['best']['connected_final_score']
"""
    text=text[:start]+replacement+text[end:]
    driver=A/'publish_rank20_two_seed_protected_native14_stages_main_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed()
    name='actual_Rank20_two_seed_protected_native14_stages_main_v1_20261011'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(Path(__file__)):sha(__file__)})
    create(A/(name+'_activation.json'),row)
    print({'selected_native14_publication_queued':True,'actual_checks_pending':True},flush=True)

if __name__=='__main__':main()

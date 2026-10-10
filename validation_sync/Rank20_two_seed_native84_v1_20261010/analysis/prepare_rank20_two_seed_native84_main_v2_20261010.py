"""Publish separately frozen native-stage sources and the actual84 checks when completed."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();source=A/'publish_rank20_two_seed_stages_main_v1_20261010.py';text=source.read_text(encoding='utf8')
    old="[('sources',()),('official49',('actual_rank20_two_seed_after175_complement49_screen_v1_20261010',))]"
    assert text.count(old)==1;text=text.replace(old,"[('sources_native84',()),('native84',('actual_rank20_two_seed_native84_v1_20261010',))]")
    marker="paths=[Path(__file__),template,ROOT/'后续选模标准.md'";assert text.count(marker)==1
    text=text.replace(marker,"paths=[Path(__file__),A/'prepare_rank20_two_seed_native84_main_v2_20261010.py',A/'rank20_two_seed_after_qualified_parent_native_stage_v1_20261010.py',A/'verify_rank20_two_seed_six_pair_states_native84_v1_20261010.py',template,ROOT/'后续选模标准.md'")
    start=text.index("        if stage=='official49':");end=text.index('        text=text[:start]',start)
    replacement="""        manifest['planned_native_cases']=84
        if stage=='native84':
            pointer=A/'actual_rank20_two_seed_native84_location_v1_20261010.json'
            verification=read(Path(read(pointer)['output'])/'verification.json')
            assert verification['actual_saved_states']==12 and verification['actual_native_cases']==84 and verification['actual_cold_cases']==84
            manifest['actual_native_cases']=84;manifest['actual_cold_cases']=84
            manifest['actual_prefit_refusals']=len(verification['prefit_rejections'])
"""
    text=text[:start]+replacement+text[end:]
    driver=A/'publish_rank20_two_seed_native84_stages_main_v2_20261010.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed();row=start_service('actual_Rank20_two_seed_native84_stages_main_v2_20261010',driver.name,[],{str(driver):sha(driver),str(Path(__file__)):sha(__file__)})
    create(A/'actual_Rank20_two_seed_native84_stages_main_v2_20261010_activation.json',row)
    print({'native84_publication_queued':True,'native84_not_claimed_passed':True},flush=True)
if __name__=='__main__':main()

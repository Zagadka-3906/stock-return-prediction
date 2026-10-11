"""Complete151 drafts under fresh receiver names and preserve four verified empty outputs from first attempt."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]

def main():
    original=A/'prepare_RFFSparse151_core_receiver_drafts_v1_20261009.py'
    source=original.read_text(encoding='utf8')
    import prepare_RFFSparse151_core_receiver_drafts_v1_20261009 as first
    for name in first.FILES.values():source=source.replace(name.removesuffix('.py'),name.removesuffix('.py').replace('_v1_20261009','_v2_20261009'))
    source=source.replace('RFFSparse151_core_receiver_draft_preparation_v1_20261009','RFFSparse151_core_receiver_draft_preparation_v2_20261009')
    marker="    source=source.replace('PREVIOUS_FULL_151_PLACEHOLDER','HuberSparse59_round150_full_registration_v1_20261008')"
    assert source.count(marker)==1
    source=source.replace(marker,"    source=source.replace('round150','round151')\n"+marker)
    before="        assert not logical.exists() and not physical.exists(),(logical,physical)\n        physical.mkdir(parents=True,exist_ok=False);logical.parent.mkdir(parents=True,exist_ok=True)"
    after="""        if logical.exists():
            storage.empty(logical);outputs.append({'logical':str(logical),'physical':str(physical),'empty_junction_verified':True,'retained_from_first_partial_preparation':True});continue
        assert not physical.exists(),(logical,physical)
        physical.mkdir(parents=True,exist_ok=False);logical.parent.mkdir(parents=True,exist_ok=True)"""
    assert source.count(before)==1;source=source.replace(before,after)
    source=source.replace("plan=copy.deepcopy(read(oldplan))","plan=copy.deepcopy(proposal)")
    marker="anchor_rounds=proposal['anchor_rounds'],heads=proposal['heads'],new_cases=proposal['new_cases'][1:],graph_key='nonflag_CPU_RFFSparse_complete_parent_CDF')"
    assert source.count(marker)==1
    source=source.replace(marker,"anchor_rounds=proposal['anchor_rounds'],heads=proposal['heads'],new_cases=proposal['new_cases'][1:],graph_key='nonflag_CPU_RFFSparse_complete_parent_CDF',round=151,QA_version=62,wave=434,expected_scored_cases=59,existing_saved_native_heads=20,actual_full_OOF_heads=4,original_proposal_sha256=sha(proposal_path))")
    source=source.replace('[Path(__file__),*originals,','[Path(__file__),A/\'prepare_RFFSparse151_core_receiver_drafts_v1_20261009.py\',*originals,')
    ns={'__name__':'actual151_six_drafts_new_names_and_verified_empty_output_reuse','__file__':str(Path(__file__))}
    exec(compile(source,str(original),'exec'),ns);ns['main']()
if __name__=='__main__':main()

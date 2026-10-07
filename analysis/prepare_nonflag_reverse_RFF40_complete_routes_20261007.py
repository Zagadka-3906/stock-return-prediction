"""Freeze signed complete scoring/candidate/publication routes before new official scores."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from nonflag_reverse_RFF123_route_mapping_20261007 import convert
def main():
    names=['run_nonflag_RFFRidge40_official_comparison_v1_20261007.py',
      'prepare_nonflag_RFFRidge40_selected_candidate_v1_20261007.py','seal_nonflag_RFFRidge40_selected_candidate_v1_20261007.py',
      'run_nonflag_RFFRidge40_admitted_comparison_v2_20261007.py','run_nonflag_RFFRidge40_round122_full_registration_v2_20261007.py',
      'publish_nonflag_RFFRidge40_evidence_v2_20261007.py','verify_nonflag_RFFRidge40_round122_sources_v2_20261007.py',
      'verify_nonflag_RFFRidge40_prospective_routes_v2_20261007.py','predict_nonflag_residual_RFFRidge_complete_scheme_20261007.py']
    generated={};originals=[]
    for name in names:
        old=A/name;originals.append(old);new=A/convert(name);assert not new.exists(),new
        text=convert(old.read_text(encoding='utf8'))
        if name.startswith('run_nonflag_RFFRidge40_official'):
            needle="    assert len(cases)==plan['expected_scored_records']==40";assert text.count(needle)==1
            text=text.replace(needle,"    assert plan['residual_sign']==-1\n    for cfg in cases:\n        if cfg['model'] is not None:cfg['residual_sign']=-1\n"+needle)
            text=text.replace('Score88 predeclared refinements','Score40 predeclared reverse-residual refinements')
        if name.startswith('prepare_'):
            needle="            graph['nonflag_CPU_RFFRidge_residual_CDF']={**cfg";assert text.count(needle)==1
            text=text.replace(needle,"            assert cfg['residual_sign']==-1\n"+needle)
        if name.startswith('verify_'):
            text=text.replace("'cfg':{'model':model,", "'cfg':{'residual_sign':-1,'model':model,")
            needle="graph['nonflag_CPU_RFFRidge_residual_CDF']['ordered_equal_mean_components']=="
            if needle in text:
                # Check the persisted graph sign in every native-component branch.
                text=text.replace(needle,"graph['nonflag_CPU_RFFRidge_residual_CDF']['residual_sign']==-1 and "+needle)
        if name.startswith('publish_nonflag'):
            text=text.replace('非涨停残差随机傅里叶Ridge','非涨停残差随机傅里叶Ridge反向融合')
            text=text.replace('各12幅度','各12负向幅度')
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');generated[str(new)]=sha(new)
    paths=[Path(__file__),A/'nonflag_reverse_RFF123_route_mapping_20261007.py',A/'prepare_nonflag_reverse_RFF40_round123_sources_v1_20261007.py',*originals]
    create(A/'nonflag_reverse_RFF40_science_route_preparation_20261007.json',
      {'status':'compiled_fresh_complete_reverse_RFF123_scoring_freeze_replay_and_publication_routes',
       'input_sha256':{**generated,**{str(p):sha(p) for p in paths}},'actual_official_scores':0,
       'actual_full123_admission_not_yet_claimed':True,'test_labels_read':False})
    import verify_nonflag_reverse_RFF40_prospective_routes_v1_20261007 as verifier
    verifier.main()
if __name__=='__main__':main()

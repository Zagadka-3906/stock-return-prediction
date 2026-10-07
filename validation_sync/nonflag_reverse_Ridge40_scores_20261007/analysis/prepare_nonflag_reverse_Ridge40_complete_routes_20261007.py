"""Prepare signed linear routes with all old nonflag branches explicitly removed."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from nonflag_reverse_Ridge124_route_mapping_20261007 import convert
def main():
    names=['run_nonflag_reverse_RFF40_official_comparison_v1_20261007.py',
      'prepare_nonflag_reverse_RFF40_selected_candidate_v1_20261007.py','seal_nonflag_reverse_RFF40_selected_candidate_v1_20261007.py',
      'run_nonflag_reverse_RFF40_admitted_comparison_v1_20261007.py','run_nonflag_reverse_RFF40_round123_full_registration_v1_20261007.py',
      'publish_nonflag_reverse_RFF40_evidence_v1_20261007.py','verify_nonflag_reverse_RFF40_round123_sources_v1_20261007.py',
      'verify_nonflag_reverse_RFF40_prospective_routes_v1_20261007.py','predict_nonflag_reverse_RFF_complete_scheme_20261007.py']
    generated={};originals=[]
    for name in names:
        old=A/name;originals.append(old);new=A/convert(name)
        assert not (A/'nonflag_reverse_Ridge40_round124_source_admission_v1_20261007.json').exists()
        text=convert(old.read_text(encoding='utf8'))
        if name.startswith('prepare_'):
            needle="        assert info['year']==2025 and info['parameters']['n_components']==32\n        assert info['parameters']['gamma'] in (.03125,.25) and info['parameters']['random_state']==20261007"
            assert text.count(needle)==1
            text=text.replace(needle,"        assert info['year']==2025 and info['parameters']['solver']=='cholesky'")
            needle="\n        graph.pop('nonflag_CPU_Ridge_residual_CDF',None)";assert text.count(needle)==1
            text=text.replace(needle,needle+"\n        graph.pop('nonflag_CPU_RFFRidge_residual_CDF',None)")
        if name.startswith('verify_'):
            text=text.replace("and 'nonflag_CPU_Ridge_residual_CDF' not in graph","and 'nonflag_CPU_RFFRidge_residual_CDF' not in graph")
            text=text.replace("'nonflag_CPU_Ridge_residual_CDF':{'old_linear_branch':'must_be_removed'}",
              "'nonflag_CPU_Ridge_residual_CDF':{'old_linear_branch':'must_be_removed'},'nonflag_CPU_RFFRidge_residual_CDF':{'old_fourier_branch':'must_be_removed'}")
        if name.startswith('publish_'):
            text=text.replace('随机傅里叶Ridge反向融合','线性Ridge反向融合')
        text=text.replace("'nonflag_cpu_ridge_','nonflag_cpu_ridge_'", "'nonflag_cpu_ridge_','nonflag_cpu_rffridge_'")
        text=text.replace("'nonflag_residual_ridge','nonflag_residual_ridge'", "'nonflag_residual_ridge','nonflag_residual_rffridge'")
        compile(text,str(new),'exec')
        if new.exists() and new.read_text(encoding='utf8')!=text:
            saved=A/'nonflag_reverse_Ridge40_unadmitted_preparation_first_attempt_20261007'/new.name
            assert saved.exists() and sha(saved)==sha(new),new
            assert not (A/'nonflag_reverse_Ridge40_official_comparison_v1_20261007').exists()
            assert not (A/'service_owned_workflows_20261006/nonflag_reverse_Ridge40_official_comparison_v1').exists()
            new.write_text(text,encoding='utf8',newline='\n')
        elif not new.exists():new.write_text(text,encoding='utf8',newline='\n')
        generated[str(new)]=sha(new)
    paths=[Path(__file__),A/'nonflag_reverse_Ridge124_route_mapping_20261007.py',A/'prepare_nonflag_reverse_Ridge40_round124_sources_v1_20261007.py',*originals]
    create(A/'nonflag_reverse_Ridge40_science_route_preparation_20261007.json',
      {'status':'compiled_fresh_complete_reverse_Ridge124_scoring_freeze_replay_and_publication_routes',
       'input_sha256':{**generated,**{str(p):sha(p) for p in paths}},'actual_official_scores':0,
       'actual_full124_admission_not_yet_claimed':True,'test_labels_read':False})
    import verify_nonflag_reverse_Ridge40_prospective_routes_v1_20261007 as verifier
    verifier.main()
if __name__=='__main__':main()

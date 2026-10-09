"""Build fresh complete routes with actual RFF metadata and replaced old nonflag branches."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from nonflag_RFFRidge122_route_mapping_20261007 import convert
def main():
    paths=['run_nonflag_Ridge40_official_comparison_v1_20261007.py',
        'prepare_nonflag_Ridge40_selected_candidate_v1_20261007.py','seal_nonflag_Ridge40_selected_candidate_v1_20261007.py',
        'run_nonflag_Ridge40_admitted_comparison_v2_20261007.py','run_nonflag_Ridge40_round121_full_registration_v2_20261007.py',
        'publish_nonflag_Ridge40_evidence_v2_20261007.py','verify_nonflag_Ridge40_round121_sources_v2_20261007.py',
        'verify_nonflag_Ridge40_prospective_routes_v2_20261007.py','predict_nonflag_residual_Ridge_complete_scheme_20261007.py']
    generated={}
    for name in paths:
        old=A/name;new=A/convert(name);assert not new.exists();text=convert(old.read_text(encoding='utf8'))
        if name.startswith('prepare_'):
            needle="        assert info['year']==2025 and info['parameters']['solver']=='cholesky'"
            assert text.count(needle)==1
            text=text.replace(needle,"        assert info['year']==2025 and info['parameters']['n_components']==32\n        assert info['parameters']['gamma'] in (.03125,.25) and info['parameters']['random_state']==20261007")
            text=text.replace("        graph.pop('nonflag_CPU_HGB_residual_CDF',None)","        graph.pop('nonflag_CPU_HGB_residual_CDF',None)\n        graph.pop('nonflag_CPU_Ridge_residual_CDF',None)")
            text=text.replace("('nonflag_cpu_hgb_','nonflag_cpu_rffridge_')","('nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_rffridge_')")
            text=text.replace("('nonflag_residual_hgb','nonflag_residual_rffridge')","('nonflag_residual_hgb','nonflag_residual_ridge','nonflag_residual_rffridge')")
        if name.startswith('verify_nonflag_Ridge40_round'):
            text=text.replace("if not key.startswith(('nonflag_cpu_hgb_','nonflag_cpu_rffridge_'))","if not key.startswith(('nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_rffridge_'))")
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}", "'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'},'nonflag_CPU_Ridge_residual_CDF':{'old_linear_branch':'must_be_removed'}")
            text=text.replace("assert 'nonflag_CPU_HGB_residual_CDF' not in graph","assert 'nonflag_CPU_HGB_residual_CDF' not in graph and 'nonflag_CPU_Ridge_residual_CDF' not in graph")
        if name.startswith('verify_nonflag_Ridge40_prospective'):
            text=text.replace("'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}", "'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'},'nonflag_CPU_Ridge_residual_CDF':{'old_linear_branch':'must_be_removed'}")
            text=text.replace("assert 'nonflag_CPU_HGB_residual_CDF' not in graph","assert 'nonflag_CPU_HGB_residual_CDF' not in graph and 'nonflag_CPU_Ridge_residual_CDF' not in graph")
            text=text.replace('for n in (119,120)','for n in (120,121)')
        if name.startswith('publish_nonflag'):
            # Publish local RFF controls only after its actual bank publication, which waits for prior writers.
            text=text.replace('非涨停残差Ridge','非涨停残差随机傅里叶Ridge')
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');generated[str(new)]=sha(new)
    compatible=A/'nonflag_residual_RFFRidge_compatible_parent_20261007.py';assert not compatible.exists()
    compatible.write_text("from nonflag_residual_Ridge_compatible_parent_20261007 import core as parent_core\nfrom copy import deepcopy\ndef core(graph):\n    value=deepcopy(graph);value.pop('nonflag_CPU_RFFRidge_residual_CDF',None);return parent_core(value)\ndef compatible(graph,reference_graph):\n    return core(graph)==core(reference_graph)\n",encoding='utf8',newline='\n')
    generated[str(compatible)]=sha(compatible)
    create(A/'nonflag_RFFRidge40_science_route_preparation_20261007.json',{'status':'compiled_fresh_complete_RFFRidge122_scoring_freeze_replay_and_publication_routes',
        'input_sha256':generated,'actual_official_scores':0,'actual_full122_admission_not_yet_claimed':True,'test_labels_read':False})
    import verify_nonflag_RFFRidge40_prospective_routes_v1_20261007 as verifier
    verifier.main()
if __name__=='__main__':main()

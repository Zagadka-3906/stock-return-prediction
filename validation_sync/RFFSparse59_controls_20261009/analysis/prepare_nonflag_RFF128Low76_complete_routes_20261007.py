"""Compile fresh weaker-L2 76-case routes and execute prospective schema/graph checks."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from nonflag_RFF128Low126_route_mapping_20261007 import convert

def main():
    names=['run_nonflag_RFF12876_official_comparison_v1_20261007.py',
      'prepare_nonflag_RFF12876_selected_candidate_v1_20261007.py','seal_nonflag_RFF12876_selected_candidate_v1_20261007.py',
      'run_nonflag_RFF12876_admitted_comparison_v1_20261007.py','run_nonflag_RFF12876_round125_full_registration_v1_20261007.py',
      'publish_nonflag_RFF12876_evidence_v1_20261007.py','verify_nonflag_RFF12876_round125_sources_v1_20261007.py',
      'verify_nonflag_RFF12876_prospective_routes_v1_20261007.py','predict_nonflag_residual_RFF128_complete_scheme_20261007.py']
    sources=[];generated=[]
    for name in names:
        old=A/name;new=A/convert(name);assert not new.exists(),new
        text=convert(old.read_text(encoding='utf8'))
        if name.startswith('prepare_'):
            needle="        graph.pop('nonflag_CPU_Ridge_residual_CDF',None)";assert text.count(needle)==1
            text=text.replace(needle,needle+"\n        graph.pop('nonflag_CPU_RFFRidge_residual_CDF',None)")
            needle="assert info['parameters']['alpha']>0.";assert text.count(needle)==1
            text=text.replace(needle,"assert info['parameters']['alpha_per_training_row']==.0025 and info['parameters']['alpha']==info['training_rows']*.0025")
        if name.startswith('verify_'):
            text=text.replace("'nonflag_cpu_rffridge_','nonflag_cpu_rff128low_'", "'nonflag_cpu_rffridge_','nonflag_cpu_rff128_','nonflag_cpu_rff128low_'")
            needle="'old_linear_branch':'must_be_removed'}}";assert text.count(needle)==1
            text=text.replace(needle,"'old_linear_branch':'must_be_removed'},'nonflag_CPU_RFFRidge_residual_CDF':{'old_RFF32':'remove'},'nonflag_CPU_RFF128_residual_CDF':{'old_RFF128':'replace'}}")
            text=text.replace("assert 'nonflag_CPU_HGB_residual_CDF' not in graph and 'nonflag_CPU_Ridge_residual_CDF' not in graph",
                "assert 'nonflag_CPU_HGB_residual_CDF' not in graph and 'nonflag_CPU_Ridge_residual_CDF' not in graph and 'nonflag_CPU_RFFRidge_residual_CDF' not in graph")
            # Retain the already-qualified generic128 stage, codec and graph key.
        if name.startswith('publish_'):
            text=text.replace('共40项','共76项').replace('完整121候选','完整126候选')
        if name.startswith('run_nonflag_RFF12876_round'):
            text=text.replace('预定40项完整官方比较：三个合格锚点、36项非涨停残差Ridge和一个消融',
                              '预定76项完整官方比较：三个合格锚点、72项双向弱正则RFF128残差和一个消融')
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n')
        sources.append(old);generated.append(new)
    paths=[Path(__file__),A/'nonflag_RFF128Low126_route_mapping_20261007.py',
        A/'prepare_nonflag_RFF128Low76_round126_sources_v1_20261007.py',*sources,*generated]
    create(A/'nonflag_RFF128Low76_science_route_preparation_v1_20261007.json',
        {'status':'compiled_fresh_complete_RFF128Low126_both_signs_scoring_freeze_replay_and_publication_routes',
         'input_sha256':{str(p):sha(p) for p in paths},'actual_official_scores':0,
         'actual_full126_admission_not_yet_claimed':True,'test_labels_read':False})
    import verify_nonflag_RFF128Low76_prospective_routes_v1_20261007 as verify
    verify.main()
if __name__=='__main__':main()

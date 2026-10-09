"""Check exact route contracts and saved-code hashes before any selected future-X dispatch."""
from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def literal_assignments(path):
    result={}
    for n in ast.parse(path.read_text(encoding='utf8')).body:
        if isinstance(n,ast.Assign):
            for t in n.targets:
                if isinstance(t,ast.Name):
                    try:result[t.id]=ast.literal_eval(n.value)
                    except (ValueError,TypeError):pass
    return result

def main():
    import prepare_protected162_full_registry_sources_v1_20261010 as routes
    sources=routes.source_paths()
    for name in ('protected162_candidate_sources_preparation_v2_20261010.json','protected162_full_registry_source_preparation_v1_20261010.json'):
        for p,d in read(A/name)['input_sha256'].items():assert sha(p)==d,p
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    opt=literal_assignments(A/'optimize_training_round162.py')
    assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(162,161,(445,))
    register=(A/routes.NAMES[0]).read_text(encoding='utf8')
    for required in ("'expected_scored_records': 76","'waves': [445]","'explicit_parent_round': 161","'BF16_flag_after152157_complete_parent_rank_CDF' in graph","original_complete_parent_round':157",'original_screen_record','official_metric_capsule_sha256'):
        assert required in register,required
    assert not any(line.strip().startswith('original=read(measured') for line in register.splitlines())
    collected=(A/'collect_full_lossless_round162_qa73_20261010.py').read_text(encoding='utf8')
    assert "qa_v{qa_version}_20261010" in collected and '(162, 73, 76)' in collected
    verified=(A/'verify_lossless_ranking_display_round162_v2_20261008.py').read_text(encoding='utf8')
    assert 'lossless_ranking_display_qa_v73_20261010' in verified and "kwargs['timeout'] == 45" in verified and 'new_round_records' in verified
    publication=(A/routes.NAMES[1]).read_text(encoding='utf8')
    for required in ('collect(162, 73, 76)',"namespace['snapshot'](162)","'scored_records': 76","'actual_full_QA_version': 73",'HEAD:refs/heads/main','blob_hashes'):
        assert required in publication,required
    prep=(A/'prepare_protected162_selected_candidate_v2_20261010.py').read_text(encoding='utf8')
    assert 'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009.json' in prep
    assert "transform(raw,neural,dates,flags,valid,cfg['weight'],cfg['protect_fraction'],cfg['sign'])" in prep
    assert 'protected_tail_after_complete157_native_v1_20261010' in prep
    seal=(A/'seal_protected162_selected_candidate_v2_20261010.py').read_text(encoding='utf8')
    assert 'passed_actual76_selected_candidate_full_graph_and_metrics_and_source_bytes' in seal
    assert 'protected_tail_after157_complete_parent_native_replay_verification.json' in seal
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    # The completed37 are real score records; prospective routes do not count as new experiments.
    p=Path('E:/赛题五_本机临时/protected_upper_tail_screen_v1_20261010/verification.json');screen=read(p)
    assert len(screen['records'])==37 and screen['actual_nonidentity_full_controls']==36 and screen['actual_nonidentity_prefix_controls']==108
    for row in screen['records']:
        capsule=Path(row['official_score_cache']['official_metrics_source']);assert sha(capsule)==row['official_metric_capsule_sha256'] and read(capsule)['metrics']==row['metrics']
    create(A/'protected162_full_family_preflight_v1_20261010.json',{'status':'passed_prospective_full76_parent161_QA73_main_routes_and_actual37_source_capsules','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*sources,p]},'expected_scored_records':76,'wave':445,'comparison_parent':161,'scheme_base':157,'actual_completed_screen_records_checked':37,'actual_full_candidate_native_and_QA_still_pending':True,'new_quality_scores':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    print('PASS prospective76 routes, real37 score capsules, original index unchanged',flush=True)

if __name__=='__main__':main()

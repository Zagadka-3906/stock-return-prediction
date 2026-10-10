"""Verify preparation and control bindings without admitting the unfinished receiver drafts."""
from pathlib import Path
import ast, sys, time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    proposal=read(A/'HuberSparse59_round150_proposal_v1_20261008.json')
    plan=read(A/'HuberSparse59_round150_plan_v1_20261008.json')
    preparation=read(A/'HuberSparse150_core_receiver_draft_preparation_v2_20261008.json')
    pointer=read(A/'actual_HuberSparse55_parent134_location_v1_20261008.json')
    control_path=Path(pointer['output'])/'verification.json';controls=read(control_path)
    assert sha(control_path)==pointer['verification_sha256']
    assert len(controls['records'])==55 and len(plan['new_cases'])==54
    assert proposal['new_cases'][1:]==plan['new_cases']
    assert plan['anchor_rounds']==[146,147,148,149] and plan['expected_scored_cases']==59
    for path,digest in preparation['input_sha256'].items():assert sha(path)==digest,path
    grid=[]
    for official_case,case in [(i+4,c) for i,c in enumerate(plan['new_cases'])]+[(58,proposal['new_cases'][0])]:
        matches=[r for r in controls['records'] if r['configuration']==case]
        assert len(matches)==1 and matches[0]['rows']==5635800
        r=matches[0];assert r['full_independent_Pandas_bits_exact'] and r['preserved2020_flag1_invalid_bits_exact']
        assert [x['days'] for x in r['cold_controls']]==[80,260,975]
        assert all(x['native_independent_mixture_and_Pandas_bits_exact'] for x in r['cold_controls'])
        grid.append({'official_case':official_case,'control_case':r['case'],'configuration':case,'expected_numeric_sha256':r['numeric_sha256']})
    import HuberSparse_complete_parent_CDF_v1_20261008 as codec
    counts=sorted({len({h for names,sign in codec.GROUPS[c['group']] for h in names}) for c in plan['new_cases']})
    assert counts==[3,4]
    files=[Path(p) for p in preparation['input_sha256'] if Path(p).name in ('HuberSparse150_storage_v1_20261008.py','verify_HuberSparse150_D_scoring_scope_v1_20261008.py','run_HuberSparse59_official_comparison_v1_20261008.py','prepare_HuberSparse59_selected_candidate_v1_20261008.py','seal_HuberSparse59_selected_candidate_v1_20261008.py','run_HuberSparse59_round150_full_registration_v1_20261008.py')]
    assert len(files)==6
    for p in files:ast.parse(p.read_text(encoding='utf8'))
    for row in preparation['E_outputs']:
        p,t=Path(row['access']),Path(row['physical_E']);assert p.is_junction() and p.resolve()==t.resolve() and not any(t.iterdir())
    create(A/'HuberSparse150_draft_control_bindings_v1_20261008.json',{
        'status':'passed55_declared_control_bindings_and_six_draft_parse_and_empty_E_locations_not_complete_source_admission',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'control_to_official_mapping':grid,'native_component_counts':counts,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),control_path,A/'HuberSparse150_core_receiver_draft_preparation_v2_20261008.json',*files]},
        'required_next':['freeze_prior_complete_forecast_duplicate_audit','add_raw_control_SHA_comparison_to_actual_scorer','allow3_or4_component_guards_in_all_prospective_routes','prepare_canonical_eight_sources_and_phase_isolated_publishers','perform_all32_source_and_graph_preflight','complete_actual149_qualification_before_chronological150_admission'],
        'quality_source_admitted':False,'new_quality_scores':0,'new_future_inference':0,'new_native_fits':0,'test_labels_read':False})
    print({'actual_control_bindings':len(grid),'drafts_parsed':len(files),'verified_empty_E_outputs':6,'quality_admitted':False},flush=True)
if __name__=='__main__':main()

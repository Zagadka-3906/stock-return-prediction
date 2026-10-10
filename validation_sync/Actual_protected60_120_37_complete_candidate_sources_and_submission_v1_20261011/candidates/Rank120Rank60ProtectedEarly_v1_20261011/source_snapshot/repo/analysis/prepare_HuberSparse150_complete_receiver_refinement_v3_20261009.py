"""Refine unadmitted150 drafts: bind55 numeric controls and duplicates, correct status/parent/component contracts."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
MAP={
 'run_HuberSparse59_official_comparison_v1_20261008.py':'run_HuberSparse59_official_comparison_v2_20261009.py',
 'prepare_HuberSparse59_selected_candidate_v1_20261008.py':'prepare_HuberSparse59_selected_candidate_v2_20261009.py',
 'seal_HuberSparse59_selected_candidate_v1_20261008.py':'seal_HuberSparse59_selected_candidate_v2_20261009.py',
 'run_HuberSparse59_round150_full_registration_v1_20261008.py':'run_HuberSparse59_round150_full_registration_v2_20261009.py',
 'prepare_HuberSparse59_round150_sources_v1_20261008':'prepare_HuberSparse59_round150_sources_v2_20261009',
 'passed_actual59_CrossFamily_complete_parent_full_official_comparisons':'passed_actual59_HuberSparse_complete_parent_full_official_comparisons',
 'zero_CrossFamily_residual_identity':'zero_HuberSparse_residual_identity',
 'main_publisher_v8_20261008':'main_publisher_v9_20261009'}
META=A/'HuberSparse150_complete_receiver_refinement_v3_20261009.json'
def replace(s):
    for before,after in MAP.items():s=s.replace(before,after)
    return s
def main():
    originals=[];products=[]
    for old,new in list(MAP.items())[:4]:
        path=A/old;originals.append(path);s=replace(path.read_text(encoding='utf8'))
        if old.startswith('run_HuberSparse59_official'):
            s=s.replace("    closed('PureRFFHuber128_round149_full_registration_v1_20261008')", "    closed('PureRFFHuber128_round149_full_registration_v1_20261008')\n    closed('HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009')")
            marker='    empty(OUT)';assert s.count(marker)==1
            s=s.replace(marker,"    duplicate_path=A/'HuberSparse150_prior_complete_forecast_duplicate_audit_raw_v1_20261009.json';duplicate=read(duplicate_path)\n    assert duplicate['actual_current_cases']==55 and duplicate['known_zero_control_count']==1\n    duplicate_rows={r['control_case']:r for r in duplicate['records']}\n"+marker)
            marker="    parents={n:A/f'optimization_20261003_r{n}' for n in [134,*plan['anchor_rounds']]}";assert s.count(marker)==1
            s=s.replace(marker,"    controlled={(r['configuration']['group'],r['configuration']['share'],r['configuration']['amplitude']):r for r in control['records']}\n    assert len(controlled)==55\n"+marker)
            s=s.replace('sources=[Path(__file__),','sources=[Path(__file__),duplicate_path,A/\'HuberSparse150_complete_receiver_refinement_v3_20261009.json\',')
            s=s.replace("pins={**control['input_sha256'],", "pins={**read(A/'HuberSparse59_round150_source_admission_v1_20261008.json')['input_sha256'],**control['input_sha256'],")
            marker='                mask=codec.selected(dates,flags,valid)';assert s.count(marker)==1
            s=s.replace(marker,"                key=(cfg['group'],cfg['share'],cfg['weight']) if cfg['weight'] else (0,.5,0.)\n                measured=controlled[key];control_case=measured['case']\n                numeric=hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()\n                assert numeric==measured['numeric_sha256']==duplicate_rows[control_case]['numeric_sha256']\n"+marker)
            marker="            capsule=Path(ctx.last_official_score_cache['official_metrics_source'])";assert s.count(marker)==1
            s=s.replace(marker,"            if cfg['model'] is not None:\n                for previous in duplicate_rows[control_case]['prior_full_board_matches']:\n                    assert all(metrics[k]==value for k,value in previous['metrics'].items())\n                    if previous['all8_metrics'] is not None:assert metrics==previous['all8_metrics']\n"+marker)
            s=s.replace("'prediction_numeric_bytes_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),", "'prediction_numeric_bytes_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),\n                'actual_declared55_numeric_control_exact':cfg['model'] is not None,'actual_prior_complete_forecast_duplicate_metric_guards':cfg['model'] is not None,")
            s=s.replace('all121_nonanchors_full_and363_cold_controls_passed','all55_nonanchors_full_and165_cold_controls_passed')
        if old.startswith('run_HuberSparse59_round'):
            s=s.replace('actual_registration_v1_20261008','actual_registration_v2_20261009').replace('full_registration_v1_file_IO','full_registration_v2_file_IO')
        products.append(save(new,s))
    old=A/'prepare_HuberSparse59_round150_sources_v1_20261008.py';originals.append(old)
    # A small wrapper retains the first generator as historical evidence and executes
    # the same complete-source materialization only after the new admission proves it.
    source='''"""Correct prospective150 component counts and explicit comparison-parent paths before any59 score."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_HuberSparse59_round150_sources_v1_20261008 as original
from prepare_HuberSparse150_complete_receiver_refinement_v3_20261009 import MAP,META,replace
NAMES=original.NAMES
def source_paths():
    result=[]
    for path in original.source_paths():
        if path.is_relative_to(A):path=A/replace(path.relative_to(A).as_posix())
        result.append(path)
    result.extend([Path(__file__),Path(original.__file__),META,A/'prepare_HuberSparse150_complete_receiver_refinement_v3_20261009.py',
        A/'verify_HuberSparse59_prospective_routes_v1_20261009.py',A/'HuberSparse59_prospective_routes_v1_20261009.json',
        A/'verify_HuberSparse59_round150_sources_v1_20261009.py',A/'publish_HuberSparse59_evidence_v1_20261009.py',
        A/'verify_HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009.py',
        A/'actual_HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009.json',
        A/'HuberSparse150_prior_complete_forecast_duplicate_audit_raw_v1_20261009.json',
        A/'HuberSparse59_actual_controls_index_v1_20261008.json'])
    return list(dict.fromkeys(result))
def generate(parent):
    result={}
    for name,source in original.generate(parent).items():
        source=replace(source)
        source=source.replace("len(measured['ordered_native_components']) in (2,4)","len(measured['ordered_native_components']) in (3,4)")
        source=source.replace('_r134/',f'_r{parent}/')
        compile(source,str(A/name),'exec');result[name]=source
    return result
def main():
    before=original.read
    namespace={'__file__':str(Path(__file__)),'__name__':'actual_Sparse150_source_materialization'}
    # Main only changes the selected generator call; scientific base paths remain in generate.
    source=Path(original.__file__).read_text(encoding='utf8')
    tree=ast.parse(source);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    namespace.update(read=before,sha=original.sha,create=original.create,A=A,ROOT=ROOT,generate=generate,hashlib=original.hashlib,time=original.time)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(Path(__file__)),'exec'),namespace)
    namespace['main']()
if __name__=='__main__':main()
'''
    products.append(save('prepare_HuberSparse59_round150_sources_v2_20261009.py',source))
    create(META,{'status':'refined_unadmitted150_receiver_source_numeric55_and_duplicate_guards_status_paths_component3or4_comparison_parents',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},
        'new_cases54_plus_identity_and4_anchors_unchanged':True,'actual_previously_passed55_full165_cold72_native_controls_not_rerun':True,
        'complete_prospective_checks_and_actual_prior_duplicate_audit_still_required':True,'quality_admitted':False,
        'new_quality_scores':0,'new_future_inference':0,'new_native_fits':0,'test_labels_read':False})
    print({'refined_receivers':len(products),'quality_admitted':False},flush=True)
if __name__=='__main__':main()

"""Preserve complete native candidate and all original ranking QA for47 blends."""
from pathlib import Path
import ast
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read


def main():
    names={
        'register_longer_residual74_round104_artifacts_20261006.py':'register_simplex_residual47_round106_artifacts_20261006.py',
        'optimize_training_round104.py':'optimize_training_round106.py',
        'finalize_training_round104.py':'finalize_training_round106.py',
        'run_longer_residual74_round104_full_registration_20261006.py':'run_simplex_residual47_round106_full_registration_20261006.py',
        'publish_longer_residual74_round104_full_validation_20261006.py':'publish_simplex_residual47_round106_full_validation_20261006.py',
        'build_lossless_ranking_display_v13_20261006.py':'build_lossless_ranking_display_v15_20261006.py',
        'verify_lossless_ranking_display_v15_20261006.py':'verify_lossless_ranking_display_v17_20261006.py',
        'lossless_ranking_runtime_adapter_v12_20261006.py':'lossless_ranking_runtime_adapter_v14_20261006.py'}
    changes={
        **{old.removesuffix('.py'):new.removesuffix('.py') for old,new in names.items()},
        'conditional_residual128_256_comparison74_20261006':'residual_simplex47_official_comparison_20261006',
        'passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons':
            'passed_actual47_convex_simplex_residual_ensemble_full_official_comparisons',
        'longer_residual74':'simplex_residual47',
        'lossless_ranking_display_qa_v15_20261006':'lossless_ranking_display_qa_v17_20261006',
        'ranking_display_qa_v15_20261006':'ranking_display_qa_v17_20261006',
        'collect(104, 15, 74)':'collect(106, 17, 47)',
        "namespace['snapshot'](104)":"namespace['snapshot'](106)",
        'publish(104,':'publish(106,','lossless(104)':'lossless(106)',
        'assert number == 104':'assert number == 106',
        'actual_complete_QA_version=15':'actual_complete_QA_version=17',
        "'actual_full_QA_version': 15":"'actual_full_QA_version': 17",
        'round104':'round106','_r104':'_r106','NUMBER = 104':'NUMBER = 106',
        'WAVES = (387,)':'WAVES = (389,)','wave=387':'wave=389',
        'wave387_results':'wave389_results',"'waves': [387]":"'waves': [389]",
        "'round': 104":"'round': 106",'== 74':'== 47',
        "'expected_scored_records': 74":"'expected_scored_records': 47",
        "'existing_actual_official_records': 74":"'existing_actual_official_records': 47",
        "'existing_official_scores_registered': 74":"'existing_official_scores_registered': 47",
        "'scored_records': 74":"'scored_records': 47",
        "'original_official_pilot_records_registered': 74":"'original_official_pilot_records_registered': 47",
        'all74':'all47','actual74':'actual47','Register74':'Register47','the74':'the47',
        'official74_scores':'official47_scores',
        'actual_longer_residual104_complete':'actual_simplex_residual106_complete',
        '第104轮':'第106轮','既有74项':'既有47项',
        '预定74项128与256棵树条件残差及集成官方比较':'预定47项四分之一步长凸残差集成官方比较',
        '74项128与256棵树条件残差及集成验证':'47项四分之一步长凸残差集成验证'}
    pins,generated,routes={},{},[]
    for old,new in names.items():
        original=(A/old).read_text(encoding='utf-8');text,effective=original,{}
        for before in sorted(changes,key=len,reverse=True):
            if before in text:
                text=text.replace(before,changes[before]);effective[before]=changes[before]
        if old.startswith('register_'):
            before="'ensemble_components': measured['ensemble_components'],"
            assert text.count(before)==1
            text=text.replace(before,before+
                "\n                'component_repeat_counts': {n: measured['ensemble_components'].count(n) for n in dict.fromkeys(measured['ensemble_components'] or [])},\n"
                "                'original_ordered_ensemble_entries': measured['ensemble_components'],")
            before="'actual_native_bank_fits': 40, 'actual_new_parent_curve_fits': 0,"
            assert text.count(before)==1
            text=text.replace(before,
                "'existing_actual_native_bank_fits': 40, 'actual_new_native_fits_by_this_scope': 0, 'actual_new_parent_curve_fits': 0,")
            before="'all47_full_numeric_and_original_official_capsules_verified': True,"
            assert text.count(before)==1
            text=text.replace(before,before+
                "\n        'actual_ordered_integer_convex_weights': pilot['ensemble_integer_weights'],\n"
                "        'selected_saved_native_storage_counts_unique_components_only': True,")
        if old.startswith('publish_'):
            before='    for path in extra:'
            assert text.count(before)==1
            text=text.replace(before,
                "    extra += list((A / 'residual_simplex47_official_comparison_20261006').glob('*_verification.json'))\n"
                "    extra += [A / 'residual_simplex47_frozen_before_hidden_launch_20261006.json',\n"
                "        A / 'residual_simplex47_hidden_admission_20261006.json',\n"
                "        A / 'run_residual_simplex47_official_comparison_20261006.py',\n"
                "        A / 'publish_residual_simplex47_scores_20261006.py',\n"
                "        A / 'residual_simplex47_scores_github_20261006/receipt.json']\n"
                "    for name in ('residual_simplex47_official_comparison', 'residual_simplex47_scores_evidence_publication'):\n"
                "        service = A / 'service_owned_workflows_20261006' / name\n"
                "        extra += list(service.glob('*.json'))\n"
                "        extra += list(service.glob('*.log'))\n"+before)
        if old.startswith(('build_lossless_','verify_lossless_','lossless_ranking_runtime_')):
            restored=text
            for before in sorted(effective,key=len,reverse=True):restored=restored.replace(effective[before],before)
            assert restored==original,'Full ranking/browser QA logic must remain unchanged'
        compile(text,str(A/new),'exec')
        generated[new]=text;pins[str(A/old)]=sha(A/old)
        routes.append({'source':old,'target':new,'explicit_replacements':effective})
    runner=ast.parse(generated['run_simplex_residual47_round106_full_registration_20261006.py'])
    for name in ('publish','lossless'):
        assert [n.args[0].value for n in ast.walk(runner) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==name]==[106]
    publisher=ast.parse(generated['publish_simplex_residual47_round106_full_validation_20261006.py'])
    assert [[a.value for a in n.args] for n in ast.walk(publisher) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='collect']==[[106,17,47]]
    assert [n.args[0].value for n in ast.walk(publisher) if isinstance(n,ast.Call) and isinstance(n.func,ast.Subscript) and isinstance(n.func.slice,ast.Constant) and n.func.slice.value=='snapshot']==[106]
    optimizer=ast.parse(generated['optimize_training_round106.py'])
    constants={target.id:node.value.value for node in optimizer.body if isinstance(node,ast.Assign) and isinstance(node.value,ast.Constant) for target in node.targets if isinstance(target,ast.Name)}
    assert constants['NUMBER']==106 and constants['PREVIOUS_NUMBER']==100
    for new in generated:assert not (A/new).exists(),new
    prep=A/'simplex_residual47_candidate_workflow_preparation_20261006.json'
    pins.update(read(prep)['input_sha256']);pins[str(prep)]=sha(prep);pins[str(Path(__file__))]=sha(Path(__file__))
    admission=A/'admit_simplex_residual47_round106_full_registration_20261006.py'
    compile(admission.read_text(encoding='utf-8'),str(admission),'exec');pins[str(admission)]=sha(admission)
    for new,text in generated.items():
        with (A/new).open('x',encoding='utf-8') as stream:stream.write(text)
        pins[str(A/new)]=sha(A/new)
    create(A/'simplex_residual47_full_registration_preparation_20261006.json',{
        'status':'prepared_actual47_independent_parent100_branch_full106_QA17',
        'input_sha256':pins,'routes':routes,'actual_AST_collect':[106,17,47],
        'actual_AST_publish_lossless_snapshot_round':106,'explicit_training_parent_round':100,
        'selected74_anchor_and_actual40_component_bank_provenance_preserved':True,
        'ordered_integer_convex_weights_and_unique_native_storage_preserved':True,
        'complete_six_views_browser45s_all_values_full_source_provenance_and_candidate_QA_preserved':True,
        'global_direction_or_resource_exhaustion_claimed':False,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()

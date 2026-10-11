"""Compare both stock-embedding parents with qualified anchors before any new future inference."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
RECIPE='stock_embedding16_cross120_return1d_recent252_small512_BF16_e24'
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    plan=A/'stock_embedding_complete36_after172_selection_plan_v1_20261010.json'
    families=[{'name':f'StockEmbeddingSmall512_after{number}_high_impact17','base_round':number,'records':17,'stage_kind':'stock_embedding_return1d_direct','actual_service':('actual_stock_embedding_after170_fast17_screen_v2_20261010' if number==170 else 'actual_stock_embedding_after172_high_impact17_screen_v2_20261010'),'main_receipt':('stock_embedding17_after170_completion_main_receipt_v53_20261010.json' if number==170 else 'stock_embedding17_completion_main_receipt_v52_20261010.json')} for number in (170,172)]
    create(plan,{'status':'declared_combination_of_two_predeclared17_families_before_second_family_scores','expected_records':36,'fully_qualified_anchors':[170,172],'families':families,'expected_full_controls':32,'expected_prefix_controls':96,'new_quality_scores_by_normalization':0,'selection':'highest_connected_official_S_then_unique_physical_models_then_absolute_weight_then_case','future_X_read_for_selection':False,'test_labels_read':False,'prior_fast170_scores_can_be_reported_but_do_not_change_declared_cases':True})
    original=A/'normalize_completed_frontier133_after171_v1_20261010.py';text=original.read_text(encoding='utf8')
    begin=text.index('from normalize_predeclared_cross120_two_target132_v5_20261010 import RECIPES');end=text.index('\n\ndef main():',begin)
    text=text[:begin]+"RECIPES={"+repr(RECIPE)+":('rank_MLP512_StockEmbedding16_Cross120Recent252ReturnHuber050_seed09_e24','stock_embedding_small512_BF16_bank6_v1_20261010')}"+text[end:]
    text=text.replace('frontier133_after171','stock_embedding_complete36_after172').replace('frontier133_after171_predeclared_training_only_selection_plan_v1_20261010.json',plan.name)
    #The actual plan name is independent of the inherited prototype namespace.
    text=text.replace('stock_embedding_complete36_after172_predeclared_training_only_selection_plan_v1_20261010.json',plan.name)
    text=text.replace('==133','==36').replace('[169,170,171]','[170,172]').replace('for number in (169,170,171):','for number in (170,172):')
    text=text.replace("closed('Frontier233171_complete233_family_v2_20261010')","closed('Frontier133172_complete133_family_v2_20261010')\n    closed('actual_stock_embedding_six_state_native42_v2_20261010')")
    text=text.replace("A/'normalize_predeclared_cross120_two_target132_v5_20261010.py'","A/'stock_embedding_native_stage_and_four_parent_routes_admission_v1_20261010.json'")
    text=text.replace("info['configuration']['epochs']==64","info['configuration']['epochs']==24")
    text=text.replace("cfg.get('recipe','cross120recent252returnhuber050')","cfg.get('recipe',"+repr(RECIPE)+")")
    text=text.replace('(133,128,384)','(36,32,96)').replace('anchors[171]','anchors[172]').replace('pilot133','pilot36')
    text=text.replace('normalized133','normalized36').replace('complete133','complete36').replace("'expected_scored_records':133","'expected_scored_records':36").replace("'actual_nonidentity_full_controls':128","'actual_nonidentity_full_controls':32").replace("'actual_nonidentity_prefix_controls':384","'actual_nonidentity_prefix_controls':96").replace("'actual_comparison_parent_round':171","'actual_comparison_parent_round':172").replace("'actual_records':133","'actual_records':36")
    normalizer=save('normalize_completed_stock_embedding36_after172_v1_20261010.py',text)
    original14=A/'qualify_frontier133_selected_native14_v1_20261010.py';text=original14.read_text(encoding='utf8')
    text=text.replace('frontier133_selected_native14','stock_embedding36_selected_native14').replace('actual_frontier133_after171_normalization_queue_v1','actual_stock_embedding36_after172_normalization_queue_v1').replace('actual_frontier133_2020_TRAIN_native42_controls_v1','actual_stock_embedding_six_state_native42_v2')
    text=text.replace('import frontier133_after_complete_qualified_parent_native_stage_v1_20261010 as stage','import stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage')
    text=text.replace('from normalize_completed_frontier133_after171_v1_20261010 import RECIPES','from normalize_completed_stock_embedding36_after172_v1_20261010 import RECIPES')
    text=text.replace('actual_frontier133_after171_location_v1','actual_stock_embedding_complete36_after172_location_v1').replace('pilot133','pilot36').replace('==133','==36').replace('normalized133','normalized36').replace('anchor133','anchor36')
    text=text.replace('predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py','predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py').replace('frontier133_actual_three_nested_parent_hooks_CPU_controls_v1_20261010.json','stock_embedding_actual_four_nested_parent_hooks_CPU_controls_v1_20261010.json')
    qualifier=save('qualify_stock_embedding36_selected_native14_v1_20261010.py',text)
    n=importlib.import_module(normalizer.stem);q=importlib.import_module(qualifier.stem)
    assert list(n.RECIPES)==[RECIPE] and q.OUT.name=='stock_embedding36_selected_native14_v1_20261010'
    create(A/'stock_embedding_complete36_and_selected14_sources_admission_v1_20261010.json',{'status':'compiled_and_imported_actual36_normalizer_and_selected14_routes','input_sha256':{str(p):sha(p) for p in [Path(__file__),plan,original,original14,normalizer,qualifier]},'expected_records':36,'new_native_fits':0,'new_quality_scores':0,'full_future_candidate173_freeze_replay_and_registration_pending':True})
    for name,driver,receipt in [('actual_stock_embedding36_after172_normalization_queue_v1_20261010',normalizer,'actual_stock_embedding36_after172_normalization_activation_v1_20261010.json'),('StockEmbedding36_selected_native14_v1_20261010',qualifier,'actual_stock_embedding36_selected_native14_activation_v1_20261010.json')]:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver),str(plan):sha(plan)});create(A/receipt,row)
    print('Actual36 complete comparison and exact selected14 controls queued after full172 and both17 main receipts',flush=True)
if __name__=='__main__':main()

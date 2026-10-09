"""Normalize151 status and canonical source names under fresh receivers before any quality admission."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save
FILES={
    'run_RFFSparse59_official_comparison_v2_20261009.py':'run_RFFSparse59_official_comparison_v3_20261009.py',
    'prepare_RFFSparse59_selected_candidate_v2_20261009.py':'prepare_RFFSparse59_selected_candidate_v3_20261009.py',
    'seal_RFFSparse59_selected_candidate_v2_20261009.py':'seal_RFFSparse59_selected_candidate_v3_20261009.py',
    'run_RFFSparse59_round151_full_registration_v2_20261009.py':'run_RFFSparse59_round151_full_registration_v3_20261009.py'}
LABELS={
    'full150':'full151',
    'register_RFFSparse59_round151_artifacts_20261008':'register_RFFSparse59_round151_artifacts_20261009',
    'publish_RFFSparse59_round151_full_validation_20261008':'publish_RFFSparse59_round151_full_validation_20261009',
    'lossless_ranking_runtime_adapter_round151_v2_20261008':'lossless_ranking_runtime_adapter_round151_v2_20261009',
    'RFFSparse59_actual_source_paths_before_registration_20261008':'RFFSparse59_actual_source_paths_before_registration_20261009',
    'run_RFFSparse59_round151_full_registration_v3_file_IO_20261008':'run_RFFSparse59_round151_full_registration_v3_file_IO_20261009',
    'passed_all_actual150_registry':'passed_all_actual151_registry'}

def route(s):
    for old,new in FILES.items():s=s.replace(old,new).replace(old.removesuffix('.py'),new.removesuffix('.py'))
    for old,new in LABELS.items():s=s.replace(old,new)
    return s

def main():
    products=[];originals=[];AST_records=[]
    for old,new in FILES.items():
        p=A/old;originals.append(p);before=p.read_text(encoding='utf8');after=route(before)
        # Every edited AST leaf is a declared string label/import binding; no numeric or arithmetic nodes change.
        class RouteLeaves(ast.NodeTransformer):
            def visit_Constant(self,node):
                if isinstance(node.value,str):node.value=route(node.value)
                return node
            def visit_ImportFrom(self,node):
                if node.module:node.module=route(node.module)
                return self.generic_visit(node)
        expected=RouteLeaves().visit(ast.parse(before))
        assert ast.dump(expected,include_attributes=False)==ast.dump(ast.parse(after),include_attributes=False),(old,new)
        products.append(save(new,after));AST_records.append({'old':old,'new':new,'only_declared_string_and_import_AST_leaves_changed':True,'numeric_constants_operators_and_functions_unchanged':True})
    create(A/'RFFSparse151_receiver_label_refinement_v3_20261009.json',{'status':'passed_four_actual_receiver_AST_label_import_and_canonical_name_refinement_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products,A/'RFFSparse151_core_receiver_draft_preparation_v2_20261009.json']},
        'AST_records':AST_records,'actual55_training_controls_and_native_checks_not_rerun':True,'quality_admitted':False,'new_quality_scores':0,'new_future_inference':0,'new_native_fits':0,'test_labels_read':False})
    print({'receiver_AST_controls':4,'numeric_changes':0,'quality_admitted':False},flush=True)
if __name__=='__main__':main()

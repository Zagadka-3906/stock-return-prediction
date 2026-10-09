from pathlib import Path
import sys,ast,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
import prepare_SparseAfter14829_round152_sources_v1_20261009 as generator
canonical={Path(n).stem for n in generator.NAMES.values()}
cores=[A/n for n in ('run_SparseAfter14829_official_comparison_v2_20261009.py','prepare_SparseAfter14829_selected_candidate_v2_20261009.py','seal_SparseAfter14829_selected_candidate_v2_20261009.py','run_SparseAfter14829_round152_full_registration_v2_20261009.py','verify_SparseAfter14829_round152_sources_v1_20261009.py','publish_SparseAfter14829_evidence_v1_20261009.py')]
entries=[];paths=[Path(__file__),Path(generator.__file__),*cores]
for parent in (148,149,150,151):
 source_map={p.name:p.read_text(encoding='utf8') for p in cores};source_map.update(generator.generate(parent))
 for name,source in source_map.items():
  for node in ast.walk(ast.parse(source)):
   if not isinstance(node,ast.ImportFrom) or not node.module:continue
   module=node.module
   if not any(marker in module for marker in ('round152','SparseAfter148')):continue
   p=A/(module.replace('.','/')+'.py')
   if module in canonical:resolution='declared_canonical_source_generated_after_frozen_selection'
   else:
    assert p.is_file(),(parent,name,module)
    paths.append(p);resolution='existing_current_source'
    if module.startswith('predict_SparseAfter148'):
     tree=ast.parse(p.read_text(encoding='utf8'));assert any(isinstance(n,ast.FunctionDef) and n.name=='predict' for n in tree.body)
   entries.append({'comparison_parent':parent,'caller':name,'module':module,'resolution':resolution})
files=[A/f'run_SparseAfter14829_official_comparison_v{version}_20261009.py' for version in (1,2)]
functions=[]
for p in files:
 tree=ast.parse(p.read_text(encoding='utf8'));functions.append(ast.dump(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='best_key'),include_attributes=False))
assert functions[0]==functions[1];paths.extend(files)
create(A/'SparseAfter148152_static_entry_consistency_v1_20261009.json',{'status':'passed_all_current152_core_and32_generated_module_entries_and_identical_selection_key',
 'input_sha256':{str(p):sha(p) for p in dict.fromkeys(paths)},'entries':entries,'actual_import_entries_checked':len(entries),
 'comparison_parents':[148,149,150,151],'existing_old_best_key_import_AST_identical_to_current_scorer':True,
 'canonical_registration_sources_not_materialized_before_selection':True,'new_future_inference':0,'new_quality_scores':0,'test_labels_read':False})
print({'entry_checks':len(entries),'best_key_AST_identical':True})

"""Generate an exact-version reader and exercise the real scopes for all pending rounds."""
from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed()
 source=A/'shared_live_ranking_report_runtime_v1_20261011.py';text=source.read_text(encoding='utf8')
 text=text.replace('def installed(number):','def installed(number, codec_name=None, verifier_name=None):')
 text=text.replace("importlib.import_module(f'build_lossless_ranking_display_round{number}_v2_20261011')","importlib.import_module(codec_name or f'build_lossless_ranking_display_round{number}_v2_20261011')")
 text=text.replace("importlib.import_module(f'verify_lossless_ranking_display_round{number}_v2_20261011')","importlib.import_module(verifier_name or f'verify_lossless_ranking_display_round{number}_v2_20261011')")
 text += """
@contextmanager
def admitted_installed(number, codec_name, verifier_name):
    from run_dependency_queue_v3_20261006 import read,sha
    proof=read(A/'shared_live_report_exact15_scope_controls_v2_20261011.json')
    assert proof['status']=='passed_actual_all15_exact_codec_QA_namespace_scope_and_restoration_controls'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    row=next(r for r in proof['variants'] if r['number']==number)
    assert (row['codec_name'],row['verifier_name'])==(codec_name,verifier_name)
    with installed(number,codec_name,verifier_name) as state:yield state
"""
 target=A/'shared_live_ranking_report_runtime_v2_20261011.py';ast.parse(text);assert not target.exists();target.write_text(text,encoding='utf8')
 routes=read(A/'verified_canonical_publication_failed_chain38_routes_v1_20261011.json')
 factories=routes['source_factories'][1:]+['prepare_StockRank120Direct201_complete35_pipeline_v7_20261011']
 variants=[];paths=[Path(__file__),source,target,A/'shared_live_ranking_report_actual180_controls_v1_20261011.json',A/'shared_live_ranking_report_scope_controls_v1_20261011.json']
 for name in factories:
  module=importlib.import_module(name);adapter,codec,verifier=[A/p for p in module.NAMES[4:7]]
  tree=ast.parse(codec.read_text(encoding='utf8'))
  number=next(int(n.test.comparators[0].value) for fn in tree.body if isinstance(fn,ast.FunctionDef) and fn.name=='main' for n in fn.body if isinstance(n,ast.Assert) and isinstance(n.test,ast.Compare) and isinstance(n.test.left,ast.Name) and n.test.left.id=='number')
  adapter_text=adapter.read_text(encoding='utf8')
  assert f'from {codec.stem} import main as encode' in adapter_text and f'from {verifier.stem} import main as verify' in adapter_text
  assert "report = json.loads(REPORT.read_text(encoding='utf-8'))" in codec.read_text(encoding='utf8')
  assert "'__name__': 'actual_lossless_ranking_QA'" in verifier.read_text(encoding='utf8')
  variants.append({'number':number,'codec_name':codec.stem,'verifier_name':verifier.stem,'factory':name})
  paths += [Path(module.__file__),adapter,codec,verifier]
 assert [v['number'] for v in variants]==list(range(187,202))
 variantproof=A/'shared_live_report_exact15_variants_admission_v2_20261011.json'
 create(variantproof,{'status':'all15_exact_factory_adapter_codec_verifier_modules_prechecked','variants':variants,'input_sha256':{str(p):sha(p) for p in paths},'actual_scope_controls_pending':True})
 template=A/'verify_shared_live_ranking_report_scope_controls_v1_20261011.py';s=template.read_text(encoding='utf8')
 s=s.replace('def main():','def run_variant(row):')
 s=s.replace('import shared_live_ranking_report_runtime_v1_20261011 as runtime','import shared_live_ranking_report_runtime_v2_20261011 as runtime')
 s=s.replace('    import build_lossless_ranking_display_round187_v2_20261011 as codec\n    import verify_lossless_ranking_display_round187_v2_20261011 as verifier',"    import importlib\n    codec=importlib.import_module(row['codec_name'])\n    verifier=importlib.import_module(row['verifier_name'])")
 s=s.replace("sandbox = Path('E:/赛题五_本机临时/共享榜对象作用域控制_v1_20261011')","sandbox = Path('E:/赛题五_本机临时/共享榜对象精确15作用域控制_v2_20261011')/str(row['number'])")
 s=s.replace("assert not sandbox.exists(); sandbox.mkdir()","assert not sandbox.exists(); sandbox.mkdir(parents=True)")
 s=s.replace('with runtime.installed(187) as state:',"with runtime.installed(row['number'],row['codec_name'],row['verifier_name']) as state:")
 s=s.replace("sandbox/'shared_live_ranking_report_round187_execution_v1_20261011.json'","sandbox/f\"shared_live_ranking_report_round{row['number']}_execution_v1_20261011.json\"")
 start=s.index("    pins = {str(p): sha(p) for p in [Path(__file__)")
 s=s[:start]+"    return {'variant':row,'execution':str(fixture_receipt),'execution_sha256':sha(fixture_receipt)}\n"+"""
def main():
    assert allowed()
    path=A/'shared_live_report_exact15_variants_admission_v2_20261011.json'
    proof=read(path)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    results=[run_variant(row) for row in proof['variants']]
    assert len(results)==15
    pins={**proof['input_sha256'],str(path):sha(path),str(Path(__file__)):sha(__file__)}
    pins.update({r['execution']:r['execution_sha256'] for r in results})
    create(A/'shared_live_report_exact15_scope_controls_v2_20261011.json',
      {'status':'passed_actual_all15_exact_codec_QA_namespace_scope_and_restoration_controls',
       'input_sha256':pins,'variants':proof['variants'],'actual_scope_results':results,
       'full180_original_native_bytes_proof':str(A/'shared_live_ranking_report_actual180_controls_v1_20261011.json'),
       'actual_scientific_rounds_not_executed_by_fixture':True,'new_fits':0,'new_scores':0,'test_labels_read':False})
    print({'actual_exact15_scopes_and_restorations_passed':True},flush=True)

if __name__=='__main__':main()
"""
 driver=A/'verify_shared_live_report_exact15_scope_controls_v2_20261011.py';ast.parse(s);assert not driver.exists();driver.write_text(s,encoding='utf8')
 assert allowed();import runpy;runpy.run_path(str(driver),run_name='__main__')

if __name__=='__main__':main()

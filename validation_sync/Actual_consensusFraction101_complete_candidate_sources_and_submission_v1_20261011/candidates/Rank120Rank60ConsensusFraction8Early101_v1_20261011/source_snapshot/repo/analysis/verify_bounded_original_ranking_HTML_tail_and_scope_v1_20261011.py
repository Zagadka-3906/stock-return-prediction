"""Execute exact original HTML tails for both audit branches, then verify actual scoped restore."""
from pathlib import Path
import sys,ast,copy,json
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
import bounded_original_ranking_HTML_runtime_v1_20261011 as runtime

def tail(source,patched):
    tree=ast.parse(source);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    nodes=function.body;start=next(i for i,n in enumerate(nodes) if ('write_exact_report(output_json' if patched else 'output_json.write_text(json.dumps(report') in ast.unparse(n))
    end=next(i for i,n in enumerate(nodes[start:],start) if ('write_bounded_original_html(output_html' if patched else 'output_html.write_text(page') in ast.unparse(n))
    return compile(ast.fix_missing_locations(ast.Module(body=nodes[start:end+1],type_ignores=[])),'actual_original_ranking_HTML_tail','exec')

def main():
    assert allowed()
    import build_all_model_rankings_20261003 as ranking
    original=Path(ranking.__file__).read_text(encoding='utf-8');patched=runtime.patched_source(original)
    native_code=tail(original,False);bounded_code=tail(patched,True)
    base=Path('E:/赛题五_本机临时/原始完整榜HTML作用域实测_v1_20261011');base.mkdir(exist_ok=False)
    records=[]
    class Root:
        def __init__(self,exists):self.flag=exists
        def __truediv__(self,name):assert name=='results/validation_provenance_erratum_20261003.json';return self
        def exists(self):return self.flag
    class Date:
        @staticmethod
        def now():return Date()
        def strftime(self,format):assert format=='%Y-%m-%d %H:%M';return '2026-10-11 08:00'
    for audit in (False,True):
        for case,rows in enumerate([[],[{'中文':'</script>🚀','negative_zero':-0.,'tiny':1e-7}],['__PROVENANCE_BANNER__','__REPORT_DATE__','__VALIDATION_BEST__','__CONNECTED_COUNT__']]):
            paths=[];notes=[]
            for label,code in [('native',native_code),('bounded',bounded_code)]:
                folder=base/f'{audit}_{case}_{label}';folder.mkdir();report={'notes':[],'rows':copy.deepcopy(rows)}
                def exact(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
                namespace={'PAGE':ranking.PAGE,'ROOT':Root(audit),'report':report,'connected':[{'score':.45144551353324136,'known_restriction':False}],'output_json':folder/'report.json','output_html':folder/'report.html','json':json,'datetime':Date,'write_exact_report':exact,'write_bounded_original_html':runtime.writer.write}
                exec(code,namespace);paths.append((namespace['output_json'],namespace['output_html']));notes.append(report['notes'])
            assert notes[0]==notes[1] and sha(paths[0][0])==sha(paths[1][0]) and sha(paths[0][1])==sha(paths[1][1])
            records.append({'audit':audit,'case':case,'original_final_JSON_bytes_exact':True,'original_final_HTML_bytes_exact':True,'original_note_side_effects_exact':True})
    create(A/'bounded_original_ranking_HTML_actual6_tail_controls_v1_20261011.json',{'status':'passed_actual6_original_builder_HTML_tails_both_audit_branches_JSON_HTML_and_note_side_effects_exact','records':records,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(runtime.__file__),Path(runtime.writer.__file__),Path(ranking.__file__)]},'scope_and_full180_pending':True,'new_fits':0,'new_scores':0,'test_labels_read':False})
    print('Actual6 original tail executions passed; waiting for full180 before installed scope',flush=True)
    closed('actual_bounded_original_ranking_HTML_full180_controls_v1_20261011')
    from byte_exact_ranking_stream_runtime_v1_20261010 import installed as stream
    before=ranking.main
    with stream():
        middle=ranking.main
        with runtime.installed():
            assert ranking.main is not middle
            assert ranking.main.__globals__['write_bounded_original_html'] is runtime.writer.write
            assert ranking.main.__globals__['write_exact_report'] is middle.__globals__['write_exact_report']
        assert ranking.main is middle
    assert ranking.main is before
    create(A/'bounded_original_ranking_HTML_actual_full180_and_scope_admission_v1_20261011.json',{'status':'passed_actual_full180_HTML_bytes_six_original_tail_executions_and_nested_native_writer_scope_restore','input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(runtime.__file__),Path(runtime.writer.__file__),A/'bounded_original_ranking_HTML_actual6_tail_controls_v1_20261011.json',A/'actual_bounded_original_ranking_HTML_full180_location_v1_20261011.json']},'actual_native_scope_installed_and_restored':True,'actual_scientific_ranking_main_not_executed_by_scope_control':True,'all_original_per_round_browser_QA_still_required':True,'scientific_workers_restarted_or_terminated':0,'new_fits':0,'new_scores':0,'test_labels_read':False})
    print('Actual full180, original tails, nested native writer scope and restore passed; future adoption pending',flush=True)

if __name__=='__main__':main()

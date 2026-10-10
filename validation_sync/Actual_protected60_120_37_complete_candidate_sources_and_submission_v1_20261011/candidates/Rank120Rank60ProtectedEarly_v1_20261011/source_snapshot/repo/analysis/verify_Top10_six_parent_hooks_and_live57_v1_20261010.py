"""Execute exact six parent callback expressions and observe actual classifier epochs."""
from pathlib import Path
import sys,ast,copy,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    import predict_stock_top10_embedding_complete_qualified_parent_scheme_v1_20261010 as pred
    proof0=read(A/'stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json');controls=[]
    for entry in proof0['whole_parent_source_hook_admission']:
        source=A/entry['parent'];assert sha(source)==entry['sha256']
        tree=ast.parse(pred.prepared_parent(source.read_text(encoding='utf8')))
        nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ('tail_stage','after_whole')]
        assert len(nodes)==1
        events=[];reports=[];context=object();spec=object();component=object();components=[component];ns=object()
        def prior(a,b,c,d,e):
            assert a is ns and b is context and c==11 and d is spec and (e is component or e is components)
            events.append('actual_parent_stage_before_new_classifier');return 22,{'actual_stub_parent':True}
        def appended(a,b):
            assert a is context and b==22 and len(reports)==1;events.append('classifier_stage_after_whole_parent');return 33
        namespace=dict(ns=ns,spec=spec,component=component,components=components,calls=reports,after_parent=prior,STOCK_TOP10_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT=appended)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[])),str(source)+'::exact_actual_callback_CPU','exec'),namespace)
        assert namespace[nodes[0].name](context,11)==33
        assert events==['actual_parent_stage_before_new_classifier','classifier_stage_after_whole_parent']
        controls.append({'source':str(source),'source_sha256':sha(source),'actual_callback_order':events,'stub_CPU_only_no_saved_model_inference_claimed':True})
    proof=A/'stock_top10_actual_six_parent_callback_CPU_controls_v1_20261010.json'
    create(proof,{'status':'passed_actual_six_source_callback_expressions_whole_parent_then_classifier_CPU_controls','records':controls,'input_sha256':{str(p):sha(p) for p in (Path(__file__),Path(pred.__file__),A/'stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json')},'new_fits':0,'new_quality_scores':0,'actual_future_inference_pending':True})
    old=A/'monitor_fast_optimization_v56_20261010.py';text=old.read_text(encoding='utf8').replace('v56_20261010','v57_20261010').replace('v95_20261010','v97_20261010').replace('v28_20261010','v29_20261010')
    needle="        state['screen_progress']=summaries;state['supplementary_actual_scored_records']=len(rows)"
    assert text.count(needle)==1
    text=text.replace(needle,"""        top_bank=Path('E:/赛题五_本机临时/stock_top10_embedding_small512_BF16_bank6_v1_20261010')
        state['top10_classifier']={'completed_annual_models':[y for y in range(2020,2026) if (top_bank/str(y)/'info.json').exists()], 'bank_stage':read(top_bank/'actual_stage.json') if (top_bank/'actual_stage.json').exists() else None,'checkpoint_files':[{'year':y,'bytes':p.stat().st_size,'mtime':p.stat().st_mtime} for y in range(2020,2026) if (p:=top_bank/str(y)/'checkpoint.joblib').exists()], 'stage_status_is_legacy_text_not_evidence_of_waiting':True,'live_actual_worker':services.get('actual_stock_top10_embedding_small512_bank6_v1_20261010')}
"""+needle)
    needle="        for name in ('Frontier233171_complete233_family_v2_20261010'"
    text=text.replace(needle,"        lines.append(f\"Top10分类：已完成年度模型{len(state['top10_classifier']['completed_annual_models'])}/6；实际训练服务{state['top10_classifier']['live_actual_worker']}。大权重29项官方评分尚待前置验证，未记为完成。\")\n"+needle)
    driver=A/'monitor_fast_optimization_v57_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_fast_optimization_progress_v57_20261010',driver.name,[],{str(driver):sha(driver)});create(A/'actual_fast_optimization_progress_v57_activation_20261010.json',row)
    while not (A/'optimization_live_progress_v57_20261010.json').exists():time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v56_20261010/native_launch.json'),'Successor57 verified: actual Top10 annual completion and checkpoint metadata exposed; original scientific services unchanged.')
    print({'actual_exact_callback_CPU_cases':6,'observer':57},flush=True)
if __name__=='__main__':main()

"""Fresh complete-family versions correct overlapping namespace substitution before any scoring/inference."""
from pathlib import Path
import sys,re,subprocess,importlib,runpy,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import retire
def main():
    assert allowed()
    old=importlib.import_module('prepare_StockRankWide32Embedding181_complete48_pipeline_v1_20261010')
    post={}
    for i,name in enumerate(old.NAMES):post[Path(name).stem]=Path(name).stem.replace('_v3','_v4')
    for i,version in {0:(5,6),1:(5,6),2:(2,3),3:(5,6),4:(2,3),5:(6,7),6:(5,6),7:(5,6),8:(6,7),9:(5,6),10:(3,4),11:(1,2),12:(1,2),13:(1,2)}.items():
        stem=Path(old.EXTRAS[i]).stem;post[stem]=stem.replace('_v'+str(version[0])+'_','_v'+str(version[1])+'_')
    post.update({'actual_stock_rank_wide32_embedding48_after180_normalization_queue_v5_20261010':'actual_stock_rank_wide32_embedding48_after180_normalization_queue_v6_20261010','StockRankWide32Embedding48_selected_native14_v5_20261010':'StockRankWide32Embedding48_selected_native14_v6_20261010','StockRankWide32Embedding181_complete48_family_v6_20261010':'StockRankWide32Embedding181_complete48_family_v7_20261010','stock_rank_wide32_embedding181_full_family_preflight_v2_20261010':'stock_rank_wide32_embedding181_full_family_preflight_v3_20261010','stock_rank_wide32_embedding181_full_execution_sources_admission_v1_20261010':'stock_rank_wide32_embedding181_full_execution_sources_admission_v2_20261010'})
    source=Path(old.__file__);driver=A/'prepare_StockRankWide32Embedding181_complete48_pipeline_v2_20261010.py'
    text=source.read_text(encoding='utf8')
    # Apply simultaneous exact old-name→fresh-name routing to factory literals.
    text=re.sub('|'.join(re.escape(k) for k in sorted(post,key=len,reverse=True)),lambda m:post[m.group()],text)
    needle="    return re.sub(r'\\b91\\b','92',text)";assert text.count(needle)==1
    body="    text=text.replace('embedding16_cross120','embedding32_cross120')\n    post="+repr(post)+"\n    text=re.sub('|'.join(re.escape(k) for k in sorted(post,key=len,reverse=True)),lambda m:post[m.group()],text)\n"+needle
    text=text.replace(needle,body)
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    # Ensure all new files are exclusive and the recipe agrees with the actual
    # native backend; this is a real namespace/configuration check, not inference.
    fresh=importlib.import_module(driver.stem)
    for name in fresh.NAMES+fresh.EXTRAS[:14]:assert not (A/name).exists(),name
    import stock_rank_wide32_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
    originalnormalizer=A/'normalize_completed_stock_rank20_embedding_complete48_after179_v5_20261010.py'
    scope={}
    tree=ast.parse(fresh.route(originalnormalizer.read_text(encoding='utf8')))
    for n in tree.body:
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RECIPES' for t in n.targets):scope['RECIPES']=ast.literal_eval(n.value)
    assert set(scope['RECIPES'])==set(stage.BACKENDS)
    helpers=['actual_stock_rank_wide32_embedding48_after180_normalization_queue_v5_20261010','StockRankWide32Embedding48_selected_native14_v5_20261010','StockRankWide32Embedding181_complete48_family_v6_20261010'];identities=[]
    for name in helpers:
        row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json')
        dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,check=True).stdout
        assert '(idle)' in dump and '    closed (' in dump and '    main (' in dump
        identities.append({'name':name,'identity':row,'actual_idle_wait_stack':dump})
    for item in identities:retire(item['identity'],'Replace only verified idle dependency helper before any 181 scores/inference; exact recipe32 names and fresh source versions.')
    create(A/'capacity181_actual_recipe32_namespace_recovery_v2_20261010.json',{'status':'passed_actual_recipe32_normalizer_to_native_backend_keys_and_exclusive_fresh_sources','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,originalnormalizer,Path(stage.__file__)]},'retired_only_idle_childless_dependency_helpers':identities,'native_backend_keys':list(stage.BACKENDS),'old_sources_preserved':True,'new_fits':0,'new_quality_scores':0,'actual_future_X_read':False})
    assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()

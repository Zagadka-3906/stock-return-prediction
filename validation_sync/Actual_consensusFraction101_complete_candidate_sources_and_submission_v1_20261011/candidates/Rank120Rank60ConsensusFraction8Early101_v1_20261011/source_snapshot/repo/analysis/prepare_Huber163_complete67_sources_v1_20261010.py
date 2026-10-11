"""Derive admitted Huber67 complete qualification from the executed protected162 contract."""
from pathlib import Path
import sys,re,time,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected162_candidate_sources_v2_20261010 import change

def route(s):
    for old,new in [('prepare_protected_tail_pilot76_and_selected_native14_v1_20261010','prepare_Huber_protected_pilot67_and_selected_native14_v1_20261010'),('protected_tail_selected_native14_v1_20261010','protected_Huber_selected_native14_v1_20261010'),('actual_protected_tail_selected_native14_location_v1_20261010','actual_protected_Huber_selected_native14_location_v1_20261010'),('protected_tail_after157_native_stage_v1_20261010','protected_tail_after157_native_stage_v2_20261010'),('predict_protected_tail_after157_complete_scheme_v1_20261010','predict_protected_tail_after157_complete_scheme_v2_20261010'),('protected_tail_after157_native_predictor_preparation_v1_20261010','protected_Huber_after157_native_predictor_preparation_v1_20261010'),('protected_tail_after_complete157_native_v1_20261010','protected_tail_after_complete157_native_v2_20261010'),('TailProtected162','HuberProtected163'),('protected162','protected163'),('round162','round163'),('r162','r163'),('第162','第163'),('ReusedNN161','ReusedNN162'),('r161','r162'),('pilot76','pilot67'),('full76','full67'),('complete76','complete67'),('actual76','actual67'),('all76','all67'),('by_all76','by_all67'),('anchor76','anchor67'),('normalized76','normalized67'),('selected76','selected67'),('QA73','QA74'),('qa73','qa74'),('v73_20261010','v74_20261010')]:s=s.replace(old,new)
    s=re.sub(r'\b162\b','163',s);s=re.sub(r'\b161\b','162',s)
    s=re.sub(r'\b76\b','67',s);s=re.sub(r'\b73\b','74',s);s=re.sub(r'\b445\b','446',s)
    s=s.replace('wave445','wave446');return s

def main():
    outputs={}
    stage=(A/'protected_tail_after157_native_stage_v1_20261010.py').read_text(encoding='utf8')
    stage=route(stage)
    stage=change(stage,"BACKENDS={","BACKENDS={\n 'huber010':('neural_BF16_medium2048_huber010_seed09_e64_native_v1_20261009','neural_BF16_medium2048_huber010_seed09_independent_forward_v1_20261009'),")
    stage=change(stage,"CODECS={'valid_pool_protection_v1'","CODECS={'CDF':'BF16Medium153_complete_parent_rank_CDF_v1_20261009','valid_pool_protection_v1'")
    outputs['protected_tail_after157_native_stage_v2_20261010.py']=stage
    outputs['predict_protected_tail_after157_complete_scheme_v2_20261010.py']=route((A/'predict_protected_tail_after157_complete_scheme_v1_20261010.py').read_text(encoding='utf8'))
    pilot=route((A/'prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py').read_text(encoding='utf8'))
    start=pilot.index("    for name in ('actual_protected_upper_tail_screen")
    end=pilot.index('    import numpy as np',start)
    pilot=pilot[:start]+"    for name in ('actual_Huber010_high_impact65_screen_v1_20261010','TailProtected162_complete76_family_v1_20261010'):closed(name)\n"+pilot[end:]
    start=pilot.index('    recipes={');end=pilot.index('    records=[]',start)
    pilot=pilot[:start]+"    recipes={'huber010':('rank_MLP2048_BF16_Huber010_seed09_e64','neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009')}\n"+pilot[end:]
    pilot=change(pilot,'for n in (157,160,162)','for n in (157,161,162)')
    pilot=change(pilot,'for n in (160,162)','for n in (161,162)')
    start=pilot.index('    for family,codec in ');end=pilot.index('    assert len(records)==67',start)
    block=(A/'prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py').read_text(encoding='utf8')
    bstart=block.index('        pins.update(proof');bend=block.index('    assert len(records)==76',bstart)
    inner=route(block[bstart:bend])
    inner=change(inner,"cfg=dict(source['configuration']);cfg.update(codec=codec,anchor_round=157,role='nonflag_valid',universe='all_current_raw_forecasts')","cfg=dict(source['configuration']);cfg.update(recipe=None if source['case']==0 else 'huber010',codec=None if source['case']==0 else source['configuration']['kind'],anchor_round=157,universe='all_current_raw_forecasts')")
    prefix="    for family in ('Huber010_high_impact65_screen_v1_20261010',):\n        folder=Path('E:/赛题五_本机临时')/family;proof=read(folder/'verification.json')\n        assert len(proof['records'])==65 and proof['actual_nonidentity_full_controls']==64 and proof['actual_nonidentity_prefix_controls']==192\n"
    pilot=pilot[:start]+prefix+inner+pilot[end:]
    outputs['prepare_Huber_protected_pilot67_and_selected_native14_v1_20261010.py']=pilot
    for name in ('protected162_storage_v2_20261010.py','prepare_protected162_selected_candidate_v2_20261010.py','seal_protected162_selected_candidate_v2_20261010.py'):
        text=route((A/name).read_text(encoding='utf8'))
        if name.startswith('prepare_'):
            text=change(text,'parent_number in (157,160,162)','parent_number in (157,161,162)')
            text=change(text,"recipes={'seed09'","recipes={'huber010':'neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009','seed09'")
            text=change(text,"own_pointer={'seed09'","own_pointer={'huber010':'actual_BF16Huber010161_full5_independent_location_v1_20261009.json','seed09'")
        outputs[route(name)]=text
    import prepare_protected162_full_registry_sources_v1_20261010 as oldroutes
    for name in oldroutes.NAMES:
        text=route((A/name).read_text(encoding='utf8'))
        if name.startswith('register_'):
            text=text.replace("['seed09','seed10','drop05','complete157','qualified160','qualified161']","['huber010','complete157','qualified161','qualified162']")
            text=text.replace("[str(A/'protected_upper_tail_screen_plan_v1_20261010.json'),str(A/'protected_official_top_screen_plan_v2_20261010.json')]","[str(Path('E:/赛题五_本机临时/Huber010_high_impact65_screen_v1_20261010/frozen_before_any_new_controls_or_scores.json'))]")
        if name.startswith('publish_'):
            text=text.replace("for family in ('protected_upper_tail_screen_v1_20261010','protected_official_top_screen_v2_20261010'):","for family in ('Huber010_high_impact65_screen_v1_20261010',):")
            start=text.index("    payload[(prefix/'README.md').as_posix()] +=");end=text.index('    previous = sync.git',start)
            text=text[:start]+"    payload[(prefix/'README.md').as_posix()] += ('\\n第163轮：Huber65项实际训练内官方评分，加完整161和162两个合格锚点，共67条；同一2020—2024连接验证。最佳保护低位排序方案执行完整157后新增Huber原生阶段。仅实际选中方案执行两次全量1599600推理、cold80、模型重载；原六视图QA74与GitHub main。全部65项原始评分和控制均保留；未读取测试标签。\\n').encode('utf8')\n"+text[end:]
        outputs[route(name)]=text
    names=[route(n) for n in oldroutes.NAMES]
    paths=[route(p.name) for p in oldroutes.source_paths() if p.name not in ('prepare_protected162_candidate_sources_v2_20261010.py',)]
    paths.append(Path(__file__).name)
    routes="from pathlib import Path\nA=Path(__file__).resolve().parent\nNAMES="+repr(names)+"\ndef source_paths():return [A/n for n in "+repr(list(dict.fromkeys(paths)))+"]\n"
    outputs['prepare_protected163_full_registry_sources_v1_20261010.py']=routes
    for name in ('run_protected162_complete_family_v1_20261010.py','run_protected162_full_registration_v1_20261010.py'):
        text=route((A/name).read_text(encoding='utf8'))
        if name.startswith('run_protected162_complete'):
            text=change(text,"    from protected163_storage", "    from protected163_storage")
            text=change(text,"    assert allowed();closed('HuberProtected163_selected_native14_v1_20261010')","    assert allowed();closed('TailProtected162_complete76_family_v1_20261010')\n    driver=A/'prepare_Huber_protected_pilot67_and_selected_native14_v1_20261010.py'\n    row=start_service('HuberProtected163_selected_native14_v1_20261010',driver.name,[],{str(driver):sha(driver),str(A/'protected_tail_after157_native_stage_v2_20261010.py'):sha(A/'protected_tail_after157_native_stage_v2_20261010.py')})\n    closed('HuberProtected163_selected_native14_v1_20261010')")
        outputs[route(name)]=text
    # Exact callback transformation is unchanged; its source-specific preparation proof is explicit.
    for name,text in outputs.items():compile(text,str(A/name),'exec');assert not (A/name).exists(),name
    for name,text in outputs.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),*(A/n for n in outputs)]}
    proof={'status':'passed_compiled_complete67_derived_sources_before_native_or_future_dispatch','input_sha256':pins,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False}
    for name in ('protected163_candidate_sources_preparation_v2_20261010.json','protected163_full_registry_source_preparation_v1_20261010.json','protected_Huber_after157_native_predictor_preparation_v1_20261010.json'):create(A/name,proof)
    print({'generated':len(outputs),'status':'compiled_only_preflight_and_actual_execution_pending'},flush=True)
if __name__=='__main__':main()

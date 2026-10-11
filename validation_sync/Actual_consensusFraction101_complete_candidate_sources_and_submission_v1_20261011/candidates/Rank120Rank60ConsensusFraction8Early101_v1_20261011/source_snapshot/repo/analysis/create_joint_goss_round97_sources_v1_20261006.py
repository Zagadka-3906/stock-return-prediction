"""Create new, isolated round97 sources; preserve every existing frozen workflow."""
from pathlib import Path

A = Path(__file__).resolve().parent

def change(text, before, after, count=1):
    assert text.count(before) == count, (before, text.count(before), count)
    return text.replace(before, after)

def write(name, text):
    compile(text, str(A/name), 'exec')
    with (A/name).open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)

def main():
    old = (A/'ready_goss_reference_search_engine_v2_20261006.py').read_text(encoding='utf-8')
    text = old.split('\ndef install_refinement(ns,number):')[0]
    text = change(text, '    assert number in (95,96)', '    assert number == 97')
    text = change(text, '    parent_number=84 if number==95 else 95', '    parent_number=95')
    text = change(text, "    previous=importlib.import_module(f'optimize_training_round{parent_number}_v3' if parent_number==95 else f'optimize_training_round{parent_number}_v2')", "    previous=importlib.import_module('optimize_training_round95_v3')")
    text = change(text, 'NEW_MODELS=tuple(bank.CONFIGS) if number==95 else ()', 'NEW_MODELS=tuple(bank.CONFIGS)')
    text = change(text, "GRAPH_FIELD='gradient_sampling_reference_role_scheme_graph' if number==95 else 'gradient_sampling_reference_standalone_scheme_graph'", "GRAPH_FIELD='gradient_sampling_joint_membership_scheme_graph'")
    text = change(text, 'WAVES=(371,372,373,374) if number==95 else (375,376,377)', 'WAVES=(378,379,380)')
    text = change(text, "cfg[ns.GRAPH_FIELD]=append_role_layer(origin) if number==95 else deepcopy(origin)", "cfg[ns.GRAPH_FIELD]=deepcopy(origin)")
    text = change(text, "    def pure(cfg):return graph(cfg)['root']['kind']=='standalone' and graph(cfg)['root']['round']==96", "    def pure(cfg):return False")
    replacements = {
        'ready_goss_reference_release_engine_v2_20261006.py': 'joint_goss_membership_release_engine_v1_20261006.py',
        'predict_ready_goss_reference_scheme_v2_20261006': 'predict_joint_goss_membership_scheme_v1_20261006',
        'check_ready_goss_reference_scheme_v2_20261006.py': 'check_joint_goss_membership_scheme_v1_20261006.py',
        'run_ready_goss_reference_round_v2_20261006.py': 'run_joint_goss_membership_round_v1_20261006.py',
        'verify_ready_goss_reference_generators_v2_20261006.py': 'verify_joint_goss_membership_generators_v1_20261006.py',
        'ready_goss_reference_complete_plan_v2_20261006.json': 'joint_membership_retention_scope_20261006/planned_round97.json',
        'ready_goss_reference_generator_preflight_v2_20261006/verification.json': 'joint_goss_membership_generator_preflight_v1_20261006/verification.json',
        "f'analysis/optimize_training_round{number}_v2.py'": "f'analysis/optimize_training_round{number}_v1.py'",
        "f'analysis/finalize_training_round{number}_v2.py'": "f'analysis/finalize_training_round{number}_v1.py'",
        "f'analysis/run_training_round{number}_v2_pipeline.py'": "f'analysis/run_training_round{number}_v1_pipeline.py'",
    }
    for before, after in replacements.items():
        assert before in text, before
        text = text.replace(before, after)
    text = change(text, 'expected_scored_records\':124 if number==95 else 138', "expected_scored_records':151")
    text = change(text, "'wave_arm_counts':[73,8,18,25] if number==95 else [37,84,17]", "'wave_arm_counts':[73,24,54]")
    text = change(text, "'role_grid':{'roles':ROLES,'weights':WEIGHTS,'new_layer_floor':.98,'refined_floors':RETENTIONS,'additional_shifts':(-.04,-.02,0.,.02,.04)},", "'role_grid':{'roles':ROLES,'membership_weights':grid.WEIGHTS,'first_retentions':grid.RETENTIONS,'final_retentions':grid.FINAL_RETENTIONS,'additional_shifts':grid.DELTAS,'all_local_membership_anchors_positive':True},")
    text = change(text, "'standalone_grid':{'alphas':ALPHAS,'auxiliary':AUXILIARY,'bonus':.3,'model_alpha_offsets':(-.025,0.,.025),'model_bonus_values':(0.,.15,.3),'retentions':RETENTIONS},", "'refinement_target':'Existing GOSS layer95 through new authoritative graph field; historical95 field unchanged',")
    text = change(text, "'standalone_discards_predecessor_root_andall_role_layers':True,", "'parent_root_and_all_other_role_layers_preserved':True,")
    text = change(text, '            for role in ROLES if number==95 else (\'standalone\',):', '            for role in ROLES:')
    text = change(text, "                if number==95:node(case)['specs'][role]={'model':name,'weight':.025}\n                else:case=standalone_cfg(name)", "                node(case)['specs']['membership']={'model':name,'weight':.005}\n                node(case)['specs'][role]={'model':name,'weight':.025}\n                node(case)['retention']=.995")
    text = change(text, "        if number==95:node(changed)['specs']['rest']={'model':ns.MODELS[0],'weight':.025}\n        else:changed=standalone_cfg(ns.MODELS[0])", "        node(changed)['specs']['membership']={'model':ns.MODELS[0],'weight':.025}\n        node(changed)['retention']=.998")
    start = text.index('    def independent():')
    end = text.index('    namespace.update(graph=graph', start)
    text = text[:start] + '''    def independent():
        ns.verify();ns.build()
        ns.execute(ns.WAVES[0],grid.initial_arms(ns))
''' + text[end:]
    text = change(text, '    install_refinement(ns,number)', '    install_joint_refinement(ns)')
    text = change(text, 'ROOT=bank.ROOT', 'import joint_goss_membership_retention_grid_20261006 as grid\n\nROOT=bank.ROOT')
    text = change(text, "        sources += [Path(path) for path in ns.read(ns.PREVIOUS/'protocol.json')['input_sha256']]", "        sources += [ROOT/'analysis/joint_goss_membership_retention_grid_20261006.py',ns.PREVIOUS/'wave371_results.json',ROOT/'analysis/joint_membership_retention_scope_20261006/verification.json']\n        sources += [Path(path) for path in ns.read(ns.PREVIOUS/'protocol.json')['input_sha256']]")
    text += '''
def install_joint_refinement(ns):
    def combinations():
        first=ns.read(ns.OUT/f'wave{ns.WAVES[0]}_results.json')
        assert first['status']=='complete'
        prior=ns.read(ns.PREVIOUS/'wave371_results.json')
        assert prior['status']=='complete'
        top_rest={}
        for role in ('top','rest'):
            candidates=[r for r in prior['results'].values() if ns.previous.node(r)['specs'][role]['weight']>0]
            top_rest[role]=deepcopy(ns.previous.node(ns.previous.best(candidates))['specs'][role])
        rows=list(first['results'].values())
        anchors={name:grid.local_positive_anchor(ns,rows,name) for name in ns.MODELS}
        ns.dump(ns.OUT/'combination_protocol.json',{'model_local_positive_membership_anchors':anchors,'top_rest_from_completed_R95_wave371':top_rest},immutable=True)
        ns.execute(ns.WAVES[1],grid.combination_arms(ns,rows,top_rest))
    def refinement():
        rows=[]
        for wave in ns.WAVES[:2]:
            payload=ns.read(ns.OUT/f'wave{wave}_results.json');assert payload['status']=='complete'
            rows.extend(payload['results'].values())
        anchors={name:grid.local_positive_anchor(ns,rows,name) for name in ns.MODELS}
        ns.dump(ns.OUT/'refinement_protocol.json',{'model_local_positive_membership_anchors':anchors,'retentions':grid.FINAL_RETENTIONS,'additional_deltas':grid.DELTAS},immutable=True)
        ns.execute(ns.WAVES[2],grid.final_arms(ns,rows))
    ns.__dict__.update(combinations=combinations,refinement=refinement)
'''
    write('joint_goss_membership_search_engine_v1_20261006.py', text)

    release = (A/'ready_goss_reference_release_engine_v2_20261006.py').read_text(encoding='utf-8')
    release = release.replace("f'optimize_training_round{number}_v3'", "f'optimize_training_round{number}_v1'").replace("f'analysis/finalize_training_round{number}_v3.py'", "f'analysis/finalize_training_round{number}_v1.py'")
    release = change(release, 'def install(number,namespace):', 'def install(number,namespace):\n    assert number == 97')
    write('joint_goss_membership_release_engine_v1_20261006.py', release)

    driver = (A/'run_ready_goss_reference_round_v2_20261006.py').read_text(encoding='utf-8')
    driver = change(driver, '    assert number in (95, 96)', '    assert number == 97')
    driver = change(driver, '    parent_number = 84 if number == 95 else 95', '    parent_number = 95')
    driver = driver.replace('waiting_for_qualified_R84_R95_and_actual30_annual6_final300tree_GOSS_controls', 'waiting_for_qualified_R95_and_joint_generator_and_actual_GOSS_controls')
    driver = driver.replace('ready_goss_reference_generator_preflight_v2_20261006', 'joint_goss_membership_generator_preflight_v1_20261006')
    driver = driver.replace('ready_goss_reference_quality_run_v2_20261006.json', 'joint_goss_membership_quality_run_v1_20261006.json')
    driver = driver.replace("f'optimize_training_round{number}_v3'", "f'optimize_training_round{number}_v1'").replace("f'finalize_training_round{number}_v3'", "f'finalize_training_round{number}_v1'")
    driver = driver.replace('predict_ready_goss_reference_scheme_v2_20261006', 'predict_joint_goss_membership_scheme_v1_20261006')
    driver = driver.replace('check_ready_goss_reference_scheme_v2_20261006', 'check_joint_goss_membership_scheme_v1_20261006')
    driver = change(driver, '        stages = (module.freeze, module.build, module.independent,\n            *((module.combinations, module.refine_weights) if number == 95 else (module.model_refinement,)), module.refinement)', '        stages = (module.freeze, module.build, module.independent, module.combinations, module.refinement)')
    driver = change(driver, "        labels = ('GOSS三种用途对照', '最佳用途组合', '用途权重细搜', '留存与涨停偏移细搜') if number == 95 else ('独立完整主模型', '逐模型参数与留存细搜', '实际最高分方案细搜')", "        labels = ('非零成员权重与高留存率联合搜索', '逐模型正权重起点及用途组合', '逐模型更高留存率及涨停偏移细搜')")
    driver = driver.replace('gradient_sampling_reference_causal_checks.json', 'gradient_sampling_joint_membership_causal_checks.json').replace('成熟原始特征GOSS完整方案', 'GOSS非零成员权重与高留存率联合完整方案')
    write('run_joint_goss_membership_round_v1_20261006.py', driver)

    checks = (A/'check_ready_goss_reference_scheme_v2_20261006.py').read_text(encoding='utf-8')
    checks = change(checks, 'def main(number):', 'def main(number):\n    assert number == 97')
    checks = change(checks, "        for role in module.ROLES if number == 95 else ('standalone',):", '        for role in module.ROLES:')
    checks = change(checks, "            if number == 95:\n                module.node(cfg)['specs'][role] = {'model': name, 'weight': .025}\n            else:\n                cfg = module.standalone_cfg(name)", "            module.node(cfg)['specs']['membership'] = {'model': name, 'weight': .005}\n            module.node(cfg)['specs'][role] = {'model': name, 'weight': .025}\n            module.node(cfg)['retention'] = .998")
    checks = checks.replace('gradient_sampling_reference_causal_checks.json', 'gradient_sampling_joint_membership_causal_checks.json')
    write('check_joint_goss_membership_scheme_v1_20261006.py', checks)

    predictor = '''"""Copy round97 and all effective parent codecs before and after shared prediction."""
from pathlib import Path
import shutil
from predict_ready_goss_reference_scheme_v2_20261006 import source_names as previous_sources

def source_names(number):
    assert number == 97
    return tuple(dict.fromkeys((*previous_sources(96),
        'joint_goss_membership_retention_grid_20261006.py',
        'joint_goss_membership_search_engine_v1_20261006.py',
        'joint_goss_membership_release_engine_v1_20261006.py',
        'run_joint_goss_membership_round_v1_20261006.py',
        'check_joint_goss_membership_scheme_v1_20261006.py',
        'predict_joint_goss_membership_scheme_v1_20261006.py',
        'optimize_training_round97_v1.py','finalize_training_round97_v1.py',
        'run_training_round97_v1_pipeline.py')))

def copy_sources(ns,candidate):
    candidate=Path(candidate)
    assert not (candidate/'manifest.json').exists(),'A sealed candidate must not be edited.'
    candidate.mkdir(parents=True,exist_ok=True)
    for name in source_names(ns.NUMBER):
        shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name)
        for suffix in ('_v1.py','_v2.py','_v3.py'):
            if name.startswith(('optimize_training_round','finalize_training_round')) and name.endswith(suffix):
                shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name[:-len(suffix)]+'.py')

def predict(ns,record,candidate_path=None,mapping_path=None):
    from predict_gradient_sampling_scheme_codec_20261005 import predict as original
    candidate=Path(candidate_path) if candidate_path is not None else ns.ROOT/f'candidates/optimization_20261003_r{ns.NUMBER}'
    copy_sources(ns,candidate)
    original(ns,record,candidate_path=candidate,mapping_path=mapping_path)
    copy_sources(ns,candidate)
'''
    write('predict_joint_goss_membership_scheme_v1_20261006.py', predictor)
    write('optimize_training_round97_v1.py', 'import sys\nimport optimize_training_round95_v3\nfrom joint_goss_membership_search_engine_v1_20261006 import install\ninstall(97,globals())\nsys.modules["optimize_training_round97"]=sys.modules[__name__]\n')
    write('finalize_training_round97_v1.py', 'from joint_goss_membership_release_engine_v1_20261006 import install\ninstall(97,globals())\n')
    write('run_training_round97_v1_pipeline.py', 'from run_joint_goss_membership_round_v1_20261006 import main\nif __name__=="__main__":main(97)\n')
    write('optimize_training_round97.py', 'from optimize_training_round97_v1 import *\n')
    write('finalize_training_round97.py', 'from finalize_training_round97_v1 import *\n')
    write('run_training_round97_pipeline.py', 'from run_joint_goss_membership_round_v1_20261006 import main\nif __name__=="__main__":main(97)\n')
    print('Created isolated round97 engine, grid driver, release, causal checks and candidate source codec.', flush=True)

if __name__ == '__main__':
    main()

"""Copy immutable four-model complete-scheme adapters into the R61/R62 namespace."""
from pathlib import Path
import ast
import hashlib
import json
import re
import time
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def translate(text):
    text=text.replace('portfolio_surrogate','nystrom_ridge')
    text=text.replace('round59','round61').replace('round60','round62')
    text=re.sub(r'\b59\b','61',text);text=re.sub(r'\b60\b','62',text)
    text=text.replace('round58 as parent','round60 as parent')
    for old,new in zip(range(247,254),range(254,261)):text=text.replace(str(old),str(new))
    text=text.replace('neural_width_standalone_scheme_graph','portfolio_surrogate_standalone_scheme_graph') if 'def baseline():' in text else text
    text=text.replace('成熟训练收益、持仓重合度与平滑温度损失微调模型','成熟过去样本Nyström核近似岭回归模型')
    return text

def main():
    proof=HERE/'nystrom_ridge_preflight_20261004/verification.json'
    assert json.loads(proof.read_text(encoding='utf-8'))['status']=='passed'
    templates=('model_sources','scheme_runtime','search_engine','release_engine')
    pairs=[(f'portfolio_surrogate_{suffix}_20261004.py',f'nystrom_ridge_{suffix}_20261004.py') for suffix in templates]
    pairs += [(f'{verb}_portfolio_surrogate_scheme_20261004.py',f'{verb}_nystrom_ridge_scheme_20261004.py') for verb in ('predict','check')]
    pairs += [('run_portfolio_surrogate_round_pipeline_20261004.py','run_nystrom_ridge_round_pipeline_20261004.py'),
        ('verify_neural_width_future_models_20261004.py','verify_nystrom_ridge_future_models_20261004.py'),
        ('verify_portfolio_surrogate_search_generators_20261004.py','verify_nystrom_ridge_search_generators_20261004.py'),
        ('verify_portfolio_surrogate_complete_scheme_20261004.py','verify_nystrom_ridge_complete_scheme_20261004.py'),
        ('freeze_portfolio_surrogate_search_plan_20261004.py','freeze_nystrom_ridge_search_plan_20261004.py')]
    pairs += [(f'{prefix}_round{old}{suffix}',f'{prefix}_round{new}{suffix}')
        for prefix,suffix in (('optimize_training','.py'),('finalize_training','.py'),('run_training','_pipeline.py'))
        for old,new in ((59,61),(60,62))]
    original={str((HERE/old).resolve()):sha(HERE/old) for old,new in pairs};new_sources={}
    for old,new in pairs:
        source=HERE/old;target=HERE/new;assert not target.exists(),target
        text=translate(source.read_text(encoding='utf-8-sig'))
        if old=='verify_neural_width_future_models_20261004.py':
            text=text.replace('neural_width','nystrom_ridge')
            text=text.replace('12*2**30','14*2**30').replace("'minimum_available_ram_before_fullfit_GiB':12.","'minimum_available_ram_before_fullfit_GiB':14.")
            text=text.replace('Future matched width model checked','Future Nyström model checked')
            text=text.replace('matched neural width','Nyström kernel')
        if new=='nystrom_ridge_model_sources_20261004.py':
            text=text.replace('import neural_width_model_sources_20261004 as previous','import portfolio_surrogate_model_sources_20261004 as previous')
            before='def predict_arrays(bundle,x,dates=None,valid=None):return previous.predict_arrays(bundle,x,dates=dates,valid=valid)'
            after="def predict_arrays(bundle,x,dates=None,valid=None):\n    if bundle['kind']=='ridge_nystrom':return native.predict_arrays(bundle,x)\n    return previous.predict_arrays(bundle,x,dates=dates,valid=valid)"
            assert before in text;text=text.replace(before,after)
        if new in ('verify_nystrom_ridge_search_generators_20261004.py','verify_nystrom_ridge_complete_scheme_20261004.py'):
            indent='    ' if 'complete_scheme' in new else ''
            anchor=indent+'from neural_width_scheme_runtime_20261004 import append_role_layer as preceding_width_layer'
            assert anchor in text
            text=text.replace(anchor,anchor+'\n'+indent+'from portfolio_surrogate_scheme_runtime_20261004 import append_role_layer as preceding_portfolio_layer')
            anchor="    base['neural_width_standalone_scheme_graph']=deepcopy(base['neural_width_role_scheme_graph'])"
            assert anchor in text
            text=text.replace(anchor,anchor+"\n    base['portfolio_surrogate_role_scheme_graph']=preceding_portfolio_layer(base['neural_width_standalone_scheme_graph'])\n    base['portfolio_surrogate_standalone_scheme_graph']=deepcopy(base['portfolio_surrogate_role_scheme_graph'])")
            text=text.replace("'nystrom_ridge_role_scheme_graph':append_role_layer(base['neural_width_standalone_scheme_graph'])","'nystrom_ridge_role_scheme_graph':append_role_layer(base['portfolio_surrogate_standalone_scheme_graph'])")
            text=text.replace("==base['neural_width_standalone_scheme_graph']['layers']","==base['portfolio_surrogate_standalone_scheme_graph']['layers']")
        if new=='freeze_nystrom_ridge_search_plan_20261004.py':
            text=text.replace("'61':58,'62':61","'61':60,'62':61")
            text=text.replace("ROOT/'analysis/portfolio_bank_implementation_preflight_20261004/verification.json'","ROOT/'analysis/nystrom_ridge_preflight_20261004/verification.json'")
            text=text.replace("'warm_start_old_checkpoint_fits_reused_not_counted_as_new':True","'landmark_basis_fitted_only_on_matching_mature_past_fold':True")
            text=text.replace('Portfolio-loss complete100/98-record plans frozen','Nyström complete100/98-record plans frozen')
        text=text.replace('portfolio-loss fine-tuning models','Nyström kernel ridge models')
        text=text.replace('mature portfolio-loss fine-tuning extensions','past-sampled Nyström kernel extensions')
        ast.parse(text,filename=new);target.write_text(text,encoding='utf-8',newline='\n')
        new_sources[str(target.resolve())]=sha(target)
    for path,digest in original.items():assert sha(Path(path))==digest,path
    record={'status':'isolated_sources_generated_pending_actual_generator_andcomplete_scheme_checks',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'source_sha256':new_sources,
        'copied_from_unchanged_source_sha256':original,'planned_rounds':[61,62],
        'waves':{'61':[254,255,256,257],'62':[258,259,260]},
        'expected_total_records':{'61':100,'62':98},'new_quality_scores':0,'test_labels_read':False}
    with (HERE/'nystrom_ridge_adapter_generation_20261004.json').open('x',encoding='utf-8') as stream:json.dump(record,stream,ensure_ascii=False,indent=2)
    print('Seventeen isolated Nyström adapters generated; original frozen sources unchanged',flush=True)

if __name__=='__main__':main()

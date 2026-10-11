"""Prepare release/check/pipeline files without changing any frozen parent."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]


def main():
    source=(ROOT/'analysis/finalize_training_round29.py').read_text(encoding='utf-8')
    text=source.replace('Round29','Round30').replace('round29','round30').replace('_r29','_r30').replace('_r28','_r29')
    start=text.index("    paths=[Path(__file__)");end=text.index("    paths.extend(Path(row['official_score_cache']",start)
    text=text[:start]+"""    paths=[Path(__file__),OUT/'protocol.json',OUT/'component_audit.json',
           *[OUT/f'wave{wave}_results.json' for wave in WAVES],
           *sorted(OUT.glob('coordinate_*_protocol.json')),*sorted(OUT.glob('output_*_protocol.json')),
           OUT/'selected_validation.npy',OUT/'promote_baseline.npy',PREVIOUS/'selection.json',
           ROOT/'active_release.json',FORMAL/'generation_inputs.parquet',
           ROOT/'candidates/optimization_20261003_r29/verification.json']
"""+text[end:]
    text=text.replace('from predict_final_roles_round30 import predict as generate','from predict_complete_scheme_round30 import predict as generate')
    files={'finalize_training_round30.py':text,
      'verify_methods_round30.py':'''"""Verify selected recomputation, poisoned labels and freshly computed prefixes."""
import numpy as np
from optimize_training_round30 import OUT,prefix_controls,dump,log
from finalize_training_round30 import ReleaseContext,selected

def main():
    winner=selected()['winner'];ctx=ReleaseContext(winner)
    promote=ctx.finished('baseline');pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    controls=prefix_controls(ctx,winner)
    dump(OUT/'complete_scheme_causal_checks.json',{'status':'passed','selected_output_bit_identical':True,
         'controls':controls,'new_model_training':False,'test_data_read':False,'new_scored_records':0},immutable=True)
    log('Round30 complete reconstruction, poisoned labels and cold prefixes passed')

if __name__=='__main__':main()
'''}
    pipeline=(ROOT/'analysis/run_training_round29_pipeline.py').read_text(encoding='utf-8')
    pipeline=pipeline.replace('round29','round30').replace('_r29','_r30').replace('_r28','_r29')
    pipeline=pipeline.replace("'round':29","'round':30").replace('publish(29,','publish(30,')
    pipeline=pipeline.replace("optimization_20261003_r29/standalone_causal_checks.json","optimization_20261003_r29/linear_role_causal_checks.json")
    pipeline=pipeline.replace("ROOT/'analysis/linear_bank_20261003/oof_audit.json'","ROOT/'analysis/complete_scheme_replay_20261003/oof_audit.json'")
    pipeline=pipeline.replace('experiment.combinations,experiment.refine_weights','experiment.coordinate')
    pipeline=pipeline.replace("'linear_role_causal_checks.json'","'complete_scheme_causal_checks.json'")
    pipeline=pipeline.replace('未来一日线性信号的完整输出增量集成','完整方案各层模型权重与后处理联合复搜')
    pipeline=pipeline.replace("('6种线性信号独立用途比较','用途最优设置组合','权重细搜','涨停股输出偏移细调')", "('各层有效权重独立比较','完整重新计算的坐标细搜','完整输出参数细调')")
    files['run_training_round30_pipeline.py']=pipeline
    for filename,text in files.items():
        target=ROOT/'analysis'/filename;assert not target.exists();ast.parse(text,filename=str(target))
        target.write_text(text,encoding='utf-8',newline='\n');print(target)


if __name__=='__main__':main()

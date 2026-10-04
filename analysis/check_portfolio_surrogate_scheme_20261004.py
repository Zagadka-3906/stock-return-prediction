"""Selected full-vector equality andfresh typed role/standalone prefix controls."""
from copy import deepcopy
from pathlib import Path
import importlib


def main(number):
    import numpy as np
    module=importlib.import_module(f'optimize_training_round{number}')
    release=importlib.import_module(f'finalize_training_round{number}')
    winner=release.selected()['winner'];ctx=release.ReleaseContext(winner)
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
    assert np.array_equal(pred,np.load(module.OUT/'selected_validation.npy'))
    cases=[winner,module.baseline()]
    if number==59:
        for role in module.ROLES:
            cfg=deepcopy(module.baseline());module.node(cfg)['specs'][role]={'model':module.MODELS[0],'weight':.025};cases.append(cfg)
    else:
        for name in module.MODELS:cases.append(module.standalone_cfg(name))
    controls=[module.prefix_controls(ctx,cfg) for cfg in cases]
    module.dump(module.OUT/'portfolio_surrogate_scheme_causal_checks.json',{'status':'passed','selected_output_bit_identical':True,
        'actual_complete_output_cold_prefix_andlabel_poisoning_controls':controls,
        'explicit_graph_parameter_authority':module.GRAPH_FIELD,'new_scored_records':0,
        'new_model_training':False,'test_labels_read':False,'verification_script_sha256':module.sha(Path(__file__))},immutable=True)

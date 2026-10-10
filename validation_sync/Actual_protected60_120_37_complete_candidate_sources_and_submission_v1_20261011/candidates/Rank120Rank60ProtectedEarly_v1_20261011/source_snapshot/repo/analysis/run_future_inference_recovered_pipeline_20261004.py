"""Bind corrected future-only constants before prospective round freeze/scoring."""
from pathlib import Path
import importlib.util
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def install(stem,number):
    name=f'{stem}{number}';path=ROOT/f'analysis/{name}_future_recovery_20261004.py'
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module;spec.loader.exec_module(module)
    return module


def main(number):
    assert number in (36,38,40)
    pipeline=__import__(f'run_training_round{number}_pipeline')
    experiment=__import__(f'optimize_training_round{number}')
    original_freeze=experiment.freeze
    def recovered_freeze():
        proof=ROOT/'analysis/future_inference_recovery_20261004/verification.json'
        assert experiment.read(proof)['status']=='passed'
        audit=experiment.read(proof)
        for path,digest in audit['source_sha256'].items():assert experiment.sha(path)==digest,path
        paths=[Path(__file__),proof,ROOT/'analysis/future_inference_recovery_sources_20261004.json',
               ROOT/f'analysis/predict_standalone_round{number}_future_recovery_20261004.py',
               ROOT/f'analysis/finalize_training_round{number}_future_recovery_20261004.py']
        original_dump=experiment.dump
        def amended_dump(path,payload,*args,**kwargs):
            if Path(path)==experiment.OUT/'protocol.json':
                payload={**payload,'input_sha256':{**payload['input_sha256'],**{str(p.resolve()):experiment.sha(p) for p in paths}},
                    'future_inference_execution_recovery':{'actual_helper':str(paths[3].resolve()),'actual_finalizer':str(paths[4].resolve()),
                        'entrypoint':str(Path(__file__).resolve()),'proof':str(proof.resolve()),
                        'scope':'Correct wrong generated immutable delivery path/row assertion only. Forecast/scoring algorithms unchanged.',
                        'bound_before_any_round_scoring':True,'original_sources_retained_as_templates':True}}
            return original_dump(path,payload,*args,**kwargs)
        experiment.dump=amended_dump
        try:original_freeze()
        finally:experiment.dump=original_dump
        installed_helper=install('predict_standalone_round',number)
        installed_finalizer=install('finalize_training_round',number)
        assert Path(installed_finalizer.FORMAL)==ROOT/'deliveries/connected_topk0175_20261003'
        assert Path(installed_helper.__file__).resolve()==paths[3].resolve()
    experiment.freeze=recovered_freeze
    pipeline.main()


if __name__=='__main__':main(int(sys.argv[1]))

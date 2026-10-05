"""Retain the failed new generator and repair all embedded wave file references."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'


def create(path,text):
    if path.suffix=='.py':compile(text,str(path),'exec')
    with path.open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)


def main():
    proof=A/'reference66_linear_leaf_generator_preflight_20261005/frozen_before_generator_controls.json'
    original=json.loads(proof.read_text(encoding='utf-8'))
    for path,digest in original['source_sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    assert not (proof.parent/'verification.json').exists()
    retained=A/'reference66_linear_leaf_recovery_v2_20261005'
    retained.mkdir()
    create(retained/'original_failure_retained.json',json.dumps({'status':'original_frozen_generator_failure_retained',
        'frozen_before_controls_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
        'source_sha256':original['source_sha256'],
        'failure':'Old wave283 string path survived numeric-token remapping; no new official scores or fits.',
        'original_qualified_R66_and_original_rounds67_through80_untouched':True,'new_quality_scores':0},ensure_ascii=False,indent=2))
    stems=['linear_leaf_reference66_search_engine','explicit_parent_release_engine',
        'publish_explicit_parent_training_round','check_reference66_linear_leaf_scheme',
        'run_reference66_linear_leaf_round','predict_reference66_linear_leaf_scheme',
        'verify_reference66_linear_leaf_generators']
    replace={f'{stem}_20261005':f'{stem}_v2_20261005' for stem in stems}
    replace['reference66_linear_leaf_generator_preflight_20261005']='reference66_linear_leaf_generator_preflight_v2_20261005'
    for stem in stems:
        name=f'{stem}_20261005.py'
        text=(A/name).read_text(encoding='utf-8')
        for old,new in replace.items():text=text.replace(old,new)
        text=text.replace('optimize_training_round{number}.py','optimize_training_round{number}_v2.py')
        text=text.replace('finalize_training_round{number}.py','finalize_training_round{number}_v2.py')
        text=text.replace('run_training_round{number}_pipeline.py','run_training_round{number}_v2_pipeline.py')
        if stem=='linear_leaf_reference66_search_engine':
            for old in range(283,290):text=text.replace(f'wave{old}_',f'wave{old+42}_')
        if stem=='explicit_parent_release_engine':
            text=text.replace("f'optimize_training_round{number}'","f'optimize_training_round{number}_v2'")
        if stem=='run_reference66_linear_leaf_round':
            text=text.replace("f'optimize_training_round{number}'","f'optimize_training_round{number}_v2'",1)
            text=text.replace("f'finalize_training_round{number}'","f'finalize_training_round{number}_v2'")
            text=text.replace("release = importlib.import_module(f'finalize_training_round{number}_v2')",
                "release = importlib.import_module(f'finalize_training_round{number}_v2')\n    sys.modules[f'finalize_training_round{number}'] = release")
        if stem=='verify_reference66_linear_leaf_generators':
            text=text.replace("f'optimize_training_round{number}'","f'optimize_training_round{number}_v2'")
            text=text.replace("('optimize_training_round', '')","('optimize_training_round', '_v2')")
            text=text.replace("('finalize_training_round', '')","('finalize_training_round', '_v2')")
            text=text.replace("('run_training_round', '_pipeline')","('run_training_round', '_v2_pipeline')")
        if stem=='predict_reference66_linear_leaf_scheme':
            text=text.replace("'optimize_training_round81.py','finalize_training_round81.py'",
                "'optimize_training_round81_v2.py','finalize_training_round81_v2.py'")
            text=text.replace("shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name)",
                "shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name)\n        if name.startswith(('optimize_training_round','finalize_training_round')) and name.endswith('_v2.py'):\n            shutil.copyfile(ns.ROOT/'analysis'/name,candidate/name.replace('_v2.py','.py'))")
        create(A/(replace[f'{stem}_20261005']+'.py'),text)
    for number in (81,82):
        import_previous='import optimize_training_round81_v2\n' if number==82 else ''
        create(A/f'optimize_training_round{number}_v2.py',import_previous+
            f'import sys\nfrom linear_leaf_reference66_search_engine_v2_20261005 import install\ninstall({number},globals())\nsys.modules["optimize_training_round{number}"]=sys.modules[__name__]\n')
        create(A/f'finalize_training_round{number}_v2.py',
            f'from explicit_parent_release_engine_v2_20261005 import install\ninstall({number},globals())\n')
        create(A/f'run_training_round{number}_v2_pipeline.py',
            f'from run_reference66_linear_leaf_round_v2_20261005 import main\nif __name__=="__main__":main({number})\n')
    print(json.dumps({'status':'retained_original_generator_failure_and_created_V2','new_quality_scores':0}))


if __name__=='__main__':main()

"""Create complete-layer inference from the verified legacy inference primitives."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]


def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new)


def main():
    source=(ROOT/'analysis/finalize_training_round22.py').read_text(encoding='utf-8')
    start=source.index('def predict():');end=source.index('\n\ndef main():',start)
    text=source[start:end]
    text=text.replace('def predict():','def predict(record,candidate_path=None):')
    text=once(text,"    record=selected();winner=record['winner']", "    from optimize_training_round30 import ROOT,OUT,PREVIOUS,FORMAL,Context,KEYS,BASE_POST,HERE,ARCHIVE,read,dump,sha,log\n    CANDIDATE=Path(candidate_path) if candidate_path is not None else ROOT/'candidates/optimization_20261003_r30'\n    winner=record['winner']")
    # FORMAL is introduced below in the optimizer before the inference module is used.
    text=text.replace('neural_ensemble_model_sources_20261003','linear_model_sources_20261003')
    text=once(text,"    used=sorted({spec['model'] for group in ('diverse_augmentation','secondary_augmentation') for spec in winner[group].values() if spec['weight']>0})",
        "    groups=('diverse_augmentation','secondary_augmentation','final_augmentation','linear_augmentation')\n    used={spec['model'] for group in groups for spec in winner[group].values() if spec['weight']>0}\n    if winner.get('standalone'):used.add(winner['standalone']['model'])\n    used=sorted(used)\n    import build_market_regime_bank_20261003 as regime\n    regime_maps=regime.future_mapping() if any(spec.get('regime') for spec in winner['final_augmentation'].values()) else None")
    text=once(text,"    previous_models=read(ROOT/'candidates/optimization_20261003_r21/verification.json')['models']", "    previous_models=read(ROOT/f'candidates/{PREVIOUS.name}/verification.json')['models']")
    first=text.index("    for component in winner['recipe']['components']:");last=text.index("    source_paths=",first)
    block=text[first:last]
    text=text[:first]+"    if not winner.get('standalone'):\n"+''.join('    '+line if line.strip() else line for line in block.splitlines(keepends=True))+text[last:]
    text=once(text,"    ctx.diverse_augmentation=winner['diverse_augmentation'];ctx.secondary_augmentation=winner['secondary_augmentation'];ctx._diverse_cache={}",
        "    ctx.diverse_augmentation=winner['diverse_augmentation'];ctx.secondary_augmentation=winner['secondary_augmentation'];ctx._diverse_cache={}\n    ctx.standalone=winner.get('standalone');ctx.final_augmentation=winner['final_augmentation'];ctx.final_limit_delta=winner['final_limit_delta']\n    ctx.linear_augmentation=winner['linear_augmentation'];ctx.linear_limit_delta=winner['linear_limit_delta'];ctx._final_cache={}\n    ctx._regime_cache=regime.future_values(regime_maps,test.with_columns(pl.Series('price_valid',valid))) if regime_maps else {}\n    raw_new={}")
    # RVOL20 and RET1 are already among the frozen63 feature columns.
    text=once(text,"        ctx._diverse_cache[name]=(values,daily_ranks(values,valid,dates))", "        ctx._diverse_cache[name]=(values,daily_ranks(values,valid,dates))\n        ctx._final_cache[name]=daily_ranks(new_raw,valid,dates);raw_new[name]=new_raw")
    text=once(text,"        mixed=sum(c['weight']*daily_ranks(raw,valid,dates) for c,raw in topk_raw);mixed[~valid]=-10.\n        promote=process(mixed,winner['recipe']['postprocessing'])",
        "        if ctx.standalone:promote=process(raw_new[ctx.standalone['model']],ctx.standalone['postprocessing'])\n        else:\n            mixed=sum(c['weight']*daily_ranks(raw,valid,dates) for c,raw in topk_raw);mixed[~valid]=-10.\n            promote=process(mixed,winner['recipe']['postprocessing'])")
    text=text.replace("'diverse_augmentation':winner['diverse_augmentation'],'secondary_augmentation':winner['secondary_augmentation'],'new_fulltrain_models':len(used)",
        "'diverse_augmentation':winner['diverse_augmentation'],'secondary_augmentation':winner['secondary_augmentation'],'final_augmentation':winner['final_augmentation'],'linear_augmentation':winner['linear_augmentation'],'new_fulltrain_models':len(used)")
    text=text.replace('Round22 candidate','Round30 complete-scheme candidate')
    text="\"\"\"Replay every layer after freezing the complete validation-selected configuration.\"\"\"\nfrom pathlib import Path\n\n\n"+text+'\n'
    ast.parse(text);target=ROOT/'analysis/predict_complete_scheme_round30.py';assert not target.exists()
    target.write_text(text,encoding='utf-8',newline='\n');print(target)


if __name__=='__main__':main()

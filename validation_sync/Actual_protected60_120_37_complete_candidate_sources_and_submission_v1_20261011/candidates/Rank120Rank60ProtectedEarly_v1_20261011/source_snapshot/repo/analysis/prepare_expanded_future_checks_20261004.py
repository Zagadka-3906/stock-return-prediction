"""Adapt the verified complete future-branch diagnostic to the55-child bank."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis'


def main():
    text=(HERE/'verify_stacking_future_pipelines_20261004.py').read_text(encoding='utf-8')
    text=text.replace('stacking_fulltraining_warmup_20261004','expanded_stacking_fulltraining_warmup_20261004')
    text=text.replace('stacking_model_sources_20261004','expanded_stacking_model_sources_20261004')
    text=text.replace('round33','round39').replace('round34','round40')
    text=text.replace('stacking_future_pipelines_qa_20261004','expanded_stacking_future_pipelines_qa_20261004')
    text=text.replace('optimization_20261003_r22','optimization_20261003_r24')
    text=text.replace('stacking_augmentation','expanded_stacking_augmentation').replace('stacking_limit_delta','expanded_stacking_limit_delta')
    text=text.replace("models.bank.OUT/'input_routing_recovery_protocol.json'","models.bank.OUT/'protocol.json'")
    text=text.replace('==45','==55').replace("'embedded_children':45","'embedded_children':55").replace('portable45-child','portable55-child')
    text=text.replace('model selection','scheme selection')
    marker="    # Load the copied, embedded bundle directly; no annual child path is available to it."
    assert marker in text
    text=text.replace(marker,"    # Paired first-year policies reuse identical full-training coefficients and child bundles.\n    alias=models.read(gate)['paired_uniform_model']\n    paired=models.train_one(alias,2025);assert paired['new_model_fits']==0\n"+marker)
    marker="    assert np.array_equal(embedded,original_pred)"
    assert marker in text
    text=text.replace(marker,marker+"\n    alias_pred=models.predict_arrays(models.load_bundle(models.model_path(alias,2025)),x,dates=dates,valid=valid)\n    assert np.array_equal(original_pred,alias_pred)")
    text=text.replace("'portable_bundle_without_child_paths_replay_bit_identical':True,","'portable_bundle_without_child_paths_replay_bit_identical':True,'paired_full_training_inference_bit_identical':True,")
    path=HERE/'verify_expanded_stacking_future_pipelines_20261004.py';ast.parse(text,filename=str(path))
    if path.exists():assert path.read_text(encoding='utf-8')==text
    else:path.write_text(text,encoding='utf-8',newline='\n')
    print('Expanded future diagnostic source prepared.')


if __name__=='__main__':main()

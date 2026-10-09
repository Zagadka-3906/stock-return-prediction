"""Preserve five complete parent backend bindings and prepare the151 RFFSparse prediction ABI."""
from pathlib import Path
import sys,time,importlib.util
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def module(path,name):
    specification=importlib.util.spec_from_file_location(name,path);value=importlib.util.module_from_spec(specification);specification.loader.exec_module(value);return value

def main():
    original=A/'predict_HuberSparse_complete_parent_scheme_v1_20261008.py';source=original.read_text(encoding='utf8')
    corrected=source.replace('HuberSparse_complete_parent_native_stage_v1_20261008','RFFSparse_complete_parent_native_stage_v3_20261009').replace('HuberSparse','RFFSparse')
    destination=save('predict_RFFSparse_complete_parent_scheme_v1_20261009.py',corrected)
    before=module(original,'original150_parent_backends_for151');after=module(destination,'new151_parent_backends')
    assert before.BACKENDS==after.BACKENDS and len(after.BACKENDS)==5
    for name in after.BACKENDS:
        assert after.prepared_backend((A/after.BACKENDS[name][0]).read_text(encoding='utf8'),name).count('HUBER_CROSS_AFTER_COMPLETE_PARENT')==1
    from RFFSparse_complete_parent_native_stage_v3_20261009 import GRAPH_KEY
    assert GRAPH_KEY=='nonflag_CPU_RFFSparse_complete_parent_CDF'
    plan=read(A/'RFFSparse59_round151_proposal_v1_20261009.json');assert len(plan['heads'])==4 and plan['fixed_scientific_stage_base_round']==134
    sources=[Path(__file__),original,destination,A/'RFFSparse_complete_parent_CDF_v3_20261009.py',A/'RFFSparse_complete_parent_native_stage_v3_20261009.py',
        A/'RFFSparse59_round151_proposal_v1_20261009.json',*[A/row[0] for row in after.BACKENDS.values()],
        A/'nonflag_sparse_Gram64_codec_20261007.py',A/'nonflag_residual_RFF128_codec_20261007.py',A/'nonflag_residual_HGB_preprocessing_20261007.py']
    create(A/'RFFSparse151_complete_native_predictor_preparation_v1_20261009.json',{'status':'prepared_RFFSparse151_native_predictor_five_original_complete_parent_backend_bindings_exact',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},'parent_backends':after.BACKENDS,
        'new_graph_key':GRAPH_KEY,'new_saved_residual_families':['random_fourier_linear','SparseGram64_linear'],
        'must_take_native_stage_kind_separately_from_independent_state_storage_kind':True,'actual_future_features_read':False,'new_future_native_replays':0,
        'new_native_fits':0,'full_candidate_graph_freeze_and_two1599600_replays_still_required':True,'test_labels_read':False})
    print({'prepared_predictor':destination.name,'parent_backends_preserved':5,'new_future_inference':0},flush=True)
if __name__=='__main__':main()

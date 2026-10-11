"""Predeclare a genuinely fresh wider H60 bank; serialize GPU work behind existing fits."""
from pathlib import Path
import ast, sys, importlib
A=Path(__file__).resolve().parent
sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def changed(s):
    s=s.replace('stock_rank60','stock_rank60medium').replace('StockRank60','StockRank60Medium')
    s=s.replace('small512','medium2048').replace('Small512','Medium2048')
    s=s.replace('[512, 256, 128]','[2048, 1024, 512]')
    # Label/calendar population and already verified maturity fixture remain identical.
    s=s.replace('recent252_rank60medium','recent252_rank60')
    s=s.replace('actual_stock_rank60medium_embedding_mature_fixture_location','actual_stock_rank60_embedding_mature_fixture_location')
    return s

def main():
    assert allowed()
    files=[
      'stock_rank60_embedding_small512_BF16_native_v1_20261011.py',
      'stock_rank60_embedding_saved_tensor_decoder_v1_20261011.py',
      'verify_stock_rank60_embedding_small512_restart_v1_20261011.py',
      'verify_stock_rank60_embedding_small512_small_CPU_v1_20261011.py',
      'train_stock_rank60_embedding_small512_BF16_bank6_own64_v1_20261011.py',
      'verify_stock_rank60_embedding_small512_full5_independent_v1_20261011.py',
      'stock_rank60_embedding_after_complete_qualified_parent_native_stage_v1_20261011.py',
      'stock_rank60_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py',
      'verify_stock_rank60_embedding_six_state_native42_v1_20261011.py',
      'predict_stock_rank60_embedding_complete_qualified_parent_scheme_v2_20261011.py',
      'verify_stock_rank60_actual_twelve_parent183_callbacks_CPU_v2_20261011.py',
      'run_stock_rank60_embedding_after183_direct_allocation33_v1_20261011.py']
    outputs=[]
    for name in files:
        p=A/name;q=A/changed(name);s=changed(p.read_text(encoding='utf8'))
        if name.startswith('run_stock_'):
            s=s.replace("    closed('actual_stock_rank60medium_embedding_after175_large_allocation29_screen_v1_20261011')", "    closed('Rank120Rank60BestBlend38Early_selected_candidate_sealing_v1_20261011')")
        ast.parse(s);assert not q.exists(),q;q.write_text(s,encoding='utf8');outputs.append(q)
    native=importlib.import_module(changed(Path(files[0]).stem))
    assert native.CONFIG['hidden']==[2048,1024,512]
    assert native.CONFIG['target']=='y_rank_60mean' and native.CONFIG['epochs']==64
    assert native.CONFIG['label_horizon_trading_days']==60 and native.CONFIG['training_calendar_window']==252
    pins={str(p):sha(p) for p in [Path(__file__),*[A/n for n in files],*outputs,
        A/'recent252_rank60_mature_population_actual_CPU_controls_v2_20261011.json',
        A/'forward60_mature_training_labels_v2_20261011.py',
        A/'actual_stock_rank60_embedding_mature_fixture_location_v1_20261011.json']}
    protocol=A/'stock_rank60medium2048_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json'
    create(protocol,{'status':'predeclared_fresh_H60_medium2048_capacity_hypothesis_before_training_or_scores',
        'configuration':native.CONFIG,'input_sha256':pins,'new_fits':0,'new_scores':0,
        'expected_annual_fits':6,'expected_official_records':33,'expected_full_controls':32,
        'expected_prefix_controls':96,'reuse_label_calendar_and_fixture_only':True,
        'reuse_512_weights':False,'test_labels_read':False,'actual_future_X_read':False,
        'GPU_serialization_after':'actual_stock_rank60window504_embedding_six_state_native42_v1_20261011'})
    for tag in ['stock_rank60_embedding_native_stage_and_fast17_sources_admission_v1_20261011.json',
                'stock_rank60_after183_direct33_predeclared_sources_v1_20261011.json']:
        create(A/changed(tag),{'status':'predeclared_new_medium2048_sources_no_actual_fit_claim',
                             'input_sha256':pins,'configuration':native.CONFIG,'new_fits':0,'new_scores':0})
    jobs=[('actual_stock_rank60medium_embedding_medium2048_restart_v1_20261011',outputs[2].name),
          ('StockRank60MediumEmbeddingMedium2048_independent_small_CPU_v1_20261011',outputs[3].name),
          ('actual_stock_rank60medium_embedding_medium2048_bank6_v1_20261011',outputs[4].name),
          ('StockRank60MediumEmbeddingMedium2048_independent_full5_GPU_controls_v1_20261011',outputs[5].name),
          ('actual_stock_rank60medium_embedding_six_state_native42_v1_20261011',outputs[8].name),
          ('actual_stock_rank60medium_embedding_after183_direct_allocation33_v1_20261011',outputs[11].name)]
    queue=A/'run_rank60medium2048_own6_native42_direct33_queue_v1_20261011.py'
    source="""from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 closed('actual_stock_rank60window504_embedding_six_state_native42_v1_20261011')
 closed('Rank120Rank60BestBlend38Early_selected_candidate_sealing_v1_20261011')
 for name,driver in JOBS:
  assert allowed();p=A/driver
  row=start_service(name,driver,[],{str(p):sha(p),str(A/PROTOCOL):sha(A/PROTOCOL)})
  create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
""".replace('JOBS',repr(jobs)).replace('PROTOCOL',repr(protocol.name))
    ast.parse(source);assert not queue.exists();queue.write_text(source,encoding='utf8')
    # Actual CPU callbacks are independent of GPU fits and run immediately.
    for name,p in [('actual_rank60medium_twelve_parent183_callbacks_CPU_v2_20261011',outputs[10]),
                   ('actual_rank60medium2048_own6_native42_direct33_queue_v1_20261011',queue)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(protocol):sha(protocol)})
        create(A/(name+'_activation.json'),row)
    print({'predeclared_medium2048':True,'fresh_fit_count_claimed':0,'queue_gpu_serialized':True},flush=True)

if __name__=='__main__':main()

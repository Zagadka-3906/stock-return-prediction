"""Dispatch the frozen single-rank or dual embedding stage with unchanged complete parent."""
from types import SimpleNamespace
from stock_dual_embedding_after_complete_parent_native_stage_v1_20261010 import BACKENDS
GRAPH_KEY='stock_rank_dual44_after_complete_parent_v1_20261010'
def after_parent(ns,context,parent,spec,components):
    assert context._whole_graph[GRAPH_KEY]==spec and spec['anchor_round'] in (170,173)
    assert spec['position']=='after_complete_qualified_parent' and spec['first2020_active']
    translated=dict(spec)
    if spec['stage_kind']=='stock_rank_embedding_rank1d_direct':
        assert len(components)==1
        import stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010 as stage
        translated['original_complete_parent_round']=spec['anchor_round']
        context_copy=SimpleNamespace(**vars(context));context_copy._whole_graph={**context._whole_graph,stage.GRAPH_KEY:translated}
        value,report=stage.after_parent(ns,context_copy,parent,translated,components[0])
        report['native_reload_independent_tensor_and_Pandas_stage_bits_exact']=report['native_reload_independent_tensor_forward_and_Pandas_tail_bits_exact']
    else:
        assert spec['stage_kind']=='stock_return_rank_embedding_consensus' and len(components)==2
        import stock_dual_embedding_after_complete_parent_native_stage_v1_20261010 as stage
        context_copy=SimpleNamespace(**vars(context));context_copy._whole_graph={**context._whole_graph,stage.GRAPH_KEY:translated}
        value,report=stage.after_parent(ns,context_copy,parent,translated,components)
    report['selected44_original_parent_round']=spec['anchor_round']
    return value,report

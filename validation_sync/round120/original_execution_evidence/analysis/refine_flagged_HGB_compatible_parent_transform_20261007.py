"""Refine the106-trained flag branch while retaining a compatible complete parent's other outputs."""
from copy import deepcopy
import numpy as np
from conditional_residual_mlp_CDF_transform_20261007 import prepare,apply_prepared as reference_apply


def core(graph):
    value=deepcopy(graph)
    value.pop('conditional_flag_CPU_HGB_residual_CDF',None)
    value.pop('protected_upper_pool_CPU_HGB_CDF',None)
    def strip(node):
        if isinstance(node,dict):
            for key in ('path','independent_dump_path','independent_state_path'):node.pop(key,None)
            for child in node.values():strip(child)
        elif isinstance(node,list):
            for child in node:strip(child)
    strip(value)
    return value


def compatible(graph,reference_graph):
    return core(graph)==core(reference_graph)


def apply_prepared(complete_parent,reference106,flags,residual,weight,prepared):
    complete_parent,reference106,flags,residual=map(np.asarray,(complete_parent,reference106,flags,residual))
    assert complete_parent.shape==reference106.shape==flags.shape==residual.shape
    refined=reference_apply(reference106,residual,weight,prepared)
    values=np.asarray(complete_parent,dtype=np.float64).copy()
    selected=flags==1
    values[selected]=refined[selected]
    assert np.array_equal(values[~selected].view('u8'),np.asarray(complete_parent)[~selected].view('u8'))
    return values


def transform(complete_parent,reference106,dates,flags,valid,residual,weight,universe):
    return apply_prepared(complete_parent,reference106,flags,residual,weight,prepare(reference106,dates,flags,valid,universe))

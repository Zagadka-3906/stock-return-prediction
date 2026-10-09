"""Compare the retained106 core while replacing existing nonflag residual stages."""
from copy import deepcopy
from refine_flagged_HGB_compatible_parent_transform_20261007 import core as flag_core

def core(graph):
    value=deepcopy(graph)
    value.pop('nonflag_CPU_HGB_residual_CDF',None)
    value.pop('nonflag_CPU_SparseGram64_residual_CDF',None)
    value.pop('nonflag_CPU_ReverseBayes64_residual_CDF',None)
    value.pop('nonflag_CPU_EmpiricalBayes64_residual_CDF',None)
    value.pop('nonflag_CPU_ReverseBayes64_residual_CDF',None)
    value.pop('nonflag_CPU_Ridge_residual_CDF',None)
    value.pop('nonflag_CPU_RFFRidge_residual_CDF',None)
    value.pop('nonflag_CPU_RFF128_residual_CDF',None)
    return flag_core(value)

def compatible(graph,reference_graph):
    return core(graph)==core(reference_graph)

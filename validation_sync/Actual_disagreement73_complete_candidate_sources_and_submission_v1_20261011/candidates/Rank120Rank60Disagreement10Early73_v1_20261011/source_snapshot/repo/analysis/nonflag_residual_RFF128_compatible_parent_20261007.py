from copy import deepcopy
from nonflag_residual_RFFRidge_compatible_parent_20261007 import core as original_core
def core(graph):
    value=deepcopy(graph);value.pop('nonflag_CPU_RFF128_residual_CDF',None);return original_core(value)
def compatible(graph,reference_graph):return core(graph)==core(reference_graph)

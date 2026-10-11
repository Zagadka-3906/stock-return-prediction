from nonflag_residual_Ridge_compatible_parent_20261007 import core as parent_core
from copy import deepcopy
def core(graph):
    value=deepcopy(graph);value.pop('nonflag_CPU_RFFRidge_residual_CDF',None);return parent_core(value)
def compatible(graph,reference_graph):
    return core(graph)==core(reference_graph)

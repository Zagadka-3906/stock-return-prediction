"""Preserve root math; check empty standalone foundation before candidate-directory lookup."""
from pathlib import Path
import sys

def install():
    import optimize_training_round50 as owner
    original=owner.root_model_sources
    changed=[]
    def root_model_sources(graph):
        root=graph['root']
        if root['kind']=='standalone' or root['configuration'].get('standalone'):
            return {}
        return original(graph)
    for name,module in list(sys.modules.items()):
        if module is not None and getattr(module,'root_model_sources',None) is original:
            changed.append((name,module,original));setattr(module,'root_model_sources',root_model_sources)
    assert owner.root_model_sources is root_model_sources
    def restore():
        for name,module,before in reversed(changed):
            assert getattr(module,'root_model_sources') is root_model_sources,name
            setattr(module,'root_model_sources',before)
        assert owner.root_model_sources is original
    return restore,{'aliases_changed':[name for name,_,_ in changed],'standalone_empty_foundation_branch_same_as_original':True,'nonstandalone_delegates_exact_original_function':True,'candidate_read_order_only_changed':True}

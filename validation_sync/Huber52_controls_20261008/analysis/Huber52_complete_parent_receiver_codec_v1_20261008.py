"""Adapter for unchanged complete-parent CDF controls; fixed unused share preserves receiver schemas."""
from HuberIRLS64_complete_parent_CDF_v1_20261008 import MODES,prepare,apply_prepared,transform,pandas_oracle
from HuberIRLS64_complete_parent_CDF_v1_20261008 import mixture as signed_mixture,independent_mixture as signed_independent_mixture
from CrossFamily_complete_parent_CDF_v1_20261008 import selected
GROUPS=tuple(((names,sign),(names,sign)) for names,sign in MODES)


def mixture(raw,group,share=.5):
    assert share==.5
    return signed_mixture(raw,group)


def independent_mixture(raw,group,share=.5):
    assert share==.5
    return signed_independent_mixture(raw,group)

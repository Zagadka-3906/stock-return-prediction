"""Unchanged round41 with constructor-only configuration normalization."""
from late_context_initialization_recovery_20261004 import install
_original=install(41)
globals().update({name:value for name,value in vars(_original).items() if not name.startswith('__')})

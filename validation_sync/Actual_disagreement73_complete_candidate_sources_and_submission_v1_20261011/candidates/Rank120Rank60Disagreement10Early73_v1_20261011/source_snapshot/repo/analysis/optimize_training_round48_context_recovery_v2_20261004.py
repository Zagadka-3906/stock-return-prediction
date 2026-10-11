"""Round48 constructor-only typed-layer recovery, with exact warm-up scope."""
from late_context_initialization_recovery_v2_20261004 import install
_original=install(48)
globals().update({name:value for name,value in vars(_original).items() if not name.startswith('__')})

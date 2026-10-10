from contextlib import contextmanager
from pathlib import Path
import late_bound_dynamic_snapshot_encoder_runtime_v1_20261010 as original
from verified_shared_publication_board_loader_v1_20261011 import installed as shared_binding
@contextmanager
def installed(receiver,module_name,log):
 prior=original.bind
 def bind(publisher,binding_log=None):return shared_binding(publisher,Path(binding_log).with_name('shared_board_publication_binding.json') if binding_log else None)
 original.bind=bind
 try:
  with original.installed(receiver,module_name,log) as events:yield events
 finally:
  assert original.bind is bind;original.bind=prior

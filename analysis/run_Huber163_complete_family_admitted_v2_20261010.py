"""Run immutable admitted67 sources with explicit corrected administrative routes."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
import prepare_protected163_full_registry_sources_v1_20261010 as routes
old=routes.source_paths
routes.source_paths=lambda:list(dict.fromkeys([*old(),A/'run_Huber163_full_registration_cleanup_v2_20261010.py',A/'run_Huber163_complete_family_admitted_v2_20261010.py',A/'protected163_full_family_preflight_v1_20261010.json',A/'verify_Huber163_complete67_preflight_v1_20261010.py']))
source=A/'run_protected163_complete_family_v1_20261010.py';text=source.read_text(encoding='utf8')
assert text.count('ReusedNN162Quality19_round163_full_registration_v1_20261009')==1
text=text.replace('ReusedNN162Quality19_round163_full_registration_v1_20261009','ReusedNN163Quality19_round163_full_registration_v1_20261009')
assert text.count('run_protected163_full_registration_v1_20261010.py')==1
text=text.replace('run_protected163_full_registration_v1_20261010.py','run_Huber163_full_registration_cleanup_v2_20261010.py')
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})

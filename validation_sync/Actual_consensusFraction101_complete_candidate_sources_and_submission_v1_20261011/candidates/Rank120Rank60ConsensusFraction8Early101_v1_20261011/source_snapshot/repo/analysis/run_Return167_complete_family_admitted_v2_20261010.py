"""Admit only the corrected167 candidate and full registration receivers; keep prototypes immutable."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
def main():
    import prepare_protected167_full_registry_sources_v1_20261010 as routes
    old=routes.source_paths
    routes.source_paths=lambda:list(dict.fromkeys([*old(),Path(__file__),A/'run_Return167_full_registration_admitted_v2_20261010.py',A/'verify_Return167_complete67_preflight_v1_20261010.py',A/'protected167_full_family_preflight_v1_20261010.json',A/'prepare_protected167_selected_candidate_v3_20261010.py',A/'predict_protected_Return_after163_complete_scheme_v4_20261010.py',A/'Return167_actual_parent163_source_and_callback_controls_v2_20261010.json']))
    source=A/'run_protected167_complete_family_v1_20261010.py';text=source.read_text(encoding='utf8')
    replacements={'prepare_protected167_selected_candidate_v2_20261010.py':'prepare_protected167_selected_candidate_v3_20261010.py','run_protected167_full_registration_v1_20261010.py':'run_Return167_full_registration_admitted_v2_20261010.py'}
    for old,new in replacements.items():assert text.count(old)==1; text=text.replace(old,new)
    exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
if __name__=='__main__':main()

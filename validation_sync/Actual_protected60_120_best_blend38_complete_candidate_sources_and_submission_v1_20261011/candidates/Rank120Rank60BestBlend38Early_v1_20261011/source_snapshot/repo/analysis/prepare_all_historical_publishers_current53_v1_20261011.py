from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
s=(A/'start_current_publication_paths_and_prospective50_v3_20261011.py').read_text(encoding='utf8')
s=s.replace("p48=A/'actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json'","p48=A/'actual_current_publication_paths_and_prospective50_admission_v1_20261011.json'")
s=s.replace('old48=read(p48);old49=read(p49)','old48=read(p48);old49=read(p49);old49["tasks"]=[]')
s=s.replace("for name in old49['source_factories']:","for name in [*read(A/'actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json')['source_factories'],*old49['source_factories']]:")
s=s.replace("'source_factories':old49['source_factories']","'source_factories':[*read(A/'actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json')['source_factories'],*old49['source_factories']]")
s=s.replace("(A/'route_failed_future202_206_after_completed187_v49_20261011.py')","(A/'route_current_publication_paths_and_prospective50_v1_20261011.py')")
s=s.replace("PROOF=A/'actual_failed_future202_206_routes49_admission_v1_20261011.json'","PROOF=A/'actual_current_publication_paths_and_prospective50_admission_v1_20261011.json'")
s=s.replace(" s=s.replace("," s=s.replace(")
s=s.replace("s=s.replace(\"'actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json']\",\"'actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json','actual_failed_future202_206_routes49_admission_v1_20261011.json']\")", "s=s.replace(\"'actual_failed_future202_206_routes49_admission_v1_20261011.json']\",\"'actual_failed_future202_206_routes49_admission_v1_20261011.json','actual_current_publication_paths_and_prospective50_admission_v1_20261011.json']\")")
# The copied runtime already contains module correction binding; do not insert it twice.
start=s.index('s=s.replace(" data[\'service_aliases\']')
end=s.index('\nast.parse(s);',start)
s=s[:start]+s[end:]
s=s.replace('_actual_family_paths51.py','_actual_family_paths54.py').replace('prospective50','prospective53').replace('current50_wrapper','current53_wrapper').replace('supersession50','supersession53').replace('recovery50_','recovery53_').replace('^recovery(48|49)_','^recovery(48|49|50)_')
# Preserve the old proof path in the matching expression, while writing and using a new proof.
s=s.replace("s=s.replace(\"PROOF=A/'actual_current_publication_paths_and_prospective53_admission_v1_20261011.json'\",\"PROOF=A/'actual_current_publication_paths_and_prospective53_admission_v1_20261011.json'\")","s=s.replace(\"PROOF=A/'actual_current_publication_paths_and_prospective50_admission_v1_20261011.json'\",\"PROOF=A/'actual_current_publication_paths_and_prospective53_admission_v1_20261011.json'\")")
s=s.replace("p48=A/'actual_current_publication_paths_and_prospective53_admission_v1_20261011.json'","p48=A/'actual_current_publication_paths_and_prospective50_admission_v1_20261011.json'")
s=s.replace("(A/'route_current_publication_paths_and_prospective53_v1_20261011.py')","(A/'route_current_publication_paths_and_prospective50_v1_20261011.py')")
p=A/'start_current_publication_paths_and_prospective53_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');print(p,flush=True)

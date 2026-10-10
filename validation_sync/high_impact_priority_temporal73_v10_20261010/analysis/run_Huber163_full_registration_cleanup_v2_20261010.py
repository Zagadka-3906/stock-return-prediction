"""Restore the nested ranking adapter before the outer writer leaves its scope."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
import prepare_protected163_full_registry_sources_v1_20261010 as routes
old=routes.source_paths
routes.source_paths=lambda:list(dict.fromkeys([*old(),A/'run_Huber163_full_registration_cleanup_v2_20261010.py',A/'run_Huber163_complete_family_admitted_v2_20261010.py',A/'protected163_full_family_preflight_v1_20261010.json',A/'verify_Huber163_complete67_preflight_v1_20261010.py']))
source=A/'run_protected163_full_registration_v1_20261010.py';text=source.read_text(encoding='utf8')
needle="closed('ReusedNN162Quality19_round161_full_registration_v1_20261009')";assert text.count(needle)==1
text=text.replace(needle,"closed('ReusedNN162Quality19_round162_full_registration_v1_20261009')")
needle="            create(folder/'full_registration_execution.json'";assert text.count(needle)==1
text=text.replace(needle,"            assert restore_ranking is not None\n            restore_ranking();restore_ranking=None\n"+needle)
text=text.replace('预定两类保护头部方案各37项，以及两个已合格锚点，共76项；连续官方S优先','已实际完成Huber65项连接验证，加合格161/162锚点，共67条；连续官方S优先')
namespace={'__file__':str(source),'__name__':'__main__'}
exec(compile(text,str(source),'exec'),namespace)

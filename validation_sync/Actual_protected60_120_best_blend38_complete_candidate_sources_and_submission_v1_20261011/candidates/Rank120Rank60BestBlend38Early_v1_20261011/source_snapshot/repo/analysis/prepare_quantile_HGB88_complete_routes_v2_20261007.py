"""Correct seven-case admission and freeze complete119 routes before launching anything."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    files={
      'prepare_quantile_HGB88_round119_sources_20261007.py':'prepare_quantile_HGB88_round119_sources_v2_20261007.py',
      'verify_quantile_HGB88_round119_sources_20261007.py':'verify_quantile_HGB88_round119_sources_v2_20261007.py',
      'run_quantile_HGB88_round119_full_registration_20261007.py':'run_quantile_HGB88_round119_full_registration_v2_20261007.py',
      'publish_quantile_HGB88_evidence_20261007.py':'publish_quantile_HGB88_evidence_v2_20261007.py'}
    paths=[Path(__file__)]
    for old,new in files.items():
        s=(A/old).read_text(encoding='utf8')
        for o,n in files.items():s=s.replace(o[:-3],n[:-3])
        if old.startswith('verify_'):
            s=s.replace("assert len(read(native)['records'])==88","assert len(read(native)['records'])==7")
            s=s.replace("'canonical118_sources_written':0","'canonical119_sources_written':0")
            s=s.replace("'graph_metadata_controls':9", "'graph_metadata_controls':24")
            needle="    closed('all_forecast_percentiles_full_scoring_benchmark')";assert needle in s
            s=s.replace(needle,needle+"\n    closed('cached_official_spearman_full12_benchmark')")
            needle="    for p in sources:";assert needle in s
            s=s.replace(needle,"    sources += [A/'prepare_quantile_HGB88_complete_routes_v2_20261007.py',A/'quantile_HGB88_complete_routes_source_preparation_v2_20261007.json']\n"+needle)
        elif old.startswith('publish_'):
            needle="    if phase=='scores':\n        for row in proof['records']:";assert needle in s
            s=s.replace(needle,"    sources += [A/'prepare_quantile_HGB88_complete_routes_v2_20261007.py',A/'quantile_HGB88_complete_routes_source_preparation_v2_20261007.json',\n      A/'prepare_quantile_HGB88_round119_sources_20261007.py',A/'verify_quantile_HGB88_round119_sources_20261007.py',\n      A/'run_quantile_HGB88_round119_full_registration_20261007.py',A/'publish_quantile_HGB88_evidence_20261007.py']\n"+needle)
        p=A/new;assert not p.exists();compile(s,str(p),'exec');p.write_text(s,encoding='utf8');paths += [A/old,p]
    create(A/'quantile_HGB88_complete_routes_source_preparation_v2_20261007.json',{'status':'compiled_complete119_v2_correct_seven_native_hooks_and_explicit_full12_speed_gate','input_sha256':{str(p):sha(p) for p in paths},'new_native_fits':0,'new_quality_scores':0})
if __name__=='__main__':main()

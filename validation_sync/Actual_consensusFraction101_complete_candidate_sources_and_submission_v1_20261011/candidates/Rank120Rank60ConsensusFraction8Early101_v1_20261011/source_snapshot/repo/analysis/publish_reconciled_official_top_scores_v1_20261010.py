"""Publish all real37 scores only after the explicit pointer reconciliation closes."""
from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A),str(A.parent)]

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed,allowed
    assert allowed();closed('actual_protected_official_top_screen_v2_20261010_location_reconciliation_v2_20261010')
    import prepare_protected162_full_registry_sources_v1_20261010 as routes
    old=routes.source_paths
    archive=A/'service_owned_workflows_20261006/actual_protected_official_top_screen_v2_20261010_original_pointer_collision_evidence_v1_20261010'
    routes.source_paths=lambda:[*old(),Path(__file__),A/'protected_official_top_screen_v2_20261010_location_reconciliation_v2_20261010.json',*archive.glob('*.json'),*archive.glob('*.log')]
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from publish_high_impact_priority_v7_20261010 import main as publish
    publish('protected')

if __name__=='__main__':main()

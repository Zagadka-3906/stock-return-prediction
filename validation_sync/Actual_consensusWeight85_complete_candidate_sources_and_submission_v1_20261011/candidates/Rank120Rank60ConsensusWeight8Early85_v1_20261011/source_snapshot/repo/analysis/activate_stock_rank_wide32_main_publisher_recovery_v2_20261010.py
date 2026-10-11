from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    before=A/'publish_stock_rank_wide32_capacity_stages_main_v1_20261010.py'
    after=A/'publish_stock_rank_wide32_capacity_stages_main_v2_20261010.py'
    failure=A/'service_owned_workflows_20261006/actual_StockRankWide32_capacity_stages_main_v1_20261010/service_execution.json'
    assert read(failure)['status']=='failed'
    text=before.read_text(encoding='utf8').replace('text.index("    payload[(prefix/\'manifest.json\')]")','text.index("    payload[(prefix/\'manifest.json\').as_posix()]")')
    assert text!=before.read_text(encoding='utf8')
    template=(A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py').read_text(encoding='utf8')
    assert "    payload[(prefix/'manifest.json').as_posix()]" in template
    assert not after.exists();compile(text,str(after),'exec');after.write_text(text,encoding='utf8',newline='\n')
    create(A/'stock_rank_wide32_main_publisher_recovery_v2_20261010.json',{'status':'fixed_exact_template_manifest_locator_before_any_new_publication','input_sha256':{str(p):sha(p) for p in [Path(__file__),before,after,failure]},'original_failed_service_preserved':True})
    row=start_service('actual_StockRankWide32_capacity_stages_main_v2_20261010',after.name,[],{str(after):sha(after)})
    create(A/'actual_StockRankWide32_capacity_stages_main_v2_20261010_activation.json',row)
    print(row['name'],flush=True)
if __name__=='__main__':main()

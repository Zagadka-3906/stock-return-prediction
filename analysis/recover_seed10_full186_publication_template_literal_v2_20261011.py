"""Preserve the failed source-only publisher and namespace transport before injecting immutable paths."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    folder=A/'service_owned_workflows_20261006/actual_Seed10_full186_source_capsules_main_v1_20261011'
    execution=read(folder/'service_execution.json');launch=read(folder/'native_launch.json')
    assert execution['status']=='failed' and 'publish_Seed10_full186_sources_main' in execution['failure'] and not owned(launch)
    source=A/'publish_seed10_full186_source_capsules_main_v1_20261011.py'
    text=source.read_text(encoding='utf8')
    line="    text=text.replace('StockRank20_actual_own6_full5_v66_20261010','Seed10_full186_sources_v1_20261011').replace('StockRank20_actual_own6_full5_main_v66_20261010','Seed10_full186_sources_main_v1_20261011').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010','Seed10_full186_sources_main_receipt_v1_20261011')\n"
    assert text.count(line)==1;text=text.replace(line,'')
    marker="    text=template.read_text(encoding='utf8')\n";assert text.count(marker)==1
    text=text.replace(marker,marker+line)
    # This fresh payload has distinct paths, scratch and receipt names; original failure remains intact.
    text=text.replace('Seed10_full186_sources_v1_20261011','Seed10_full186_sources_v2_20261011')
    text=text.replace('Seed10_full186_sources_main_v1_20261011','Seed10_full186_sources_main_v2_20261011')
    text=text.replace('Seed10_full186_sources_main_receipt_v1_20261011','Seed10_full186_sources_main_receipt_v2_20261011')
    text=text.replace('publish_Seed10_full186_sources_payload_main_v1_20261011.py','publish_Seed10_full186_sources_payload_main_v2_20261011.py')
    proof=A/'seed10_full186_publication_literal_recovery_v2_20261011.json'
    marker='    assert all(p.is_file() for p in paths)';assert text.count(marker)==1
    additions=[str(Path(__file__)),str(proof),str(folder/'service_execution.json'),str(folder/'stderr.log'),str(A/'publish_Seed10_full186_sources_payload_main_v1_20261011.py')]
    text=text.replace(marker,'    paths += [Path(p) for p in '+repr(additions)+']\n'+marker)
    driver=A/'publish_seed10_full186_source_capsules_main_v2_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    create(proof,{'status':'preserved_original_source_only_publication_failure_before_any_Git_push',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,folder/'service_execution.json',folder/'stderr.log']},
        'reason':'Namespace substitution altered an immutable template filename inside the injected path list; apply substitution before injecting paths',
        'source_only_transport_correction':True,'original_failure':execution,'new_model_fits':0,'new_quality_scores':0,'actual_future_X_read':False})
    assert allowed()
    name='actual_Seed10_full186_source_capsules_main_v2_20261011'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/(name+'_activation.json'),row)
    print({'actual_source_publication_v2_queued':True,'no_scientific_task_restarted':True},flush=True)

if __name__=='__main__':main()

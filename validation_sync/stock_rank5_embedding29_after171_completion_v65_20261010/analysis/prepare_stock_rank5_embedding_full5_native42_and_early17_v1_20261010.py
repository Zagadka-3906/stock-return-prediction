"""Bind actual five-day models to complete independent replay and predeclared171 screening."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
RECIPE='stock_rank5_embedding16_cross120_rank5mean_recent252_small512_BF16_e64'
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def route(text):
    return text.replace('stock_rank_embedding','stock_rank5_embedding').replace('StockRankEmbedding','StockRank5Embedding').replace('stock_rank5_embedding16_cross120_rank1d_recent252_small512_BF16_e24',RECIPE).replace('stock_rank5_embedding_rank1d_direct','stock_rank5_embedding_rank5mean_direct')
def main():
    assert allowed();inputs=[];outputs=[]
    source=A/'verify_stock_rank_embedding_small512_full5_independent_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace("len(bundle['training_losses']) == 24","len(bundle['training_losses']) == 64")
    full=save('verify_stock_rank5_embedding_small512_full5_independent_v1_20261010.py',text);outputs.append(full)
    source=A/'stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace("len(original['training_losses'])==24","len(original['training_losses'])==64").replace('(169,170,171,172,173)','(169,170,171,172,173,174,175,176)')
    stage=save('stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py',text);outputs.append(stage)
    source=A/'verify_stock_rank_embedding_six_state_native42_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8'))
    text=''.join(line for line in text.splitlines(keepends=True)if ".exists():closed('StockEmbedding173_selected_candidate_sealing_v1_20261010')"not in line)
    native42=save('verify_stock_rank5_embedding_six_state_native42_v1_20261010.py',text);outputs.append(native42)
    source=A/'run_stock_rank_embedding_after170_fast17_screen_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8'))
    text=text.replace('Cross120170_complete132_family_v5_20261010','Frontier233171_complete233_family_v2_20261010').replace("release['scored_records']==132","release['scored_records']==233").replace('170','171')
    screen=save('run_stock_rank5_embedding_after171_fast17_screen_v1_20261010.py',text);outputs.append(screen)
    s=importlib.import_module(stage.stem);m=importlib.import_module(screen.stem)
    assert list(s.BACKENDS)==[RECIPE] and len(m.cases())==17 and m.cases()[0]['kind']=='anchor171'
    proof=A/'stock_rank5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_new_rank5_own64_full5_native42_and_original17_171_anchor_cases_actual_phase_completion_pending','input_sha256':{str(p):sha(p)for p in [Path(__file__),*inputs,*outputs,A/'stock_rank5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json']},'recipe':RECIPE,'expected_full_validation_rows':5635800,'native42_saved_states':6,'scored_records':17,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    text="""from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('actual_stock_rank5_embedding_own_training_queue_v1_20261010')
    for p,d in read(A/'stock_rank5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json')['input_sha256'].items():assert sha(p)==d,p
    for name,driver in TASKS:
        assert allowed();p=A/driver;row=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),row);closed(name)
if __name__=='__main__':main()
""".replace('TASKS',repr([('StockRank5EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',full.name),('actual_stock_rank5_embedding_six_state_native42_v1_20261010',native42.name),('actual_stock_rank5_embedding_after171_fast17_screen_v1_20261010',screen.name)]))
    driver=save('run_stock_rank5_embedding_full5_native42_and_early17_queue_v1_20261010.py',text);row=start_service('actual_stock_rank5_embedding_full5_native42_and_early17_queue_v1_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/'actual_stock_rank5_embedding_full5_native42_and_early17_queue_activation_v1_20261010.json',row);print({'actual_rank5_full5_42_17_queue_started':True,'original_cases':17,'new_scores':0},flush=True)
if __name__=='__main__':main()

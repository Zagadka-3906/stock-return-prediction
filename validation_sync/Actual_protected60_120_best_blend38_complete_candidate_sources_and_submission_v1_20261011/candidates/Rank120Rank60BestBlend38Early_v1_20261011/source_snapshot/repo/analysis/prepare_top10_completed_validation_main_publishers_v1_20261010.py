"""Publish actual Top10 classifier native42 and17 scoring batches only once complete."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    for original,number in [('publish_stock_rank_embedding_six_state_native42_completion_v54_20261010.py',58),('publish_stock_rank_embedding_after170_completion_v55_20261010.py',59)]:
        text=(A/original).read_text(encoding='utf8').replace('stock_rank_embedding','stock_top10_embedding').replace('StockRankEmbeddingSmall512','StockTop10EmbeddingSmall512')
        text=text.replace('stock_top10_embedding_native_stage_and_fast17_sources_admission_v1_20261010','stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010')
        if number==58:
            text=text.replace('v54_20261010','v58_20261010');name='actual_stock_top10_embedding_native42_completion_main_v58_20261010'
        else:
            text=text.replace('after170','after174').replace('v55_20261010','v59_20261010')
            begin=text.index('    for admission in (');end=text.index('    bank=Path',begin)
            text=text[:begin]+"    for admission in ('stock_top10_embedding_own_sources_admission_v1_20261010.json','stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010.json'):\n        paths += [A/admission,*[Path(p) for p in read(A/admission)['input_sha256'] if Path(p).suffix=='.py']]\n"+text[end:]
            name='actual_stock_top10_embedding_after174_completion_main_v59_20261010'
        newname=original.replace('stock_rank_embedding','stock_top10_embedding').replace('after170','after174').replace('v54_','v58_').replace('v55_','v59_')
        dest=A/newname;assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n')
        row=start_service(name,dest.name,[],{str(dest):sha(dest)});create(A/(name+'_activation.json'),row)
    print({'Top10_completed_validation_main_publishers':[58,59],'new_quality_scores':0},flush=True)
if __name__=='__main__':main()

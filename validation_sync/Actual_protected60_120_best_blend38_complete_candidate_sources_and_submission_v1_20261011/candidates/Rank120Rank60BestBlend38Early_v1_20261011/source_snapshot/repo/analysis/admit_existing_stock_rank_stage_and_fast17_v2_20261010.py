"""Recover a config-key-only source admission failure without recreating prior files."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    native=__import__('stock_rank_embedding_small512_BF16_native_v1_20261010')
    assert native.CONFIG['target']=='y_rank' and native.CONFIG['return_target_scale']==1.
    screen=__import__('run_stock_rank_embedding_after170_fast17_screen_v1_20261010');cases=screen.cases()
    paths=[Path(__file__),A/'prepare_stock_rank_stage_and_fast17_v1_20261010.py',A/'stock_rank_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json',A/'stock_rank_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py',A/'verify_stock_rank_embedding_six_state_native42_v1_20261010.py',A/'run_stock_rank_embedding_after170_fast17_screen_v1_20261010.py',A/'stock_rank_embedding_small512_BF16_native_v1_20261010.py',A/'stock_rank_embedding_saved_tensor_decoder_v1_20261010.py']
    for p in paths:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    # Continue only the unexecuted tail of the preserved generator: proof and dispatcher.
    prototype=(A/'prepare_stock_rank_stage_and_fast17_v1_20261010.py').read_text(encoding='utf8')
    body=prototype[prototype.index("    create(A/'stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'"):prototype.index("\nif __name__=='__main__':main()")]
    import textwrap
    exec(compile(textwrap.dedent(body),str(Path(__file__)),'exec'),dict(globals(),paths=paths,cases=cases,native=native))
if __name__=='__main__':main()

from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent
sys.path[:0]=[str(A.parent),str(A)]
def main():
    p=A/'activate_capacity181_complement182_routes6_sources_main_v67_20261010.py';q=A/'activate_tiny183_QA94_sources_main_v71_20261010.py'
    text=p.read_text(encoding='utf8').replace('import prepare_StockRankWide32Embedding181_complete48_pipeline_v2_20261010 as wide','import prepare_StockRank20Tiny183_complete85_pipeline_v1_20261010 as wide')
    text=text.replace('Capacity181_Complement182_actual_routes6_sources','Tiny183_QA94_actual_sources').replace('capacity181_complement182_routes6_sources','tiny183_QA94_sources').replace('v67_20261010','v71_20261010')
    text=text.replace('extras=[',"extras=['stock_rank20_embedding183_full_execution_sources_admission_v1_20261010.json','prepare_StockRank20Tiny183_complete85_pipeline_v1_20261010.py','publish_rank20_tinyCDF82_stages_main_v68_20261010.py',")
    text=text.replace("'full181_records':48","'full183_records':85,'full183_full_controls':80,'full183_prefix_controls':240,'full183_expected_board':17258,'full183_QA':94")
    text=text.replace('保存身份32维容量181轮48项与20日排名互补182轮63项完整流程；实际111别名、9候选入口、12父方案回调CPU验证及真实终端修复','保存第183轮82项微权重互补与3个合格锚点组成的85项完整流程，QA94与17258项完整榜源码；尚未执行未来推理')
    assert not q.exists();compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n')
    runpy.run_path(str(q),run_name='__main__')
if __name__=='__main__':main()

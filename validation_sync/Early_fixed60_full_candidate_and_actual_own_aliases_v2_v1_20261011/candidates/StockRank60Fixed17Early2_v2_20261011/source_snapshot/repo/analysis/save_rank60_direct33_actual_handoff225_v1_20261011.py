from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from monitor_verified_current_optimization_v118_20261011 import status
def main():
 assert allowed()
 proof=A/'stock_rank60_after183_direct33_predeclared_sources_v1_20261011.json';cpu=A/'stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json'
 for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
 assert len(read(cpu)['records'])==12 and len(read(proof)['cases'])==33
 names=['actual_stock_rank60_embedding_after183_direct_allocation33_v1_20261011','actual_rank60_after183_completed33_main_v1_20261011','actual_rank60_direct33_predeclared_CPU_sources_main_v1_20261011','actual_stock_rank60_native42_and_fast46_queue_v2_20261011','actual_stock_rank60_embedding_after175_fast17_screen_v1_20261011','actual_stock_rank20class25_embedding_after175_large_allocation29_screen_v1_20261011','recovery15_StockTopPairEmbedding185_round185_full_registration_v1_20261010']
 counts={}
 for name,dirname,total in [('H60_fast17','StockRank60EmbeddingSmall512_after175_high_impact17_screen_v1_20261011',17),('Class25_large29','StockRank20Class25EmbeddingSmall512_after175_large_allocation29_screen_v1_20261011',29)]:
  rows=[read(p) for p in (Path('E:/赛题五_本机临时')/dirname).glob('case*_official.json')]
  counts[name]={'completed':len(rows),'expected':total,'best_S':max((r['connected_final_score'] for r in rows),default=None),'complete_not_claimed':len(rows)!=total}
 record={'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat(),'stop_at_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],'status':'active_actual_new33_and12_CPU_controls_not_complete_goal','previous_goal_turn_classification':'progress','source_sha256':{str(p):sha(p) for p in (Path(__file__),proof,cpu)},'services':{n:status(n) for n in names},'score_counts':counts,'actual_cpu_callback_cases':12,'actual_direct33_scores_completed':0,'future_qualification_pending':True,'latest_fully_qualified_delivery':read(A/'latest_verified_submission_delivery_v2_20261008.json'),'next_actions':['Monitor original H60 fast17+large29; direct33 and mixed49 both wait that actual completion.','Direct33 proof/output are separate from mixed49, use pure H60 recipe and corrected183 stagev2 and predictorv2.','Build prospective complete200 with35 records=complete183 anchor+complete199 anchor+actualdirect33; expected QA111/connected18149/W483. Reuse corrected196 single-bank normalizer/native14/selectedcandidate templates via actual37 overrides and shared actual199 full pipeline. Require real all8 anchor metrics/main before normalization.','Do not call new183 CPU callbacks native14: CPU stubs only; chosen stage must pass actual native14 and cold replay before reading candidate future X.','Source predeclaration and completed33 publishers are actual owned queues; receipts are still pending.','Observer118 covers through199 plus newtwo-stream scheduler; next observer update should include direct33 and completed200 after source factory is real.','At13:00 stop project tasks and pause goal only after actual guard/recovery records; no automatic restart.'],'goal_exhaustion_proven':False,'new_native_fits_by_this_round':0}
 create(A/'actual_pure_H60_direct33_and_CPU12_handoff_v225_20261011.json',record)
 print({'actual_CPU12':12,'predeclared_direct33':33,'live_scores':counts,'goal_active':True},flush=True)
if __name__=='__main__':main()

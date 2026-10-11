from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
if __name__=='__main__':
 assert allowed();control=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json');data=read(A/'actual_optimization_fast_runtime_handoff_v205_20261011.json');actual={}
 names=['actual_fast_optimization_progress_reboot_v113_20261011','actual184_registered_QA_main_resume29_v1_20261011','actual_parent3134_frozen_publication_runtime_sources_main_v1_20261011','actual_stock_rank20class25_BCE_own6_full5_queue_v1_20261011','actual_stock_rank20class25_CPU6_sources_main_v1_20261011','actual_stock_rank20class25_objective_stages_main_v1_20261011','StockRank20Class10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011']
 for n in names:
  f=A/'service_owned_workflows_20261006'/n;identity=read(f/'native_launch.json');terminal=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None;actual[n]={'status':terminal['status'] if terminal else 'running_exact_owned' if owned(identity) else 'not_owned_no_terminal','identity':identity,'terminal':terminal}
 proofs=['stock_rank20class25_BCE_own6_sources_admission_v1_20261011.json','stock_rank20class25_balanced_BCE_actual_CPU_controls_v1_20261011.json','rank20class25_actual_reused_fixture_gate_v1_20261011.json','stock_rank20class25_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json','actual_observer113_class25_sources_admission_v1_20261011.json']
 notes=['Previous goal turn was progress: actual Class10 six independent annual models completed; actual Class25 independent BCE scalar/gradient6, mature49153 fixture gate, callback11 passed; new fresh bank/scoring46 queues activated, source/stage main publishers queued.',
 'Deadline remains actual user13:00 today; keep goalactive until cutoff; source control10 and09 read before dispatch. Actual13 guardian live; do not restart old11 guardian.',
 'Current observer113 writes handoff205 and stable current Markdown. Full current identity and predecessor recovery details remain handoff203; current parentchain31/objectives34, not retired32/33.',
 'Class25 labels use mature20mean raw rank>=.75, centered threshold>=.25, BCEposweight3, fresh six states. Clone actual Class10 controls and independent decoder, same252/64/seed. Actual scalar/gradient oracle changed3 consistently and tests include exact .25 boundary.',
 'Class25 training queue waits Class10native42 before restart/GPU, its CPU6 andfixture andcallback11 alreadypassed. Class25score46 waits Class10after18317, preserves science jobs.',
 'Class10full5 observed real owned29572 performing independent Pandas perdate rank; actual2020/2021 complete and80/160 prefix bitexact. Do not restart basedon observation timeout.',
 '184resume29 observed real owned25132 in complete ranking QA JSONdecoder; originalscore48reported, main184/17306 stillpending. Strict133cachedcapsules controls and watcher12hold2+externalpublisher3 fixed. Bridge30 checks actualcandidate/source hashes then dispatch31.',
 'Class10 after18317 and main publisher queued; if actualS improves complete19 normal/native14/future196/Q10717967/W479 anchors183195, then Class25 full197 or adjust honest prospective numbering; no196/197fullfactoryexistsyet.',
 'Class195 full48 factory compiledpassed; normalization,selected14, future,fullQA106/main17948 pending parent19434 andactual46. v2classpublication is metadataalias of actual3phasev1 receipts, not duplicate science.',
 'Unfinished scientific and main outputs are not passed. No feasible/resource boundary has been proven; completed qualified183 retained, cached149higher pending189qualification. Source Gitindex unchanged, models/data/tempE, mainonly.']
 p=A/'actual_class25_CPU_and_class10_completed6_handoff_v206_20261011.json';create(p,{'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat(),'stop_at_local':control['stop_at_local'],'actual_services_now':actual,'observer_state':data,'source_proof_sha256':{str(A/n):sha(A/n) for n in proofs},'notes':notes,'root_git_index_sha256':sha(ROOT/'.git/index'),'goal_exhaustion_proven':False,'full_goal_complete':False})
 print({'handoff206_actual_progress_saved':True,'verified_current_services':{n:r['status'] for n,r in actual.items()}},flush=True)

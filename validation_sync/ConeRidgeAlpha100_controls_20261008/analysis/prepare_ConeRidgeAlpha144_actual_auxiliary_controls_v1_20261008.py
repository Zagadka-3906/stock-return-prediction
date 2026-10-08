"""Fresh exact saved-model hooks/calendar and independently recomputed current-parent CDF controls."""
from pathlib import Path
import io,sys,time,tokenize
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def adapt(text):
    mapping={
        'ConeRidgeFine65':'ConeRidgeAlpha97','ConeRidgeFine68':'ConeRidgeAlpha100',
        'ConeRidgeFine24':'ConeRidgeAlpha48','ConeRidgeFine143':'ConeRidgeAlpha144',
        'ConeRidgeFine_multiyear':'ConeRidgeAlpha_multiyear',
        'ConeRidge64_complete_parent':'ConeRidgeAlpha8_64_complete_parent',
        'round143':'round144','final143':'final144','actual143':'actual144',
        '第143轮':'第144轮','full143':'full144','_r143':'_r144',
        'qa54':'qa55','QA54':'QA55','qa_v54':'qa_v55',
        'actual68':'actual100','actual65':'actual97','actual24':'actual48',
        '65_current':'97_current','65_full195':'97_full291','and195':'and291',
        'CDF195':'CDF291','65full195':'97full291','all65_nonanchors':'all97_nonanchors',
        'actual20_heads':'actual40_heads','actual20 existing':'actual40 existing',
        'ConeRidge20_causal_refit_controls_v1':'ConeRidgeAlpha40_causal_refit_v2',
        'actual_ConeRidge20_causal_refit_location_v1':'actual_ConeRidgeAlpha40_causal_refit_location_v2',
    }
    for before,after in mapping.items():text=text.replace(before,after)
    numeric={'68':'100','65':'97','195':'291','1560':'2619','143':'144'}
    tokens=list(tokenize.generate_tokens(io.StringIO(text).readline))
    text=tokenize.untokenize([t._replace(string=numeric[t.string]) if t.type==tokenize.NUMBER and t.string in numeric else t for t in tokens])
    text=text.replace('(132,133,134)','(132,134,143)').replace('(132, 133, 134)','(132, 134, 143)')
    text=text.replace('range(8)','range(16)')
    text=text.replace('frozen_before_actual18_historical_hooks','frozen_before_actual48_historical_hooks')
    text=text.replace('new_actual65_current','new_actual97_current').replace('reused_actual65_147','reused_actual97_291')
    return text

def save(name,text):
    path=A/name;assert not path.exists(),path;compile(text,str(path),'exec')
    path.write_text(text,encoding='utf8',newline='\n');return path

def main():
    plan=A/'ConeRidgeAlpha100_round144_plan_v1_20261008.json';assert len(read(plan)['heads'])==8
    sources=[Path(__file__),plan];outputs=[]
    for original in ('verify_ConeRidgeFine24_native_historical_hooks_v1_20261008.py',
                     'verify_ConeRidgeFine_multiyear_native_calendar_v1_20261008.py',
                     'verify_ConeRidgeFine65_current_parent_v1_20261008.py'):
        source=A/original; sources.append(source);text=adapt(source.read_text(encoding='utf8'))
        if 'native_historical_hooks' in original:
            text=text.replace('/24:', '/48:').replace("'groups':6","'groups':16")
            text=text.replace('actual24_', 'actual48_').replace('and24_', 'and48_')
            text=text.replace("'actual_hooks':24,'actual_cold_hooks':24","'actual_hooks':48,'actual_cold_hooks':48")
            text=text.replace('assert read(proof)', 'assert read(proof)')
        elif 'calendar' in original:
            text=text.replace('actual24_', 'actual48_').replace('and48_day', 'and96_day')
            text=text.replace("'actual_calendar_cases':24,'actual_whole_day_controls':64", "'actual_calendar_cases':48,'actual_whole_day_controls':96")
            text=text.replace("'rejected_pre_fit_cases':rejected", "'rejected_pre_fit_cases':rejected")
        else:
            old="'ConeRidgeAlpha144_historical_causal_main_publication_v1_20261008'"
            assert old in text;text=text.replace(old,"'ConeRidgeAlpha8_completed_controls_main_publication_v1_20261008'")
            text=text.replace("'status':'passed_current_parent49_147_on_E'", "'status':'passed_actual_current_parent97_291_on_E'")
        outputs.append(save(adapt(original),text))
    pins={str(p):sha(p) for p in [*sources,*outputs]}
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=[('ConeRidgeAlpha48_native_historical_hooks_v1_20261008','verify_ConeRidgeAlpha48_native_historical_hooks_v1_20261008.py'),
          ('ConeRidgeAlpha_multiyear_native_calendar_v1_20261008','verify_ConeRidgeAlpha_multiyear_native_calendar_v1_20261008.py'),
          ('ConeRidgeAlpha97_current_parent_controls_v1_20261008','verify_ConeRidgeAlpha97_current_parent_v1_20261008.py')]
    launches={name:start(name,driver,[],pins) for name,driver in jobs}
    create(A/'ConeRidgeAlpha144_actual_auxiliary_hidden_launches_v1_20261008.json',{
        'status':'started_actual48_native48_cold48_calendar96_day_and97_current291_cold_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'launches':launches,
        'actual_quality_scores':0,'actual_future_X_and_Y_read':False,
        'complete100_pipeline_still_required':True})
    print('Actual Alpha144 auxiliary native/calendar/current controls dispatched; no quality claimed.',flush=True)

if __name__=='__main__':main()

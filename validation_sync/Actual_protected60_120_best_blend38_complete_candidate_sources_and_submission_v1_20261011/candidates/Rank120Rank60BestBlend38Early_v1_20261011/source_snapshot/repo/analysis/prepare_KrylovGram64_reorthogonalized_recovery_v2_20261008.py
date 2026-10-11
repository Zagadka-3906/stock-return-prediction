"""Fresh numerical recipe after the16-step recurrence failed an independent actual-data oracle."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    failure=A/'service_owned_workflows_20261006/nonflag_KrylovGram64_actual200k_v1_20261008'
    assert not owned(read(failure/'native_launch.json')) and read(failure/'service_execution.json')['status']=='failed'
    sources=[Path(__file__),failure/'native_launch.json',failure/'job_definition.json',failure/'service_execution.json',failure/'stderr.log',failure/'stdout.log'];outputs=[]
    source=A/'nonflag_KrylovGram64_streamed_v1_20261008.py';text=source.read_text(encoding='utf8');sources.append(source)
    text=text.replace('krylovGram64_s','krylovGram64r2_s').replace("'centered_covariance_symmetrized':True}","'centered_covariance_symmetrized':True,'direction_reorthogonalization_passes':2,'residual_recomputed_each_iteration':True}")
    text=text.replace('fixed8192_centered_damped_CG64','fixed8192_centered_reorthogonalized_CG64_v2').replace('nonflag_residual_KrylovGram64','nonflag_residual_KrylovGram64_v2')
    first='    squared=float(residual@residual);initial=squared;iterations=0'
    last='    model.coef_=coef;model.intercept_='
    left=text.index(first);right=text.index(last)
    text=text[:left]+'''    squared=float(residual@residual);initial=squared;iterations=0;directions=[]
    for iteration in range(cfg['maximum_iterations']):
        residual=rhs-matrix@coef;squared=float(residual@residual)
        if squared<=initial*cfg['relative_residual_tolerance']**2:break
        direction=residual.copy()
        for repeat in range(cfg['direction_reorthogonalization_passes']):
            for previous,previous_product,previous_denominator in directions:
                direction-=previous*float(previous_product@direction)/previous_denominator
        product=matrix@direction;denominator=float(direction@product);assert denominator>0 and np.isfinite(denominator)
        step=float(direction@residual)/denominator;coef+=step*direction
        directions.append((direction.copy(),product.copy(),denominator));iterations=iteration+1
    residual=rhs-matrix@coef;squared=float(residual@residual)
'''+text[right:]
    target=A/'nonflag_KrylovGram64_streamed_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    for stem in ('verify_nonflag_KrylovGram64_small','verify_nonflag_KrylovGram64_actual200k'):
        source=A/(stem+'_v1_20261008.py');sources.append(source);text=source.read_text(encoding='utf8')
        text=text.replace('nonflag_KrylovGram64_streamed_v1_20261008','nonflag_KrylovGram64_streamed_v2_20261008')
        text=text.replace('verify_nonflag_KrylovGram64_small_v1_20261008','verify_nonflag_KrylovGram64_small_v2_20261008')
        text=text.replace('nonflag_KrylovGram64_small_v1_20261008','nonflag_KrylovGram64_small_v2_20261008').replace('nonflag_KrylovGram64_small_location_v1_20261008','nonflag_KrylovGram64_small_location_v2_20261008')
        text=text.replace('nonflag_KrylovGram64_actual200k_v1_20261008','nonflag_KrylovGram64_actual200k_v2_20261008').replace('nonflag_KrylovGram64_actual200k_location_v1_20261008','nonflag_KrylovGram64_actual200k_location_v2_20261008')
        target=A/(stem+'_v2_20261008.py');assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');outputs.append(target)
    create(A/'KrylovGram64_reorthogonalized_source_preparation_v2_20261008.json',{
        'status':'prepared_fresh_reorthogonalized_CG_recipe_after_actual16step_oracle_failure',
        'input_sha256':{str(p):sha(p) for p in [*sources,*outputs]},'failed_v1_preserved':True,
        'scientific_solver_changed_before_quality':True,'official_scores':0,'no_actual_future_X_or_Y_read':True})
    print('Fresh reorthogonalized2 native recipe and independent controls prepared; failed1 retained.',flush=True)

if __name__=='__main__':main()

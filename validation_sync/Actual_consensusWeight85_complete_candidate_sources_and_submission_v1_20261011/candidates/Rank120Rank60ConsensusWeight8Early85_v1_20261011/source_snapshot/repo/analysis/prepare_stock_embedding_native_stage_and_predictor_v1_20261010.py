"""Bind the saved mature vocabulary after a complete parent; independent stock embedding decoder."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
RECIPE='stock_embedding16_cross120_return1d_recent252_small512_BF16_e24'
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def once(text,before,after):
    assert text.count(before)==1,(before,text.count(before));return text.replace(before,after)
def main():
    original=A/'frontier133_after_complete_qualified_parent_native_stage_v1_20261010.py';text=original.read_text(encoding='utf8')
    begin=text.index('BACKENDS=');end=text.index('\nCODECS=',begin)
    text=text[:begin]+"BACKENDS={"+repr(RECIPE)+":('stock_embedding_small512_BF16_native_v1_20261010','stock_embedding_saved_tensor_decoder_v1_20261010')}"+text[end:]
    text=text.replace('frontier133_after_complete_qualified_parent','stock_embedding_after_complete_qualified_parent')
    text=text.replace("spec['original_complete_parent_round'] in (169,170)","spec['original_complete_parent_round'] in (169,170,171,172)")
    text=once(text,"    x=feature_matrix(context,meta);assert x.shape==(len(parent),120)","    from frontier233_after_complete_parent_native_stage_v1_20261010 import stock_identity\n    stock_identity(context)\n    assert meta['vocabulary_fitted_only_mature_training_rows']\n    x=feature_matrix(context,meta);assert x.shape==(len(parent),120)")
    text=once(text,"    original=joblib.load(path);assert original['config']==native.CONFIG and len(original['training_losses'])==64", "    original=joblib.load(path);assert original['config']==native.CONFIG and len(original['training_losses'])==24\n    assert original['stock_vocabulary']==meta['stock_vocabulary']\n    x=native.architecture.attach(x,context.frame['ts_code'].to_list(),original['stock_vocabulary'])\n    assert x.shape==(len(parent),121)")
    begin=text.index("    if spec['stage_kind']=='cross120_causal_smoothing':");end=text.index("    if spec['codec']=='CDF':",begin)
    text=text[:begin]+"    assert spec['stage_kind']=='stock_embedding_return1d_direct' and spec['recipe']=="+repr(RECIPE)+" and spec['decay'] is None\n"+text[end:]
    text=text.replace("'feature_count':120","'feature_count':121,'numeric_feature_count':120,'mature_stock_vocabulary_transform_only':True")
    stage=save('stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010.py',text)
    originalpredictor=A/'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py';text=originalpredictor.read_text(encoding='utf8')
    text=once(text,'def parent_filename(graph):',"def parent_filename(graph):\n    from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as key133\n    if key133 in graph:return 'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py'")
    text=text.replace('from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import after_parent,GRAPH_KEY','from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import after_parent,GRAPH_KEY')
    text=text.replace("spec['original_complete_parent_round'] in (169,170)","spec['original_complete_parent_round'] in (169,170,171,172)")
    text=text.replace('FRONTIER133_AFTER_WHOLE_QUALIFIED_PARENT','STOCK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT')
    text=text.replace('frontier133','stock_embedding').replace('Frontier133','StockEmbedding')
    #The delegated parent module name stays original; only our own stage/report
    #namespace is stock_embedding. Restore actual133 lineage routing explicitly.
    text=text.replace('from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as key133','from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY as key133')
    text=text.replace("if key133 in graph:return 'predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py'","if key133 in graph:return 'predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py'")
    predictor=save('predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010.py',text)
    import importlib
    s=importlib.import_module(stage.stem);p=importlib.import_module(predictor.stem)
    from frontier133_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY
    assert p.parent_filename({GRAPH_KEY:{}})=='predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py'
    candidate_sources=['predict_frontier133_complete_qualified_parent_scheme_v1_20261010.py','predict_frontier233_complete_parent_scheme_v1_20261010.py','predict_cross120170_complete169_scheme_v1_20261010.py','predict_fast_neural_frontier169_complete_scheme_v2_20261010.py']
    for name in candidate_sources:
        source=A/name;rewritten=p.prepared_parent(source.read_text(encoding='utf8'));compile(rewritten,str(source),'exec')
        assert rewritten.count('return STOCK_EMBEDDING_AFTER_WHOLE_QUALIFIED_PARENT(context,value)')==1
    create(A/'stock_embedding_native_stage_and_four_parent_routes_admission_v1_20261010.json',{'status':'compiled_stock_saved_vocabulary_stage_and_four_actual_parent_callback_routes','input_sha256':{str(p):sha(p) for p in [Path(__file__),original,originalpredictor,stage,predictor,*[A/n for n in candidate_sources]]},'actual_saved_stage_GPU_controls_pending':True,'full_future_native_replay_pending':True,'new_quality_scores':0})
    print('PASS actual four parent callback source routes; stock GPU stage replay pending',flush=True)
if __name__=='__main__':main()

"""Fresh runtime versions admit precreated E-only cache directories, never prior scientific outputs."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    inputs=[];outputs=[]
    p=A/'verify_stock_embedding_small512_restart_v1_20261010.py';inputs.append(p);text=p.read_text(encoding='utf8')
    text=text.replace('    assert not OUT.exists()\n    OUT.mkdir(parents=True)',"    assert not (OUT/'frozen_before_actual_controls.json').exists()\n    assert not (OUT/'small32').exists() and not (OUT/'wide2').exists()\n    OUT.mkdir(parents=True,exist_ok=True)")
    outputs.append(save('verify_stock_embedding_small512_restart_v3_20261010.py',text))
    p=A/'train_stock_embedding_small512_BF16_bank6_v1_20261010.py';inputs.append(p);text=p.read_text(encoding='utf8')
    text=text.replace('    if not OUT.exists():\n        OUT.mkdir(parents=True)',"    if not (OUT/'protocol.json').exists():\n        assert not any((OUT/str(y)).exists() for y in years)\n        OUT.mkdir(parents=True,exist_ok=True)")
    outputs.append(save('train_stock_embedding_small512_BF16_bank6_v3_20261010.py',text))
    p=A/'verify_stock_embedding_small512_small_CPU_v2_20261010.py';inputs.append(p);text=p.read_text(encoding='utf8')
    text=text.replace('import time\n','import time,os\nE_CACHE="E:/赛题五_本机临时/StockEmbeddingSmall512_independent_small_CPU_v1_20261009/tmp"\nfor key in ("TMP","TEMP","TMPDIR","TORCH_HOME","TORCHINDUCTOR_CACHE_DIR","TRITON_CACHE_DIR","CUDA_CACHE_PATH"):os.environ[key]=E_CACHE+"/"+key\nos.environ["CUDA_CACHE_DISABLE"]="1"\n')
    text=text.replace('    assert not out.exists();out.mkdir()',"    assert not (out/'verification.json').exists() and not (out/'frozen_before_actual_controls.json').exists();out.mkdir(parents=True,exist_ok=True)")
    outputs.append(save('verify_stock_embedding_small512_small_CPU_v3_20261010.py',text))
    p=A/'verify_stock_embedding_small512_full5_independent_v2_20261010.py';inputs.append(p);text=p.read_text(encoding='utf8')
    text=text.replace('    assert not OUT.exists();OUT.mkdir(parents=True)',"    assert not (OUT/'frozen_before_actual_independent_full_controls.json').exists();OUT.mkdir(parents=True,exist_ok=True)")
    outputs.append(save('verify_stock_embedding_small512_full5_independent_v3_20261010.py',text))
    p=A/'run_stock_embedding_small512_own_training_queue_v1_20261010.py';inputs.append(p);text=p.read_text(encoding='utf8')
    for old,new in [('verify_stock_embedding_small512_restart_v1','verify_stock_embedding_small512_restart_v3'),('train_stock_embedding_small512_BF16_bank6_v1','train_stock_embedding_small512_BF16_bank6_v3'),('verify_stock_embedding_small512_small_CPU_v2','verify_stock_embedding_small512_small_CPU_v3'),('verify_stock_embedding_small512_full5_independent_v2','verify_stock_embedding_small512_full5_independent_v3')]:text=text.replace(old,new)
    text=text.replace("    fixture=Path(read(","    for p,d in read(A/'stock_embedding_E_cache_safe_runtime_admission_v3_20261010.json')['input_sha256'].items():assert sha(p)==d,p\n    fixture=Path(read(")
    outputs.append(save('run_stock_embedding_small512_own_training_queue_v3_20261010.py',text))
    create(A/'stock_embedding_E_cache_safe_runtime_admission_v3_20261010.json',{'status':'compiled_E_cache_safe_runtime_and_actual_queue_routes','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'large_artifact_drive':'E','actual_native_fits':0,'new_quality_scores':0})
if __name__=='__main__':main()

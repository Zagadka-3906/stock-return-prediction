"""Resume import admission of already-created exclusive173 sources with explicit importlib.util."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def main():
    import importlib.util
    original=A/'admit_and_activate_StockEmbedding173_actual_full_pipeline_v3_20261010.py'
    text=original.read_text(encoding='utf8')
    begin=text.index("    original=A/'verify_StockEmbedding173_full36_preflight_v2_20261010.py'")
    end=text.index('    from prepare_stock_embedding173_full_registry_sources_v2_20261010 import source_paths',begin)
    existing="    preflight=A/'verify_StockEmbedding173_full36_preflight_v3_20261010.py'\n    registration=A/'run_StockEmbedding173_full_registration_v3_20261010.py'\n    family=A/'run_StockEmbedding173_complete_family_v3_20261010.py'\n    assert all(p.is_file() for p in (preflight,registration,family))\n"
    text=text[:begin]+existing+text[end:]
    text=text.replace('stock_embedding173_actual_local_import_and_scalar_routes_admission_v3','stock_embedding173_actual_local_import_and_scalar_routes_admission_v4')
    scope={'__file__':str(Path(__file__)),'__name__':'actual_stock173_existing_source_admission'}
    exec(compile(text,str(original)+'::existing_routes','exec'),scope);scope['main']()
if __name__=='__main__':main()

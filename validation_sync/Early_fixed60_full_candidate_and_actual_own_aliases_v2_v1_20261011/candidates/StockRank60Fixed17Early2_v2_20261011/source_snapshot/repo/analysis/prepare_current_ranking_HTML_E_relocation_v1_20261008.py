from pathlib import Path
A=Path(__file__).resolve().parent
source=A/'relocate_current_ranking_JSON_byte_exact_to_E_v1_20261008.py';value=source.read_text(encoding='utf8')
value=value.replace('all_model_rankings_20261003.json','all_model_rankings_20261003.html').replace('current_mutable_rankings_v1_20261008','current_mutable_ranking_HTML_v1_20261008').replace('current_ranking_JSON_E_relocation','current_ranking_HTML_E_relocation').replace('Current complete ranking JSON','Current complete ranking HTML').replace('BF16wide40_official_comparison_v4_20261008','BF16wide40_official_comparison_v1_20261008')
needle="    source=ROOT/'results/all_model_rankings_20261003.html'";assert value.count(needle)==1
value=value.replace(needle,"    assert (A/'round144_connected_API_main_request_v1_20261008.json').exists(), 'Wait until all current HTML publication bytes are already staged and hashed'\n"+needle)
target=A/'relocate_current_ranking_HTML_byte_exact_to_E_v1_20261008.py';assert not target.exists();compile(value,str(target),'exec');target.write_text(value,encoding='utf8',newline='\n')

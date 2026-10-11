from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'analysis/verify_complete_future_branches_20261003.py'
q=ROOT/'analysis/verify_complete_future_branches_v2_20261003.py'
assert not q.exists()
text=p.read_text(encoding='utf-8').replace('complete_scheme_future_branches_qa_20261003','complete_scheme_future_branches_qa_v2_20261003')
text=text.replace('    verification=m.read',"    assert m.sha(qa/'candidate/market_regime_mapping.json')==m.sha(ROOT/'analysis/market_regime_bank_20261003/future_mapping_2025.json')\n    verification=m.read")
text=text.replace("'candidate_verification_sha256':m.sha(qa/'candidate/verification.json'),",
                  "'candidate_verification_sha256':m.sha(qa/'candidate/verification.json'),\n         'packaged_market_state_mapping_sha256':m.sha(qa/'candidate/market_regime_mapping.json'),")
ast.parse(text);q.write_text(text,encoding='utf-8',newline='\n');print(q)

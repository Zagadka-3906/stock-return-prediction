from pathlib import Path
import json,sys
assert sys.argv[1:]==["30"]
Path('D:\\3.Study\\数据分析\\赛题五\\analysis\\late_context_lazy_queue_v2_preflight_20261004\\fixture\\ran.json').write_text(json.dumps({"executed":True,"round":30}),encoding="utf-8")

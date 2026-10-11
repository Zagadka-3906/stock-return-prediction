from pathlib import Path
A=Path(__file__).resolve().parent
source=A/'monitor_actual135_144_connected_API_progress_v19_20261008.py';value=source.read_text(encoding='utf8').replace('progress_v19_20261008','progress_v20_20261008')
needle="    stages={n:status(n) for n in services};scores={}";assert value.count(needle)==1
value=value.replace(needle,"    services.extend(['CrossFamily91_current_parent_controls_v2_20261008','CrossFamily94_round136_source_admission_v5_20261008','CrossFamily94_controls_main_publication_v5_20261008','CrossFamily94_official_comparison_v5_20261008','CrossFamily94_scores_main_publication_v5_20261008'])\n"+needle)
value=value.replace("'pending136_to141_need_fresh135_gate_repair':True","'pending137_to141_need_fresh136_gate_repair':True,'actual136_fresh94_case_quality_receivers_queued_after144':True")
value=value.replace("text+='\\n'.join", "text+='第136轮30份已成熟模型、91项完整变换、273项冷启动、15项原生推理控制及24份未来接收程序检查已通过。94项官方评分等待第144轮完整榜同步结束后开始，避免发布冲突。\\n\\n'\n    text+='\\n'.join")
target=A/'monitor_actual135_144_connected_API_progress_v20_20261008.py';assert not target.exists();compile(value,str(target),'exec');target.write_text(value,encoding='utf8',newline='\n')

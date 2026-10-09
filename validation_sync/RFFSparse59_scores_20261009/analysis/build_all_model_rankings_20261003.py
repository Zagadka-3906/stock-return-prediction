"""Inventory saved experiments and scores; never train, predict or load test labels."""
from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "analysis/connected_validation_20261002"
ARCHIVE = ROOT.parent / "赛题五_历史归档_20261001"
OUT = ROOT / "results"
SOURCES: dict[str, dict] = {}
LATER_ROUNDS: dict[int, dict] = {}


def read(path: Path):
    data = path.read_bytes()
    SOURCES[str(path)] = {"path": path.as_posix(), "bytes": len(data),
                          "sha256": hashlib.sha256(data).hexdigest()}
    return json.loads(data.decode("utf-8-sig"))


def leaves(value, path=()):
    if isinstance(value, dict):
        if isinstance(value.get("connected_final_score"), (int, float)):
            yield path, value
            return
        for key, child in value.items():
            yield from leaves(child, path + (str(key),))
    elif isinstance(value, list):
        for key, child in enumerate(value):
            yield from leaves(child, path + (str(key),))


def pointer(parts):
    return "/" + "/".join(str(k).replace("~", "~0").replace("/", "~1") for k in parts)


def rank(rows):
    rows.sort(key=lambda r: (r["score"] is None, -(r["score"] or 0), r["id"]))
    previous = object()
    current = 0
    for index, row in enumerate(rows, 1):
        if row["score"] is None:
            row["rank"] = None
            continue
        if row["score"] != previous:
            current = index
        row["rank"] = current
        previous = row["score"]
    return rows


METRIC_KEYS = {"ic_mean", "annual_excess", "mean_turnover", "final_score"}


def metric_values(saved):
    m = saved.get("connected_metrics", saved.get("metrics", saved.get("full", saved)))
    return {k: m[k] for k in METRIC_KEYS if k in m}


def verify_score(row):
    m = row["metrics"]
    if row["score"] is not None and {"ic_mean", "annual_excess", "mean_turnover"} <= m.keys():
        calculated = .4*m["ic_mean"] + .3*m["annual_excess"] + .3*(1-m["mean_turnover"])
        assert math.isclose(calculated, row["score"], abs_tol=1e-11), (row["id"], calculated, row["score"])


def normalize(path, key, saved, name=None, wave=None, context=None):
    score = saved.get("connected_final_score", saved.get("final_score"))
    parameters = {k: v for k, v in saved.items()
                  if k not in {"connected_metrics", "metrics", "annual_metrics", "annual_official_metrics",
                               "connected_final_score", "annual_final_scores", "halves", "source_sha256"}}
    return {"id": path.stem + "::" + "/".join(key), "name": name or saved.get("name") or "/".join(key),
            "wave": str(wave or "1–3"), "score": score, "metrics": metric_values(saved),
            "source": path.as_posix(), "source_pointer": pointer(key),
            "parameters": parameters, "fixed_context": context or {},
            "status": "已存精确分", "known_restriction": False, "notes": []}


def connected_inventory():
    rows, counts, failures = [], [], []
    paths = [OLD / "connected_results_all.json", *sorted(OLD.glob("wave*results.json"))]
    for suffix in ["", "_r2", "_r3", "_r4", "_r5", "_r6"]:
        paths.extend(sorted((ROOT / f"analysis/optimization_20261003{suffix}").glob("wave*results.json")))
    paths.extend(sorted((ROOT / "analysis/optimization_20261003_r7").glob("wave*results.json")))
    paths.extend(sorted((ROOT / "analysis/optimization_20261003_r8").glob("wave*results.json")))
    paths.extend(sorted((ROOT / "analysis/optimization_20261003_r9").glob("wave*results.json")))
    paths.extend(sorted((ROOT / "analysis/optimization_20261003_r10").glob("wave*results.json")))
    paths.extend(sorted((ROOT / "analysis/optimization_20261003_r11").glob("wave*results.json")))
    paths.extend(sorted((ROOT / "analysis/optimization_20261003_r12").glob("wave*results.json")))
    LATER_ROUNDS.clear()
    for result_path in sorted((ROOT/'results').glob('optimization_20261003_r*.json')):
        match=re.fullmatch(r'optimization_20261003_r(\d+)',result_path.stem)
        if not match or int(match[1])<13:continue
        payload=read(result_path)
        if payload.get('status')!='complete':continue
        number=int(match[1]);LATER_ROUNDS[number]=payload
        paths.extend(ROOT/f'analysis/optimization_20261003_r{number}/wave{wave}_results.json' for wave in payload['waves'])
    provenance_erratum = ROOT / "results/validation_provenance_erratum_20261003.json"
    has_pruning_erratum = provenance_erratum.exists()
    if has_pruning_erratum:
        read(provenance_erratum)
    for path in paths:
        payload = read(path)
        assert payload.get("status") == "complete", path
        primary = "results" if "results" in payload else "variants"
        wave_match = re.match(r"wave(\d+[a-z]?)_results", path.stem)
        wave = wave_match.group(1) if wave_match else "1–3"
        context = {k: payload[k] for k in ["purpose", "donor_fixed", "orderer_fixed", "m_frac",
                                          "tie_break_eps", "promote_source"] if k in payload}
        local_rows = []
        for keys, saved in leaves(payload[primary], (primary,)):
            row = normalize(path, keys, saved, wave=wave, context=context)
            description = json.dumps([row["name"], row["parameters"]], ensure_ascii=False)
            if "transductive_self_training" in description:
                row.update(status="未来整段特征自训练：历史诊断", known_restriction=True)
                row["notes"].append("不能用于按当前禁止未来信息标准选模。")
            elif any(s in description for s in ["ensemble4_old_pruned", "W3e_rank_average"]):
                row.update(status="旧全验证期特征筛选：历史诊断", known_restriction=True)
                row["notes"].append("旧剪枝使用跨折特征重要性；fold-local 修订是另一方案。")
            if wave == "28":
                row["status"] = "已存精确分；波28并列重排勘误"
                row["notes"].append("额外1e-9代码并列重排同时变化；不能把差异仅归因于候选池宽度。")
            if has_pruning_erratum and not saved.get("fold_local_pruning_repaired"):
                ancestry = json.dumps([row["name"], parameters_without_metrics(saved), context], ensure_ascii=False).lower()
                default_w5a_wave = wave.isdigit() and int(wave) in {
                    19,22,23,24,25,26,27,28,29,31,35,36,37,38,39,*range(40,59)}
                if ("w5a" in ancestry or "w5b" in ancestry or "w8a_zscore_mean" in ancestry
                        or "w8b_trimmed_mean" in ancestry or default_w5a_wave
                        or (wave=="34" and saved.get("kind")!="sole_orderer")
                        or (wave=="32" and saved.get("kind")!="transformer_alone")):
                    row.update(status="继承旧全时期剪枝的验证依赖：历史诊断", known_restriction=True)
                    row["notes"].append("W5a/旧剪枝成员的验证特征选择非fold-local；分数保留，本轮修正版另列。")
            verify_score(row)
            local_rows.append(row)
        if isinstance(payload[primary], dict):
            for key, saved in payload[primary].items():
                if isinstance(saved, dict) and "error" in saved and "connected_final_score" not in saved:
                    failures.append({"name": key, "source": path.as_posix(), "error": saved["error"],
                                     "status": "失败，未产生可排序分数"})
        counts.append({"source": path.as_posix(), "wave": wave, "score_records": len(local_rows)})
        rows.extend(local_rows)
    prior_records = sum(r['score_records'] for r in counts if not (
        (match:=re.search(r'/optimization_20261003_r(\d+)/',r['source'])) and int(match[1])>=7))
    assert prior_records == 1156, prior_records
    assert len({r["id"] for r in rows}) == len(rows)
    rank(rows)
    ranked_comparable = rank([r.copy() for r in rows if not r["known_restriction"]])
    comparable_ranks = {r["id"]: r["rank"] for r in ranked_comparable}
    for row in rows:
        row["rank_without_known_restrictions"] = comparable_ranks.get(row["id"])
    return rows, counts, failures


def parameters_without_metrics(saved):
    return {k:v for k,v in saved.items() if k not in {"metrics","connected_metrics","annual_metrics"}}


def family_from_name(name):
    found = []
    low = name.lower()
    for text, label in [("lightgbm", "LightGBM"), ("xgboost", "XGBoost"), ("mlp", "MLP"),
                        ("gru", "GRU"), ("transformer", "Transformer"), ("ridge", "Ridge")]:
        if text in low:
            found.append(label)
    return "＋".join(found) or "集成／后处理／对照"


def historical_inventory():
    path = ARCHIVE / "analysis/all_models_test_20260929/all_results.json"
    payload = read(path)
    rows, raw_configs = [], {}
    for group in ["rows", "supplemental_rows"]:
        for index, saved in enumerate(payload[group]):
            uid = saved.get("inventory_id", saved.get("model_id"))
            status = saved.get("status")
            eligible = status in {"scored", "same_model_reference"} and "transductive_self_training" not in uid
            name = saved.get("display_name", uid)
            full = saved.get("full") or {}
            metadata = saved.get("metadata", {})
            row = {"id": uid, "name": name, "score": full.get("final_score"),
                   "metrics": {k: full[k] for k in METRIC_KEYS if k in full},
                   "wave": saved.get("scope", "补充"), "source": path.as_posix(),
                   "source_pointer": pointer((group, index)), "family": family_from_name(name),
                   "status": {"scored": "已评分", "same_model_reference": "同模型别名对照",
                              "statistic_mean": "单种子分数均值，无独立预测",
                              "scored_invalid_diagnostic": "已失败诊断",
                              "not_independent_tried_model": "未产出独立候选"}.get(status, status),
                   "known_restriction": not eligible, "archive_ranking_eligible": eligible,
                   "notes": [], "parameters": {k: v for k, v in metadata.items()
                                                if k in {"config", "family", "dependencies", "group", "candidate",
                                                         "true_training_label_row_cutoff", "refit", "constituents"}}}
            if "transductive_self_training" in uid:
                row["status"] = "未来整段特征自训练：历史诊断"
            if status == "statistic_mean":
                row["parameters"]["arithmetic_mean_of_scores"] = row["score"]
                row["score"] = None  # Not a score of any actual ensemble prediction.
            row["parameters"]["continuous_segments"] = saved.get("segments_continuous_state")
            verify_score(row)
            rows.append(row)
            for key, config in metadata.get("raw_metadata", {}).items():
                if key not in raw_configs:
                    raw_configs[key] = {"name": key, "family": config.get("model_family"),
                                       "source": path.as_posix(),
                                       "source_pointer": pointer((group, index, "metadata", "raw_metadata", key)),
                                       "features_count": len(config.get("features", [])),
                                       "training_details": {k: v for k, v in config.items() if k != "features"}}
    assert len(rows) == 396
    comparable = rank([r.copy() for r in rows if r["archive_ranking_eligible"]])
    assert len(comparable) == 370, len(comparable)
    ranks = {r["id"]: r["rank"] for r in comparable}
    for row in rows:
        row["rank"] = ranks.get(row["id"])
    rows.sort(key=lambda r: (r["rank"] is None, r["rank"] or 0, r["id"]))
    return rows, list(raw_configs.values())


def csv_disclosures():
    rows = []
    path = OLD / "official_test_period_scores.json"
    for key, saved in read(path)["results"].items():
        row = normalize(path, ("results", key), saved, name=key, wave="历史 CSV")
        row["parameters"] = {"csv_path": saved["path"]}
        if "peer67" not in key:
            row["status"] = "旧12位精度 CSV；已被17位版本替代"
        else:
            row["status"] = "历史17位精度 CSV"
        rows.append(row)
    for filename, name in [("submission_NESTED_W5A_p17_retrospective.json", "波13：nested × W5a，17位 CSV"),
                           ("submission_FINAL_v3_retrospective.json", "波15：nested × (W5a＋25% slow16)，17位 CSV")]:
        path = OLD / "final_submission" / filename
        saved = read(path)
        row = normalize(path, ("metrics",), {**saved, "final_score": saved["test_period_score"]}, name=name,
                        wave="历史 CSV")
        row["status"] = "官方脚本已评分的17位 CSV（回顾）"
        rows.append(row)
    path = ROOT / "deliveries/connected_topk0175_20261003/retrospective.json"
    saved = read(path)
    row = normalize(path, ("metrics",), {**saved, "final_score": saved["metrics"]["final_score"]},
                    name="现正式交付：TopK 17.5% 原版完整方案", wave="现正式交付")
    row["status"] = "官方脚本已评分的17位 CSV（回顾）"
    rows.append(row)
    for row in rows:
        verify_score(row)
    return rank(rows)


CATALOG = [
    ("LightGBM 回归与辅助模型", "基准秩回归；两日目标；pooled／OOF收益辅助；Huber、DART；每日等权、近期加权、3年滚动窗口；价量／市场／隔夜／日历特征；标签平滑与标准化；剪枝及fold-local修订；叶子数15/31/63、轮数与L2网格、Optuna和多种子。"),
    ("LightGBM TopK 收益加权排序", "训练目标TopK比例10%、12.5%、15%、17.5%、20%、25%、30%、40%、50%、60%；63/83特征；单种子、多种子与不同轮数检查点秩融合；学习率、叶子、采样、正则参数。评分Top组始终仍是官方前10%。"),
    ("LightGBM 学习排序", "LambdaRank、RankXendcg；80/180轮；graded、binary、topheavy标签；truncation=500变体。"),
    ("XGBoost", "63/67/83特征；同伴信号及滞后、置换负对照；8/16/32种子融合；0.025慢学习率360轮；确定性／采样／线程对照；一日、混合两日目标；可交易样本训练；早停、时间衰减、波动状态切换；NDCG和90%分位数目标；整段特征自训练诊断。"),
    ("MLP 历史记录", "隐藏维度64和128，窗口1天；统一完整后处理；历史记录的2020–2024连接验证分仅可恢复区间，年度均分与历史343日测试分另列。"),
    ("MLP 新增完整年度 OOF", "已完成原始63特征的秩／收益目标128维网络，以及64／256／512维、32／64轮扩展；新增三个当日截面分位数输入网络。每个配置均有2020–2024五折预测，过去数据拟合均值、尺度和目标裁剪，成熟标签边界检查及模型重载复放。完整方案评分按已完成轮次逐步纳入连接榜，训练完成本身不代表取得排名。"),
    ("ExtraTrees 新增完整年度 OOF", "192棵树、深度12、叶子最少128样本、特征比例0.7、bootstrap训练抽样0.25；已完成五个年度折和成熟标签检查。分别用于持仓成员、Top组、其余股票排序的集成，按完整方案连接评分。"),
    ("MLP 新增头部与成对排序损失", "已完成头部10%分类、头部加权MSE和同日RankNet三个目标的15次年度训练；128/64隐藏层、32轮；成对样本只来自同一过去训练交易日。完整评分按已完成轮次纳入，训练完成不代表入选。"),
    ("CatBoost 新增完整年度 OOF", "秩RMSE目标深度6/8、收益Huber目标深度6，均600轮；三个配置的15次年度训练、CPU小模型成熟边界对照、冻结模型的串行重载推理均通过。GPU重新训练不保证逐位确定性；只对实际冻结模型验证推理复现。完整方案按完成轮次纳入连接榜。"),
    ("MLP 新增种子与容量", "围绕已改善完整方案的512维网络，新增两个32轮种子、一个64轮版本和1024/512/256维32轮网络；四个配置的20次年度训练完成。个体模型和后续种子集成按实际完成的完整方案评分记录展示，训练完成本身不赋予排名。"),
    ("MLP 匹配 Dropout 与权重衰减", "固定512/256/128结构、原种子、32轮和训练样本，比较Dropout=0/0.15及权重衰减=0.001/0.00001，共20次年度训练完成。特征矩阵、目标和样本键与原512维基准逐位匹配；12项用途及4项独立后处理前缀检查通过。R31增量集成、R32独立主模型完成评分后纳入排名。"),
    ("MLP 种子原始均值与每日秩均值集成", "三个32轮512维模型、四个512维变体、含1024维模型的五成员集成，各比较原始均值与当日秩均值，共六种方案、30个年度集成产物。重载、完整交易日前缀和标签污染检查通过；这些是已有模型的集成，不计作30次新增训练，完成方案评分后才取得排名。"),
    ("MLP 两年与三年滚动训练窗口", "512维秩目标及256维收益目标，各用最近两年或三年成熟历史，网络、种子、32轮预算和优化器匹配扩展窗口对照，共20次年度训练完成。旧历史排除、未来标签污染及重载检查通过；首折历史相同的四项预测均与扩展窗口逐位一致，属于对照。"),
    ("RankNet 容量与排序温度", "围绕已提高完整方案得分的128维同日成对排序目标，增加256维和512维网络，以及原始128维网络的0.05/0.2温度变体。种子、32轮预算、同日成熟样本配对和MSE项固定；四个配置的20次年度训练完成，按完整输出用途集成的实际评分排名。"),
    ("GRU", "普通GRU和拼接当日特征的GRU_cat；隐藏维度64/128 × 窗口10/20天，共8个基本结构；原始输出、统一后处理、半权重融合、五模型集成及GRU特征堆叠。"),
    ("Transformer", "Tabular Transformer、共享特征编码、特征身份编码；原始与pooled完整后处理；10%神经网络融合；在嵌套TopK方案中的排序臂及融合权重测试。"),
    ("Ridge 一日原始特征主模型", "新增六个线性配置：未来一日秩与收益目标各比较三种正则强度，全部63个特征；30次年度向前训练、成熟标签边界、独立求解器、重载和前缀检查已完成。R28独立完整输出与R29增量用途集成已准备，完成方案评分后纳入排名。"),
    ("Ridge 历史样本外预测学习集成", "45个已冻结模型的当日秩作为二层输入，秩与一日收益目标各比较三种正则强度；2021–2024仅用此前成熟的年度样本外预测与标签，已完成24次二层训练。2020没有更早样本外历史，固定复用对应的原始特征Ridge，六个首年产物不计为新增拟合。五年30个预测产物、完整交易日前缀、标签污染、独立求解器和实际子模型重放通过；R33增量集成与R34独立完整方案待评分，训练完成不赋予排名。"),
    ("Ridge 历史五日校准", "五日收益校准；原始秩和平滑信号联合、仅原始、仅平滑版本。预测期限与当前未来一日收益要求不同，仅保留为历史尝试。"),
    ("跨模型集成与完整输出方案", "树模型秩均值／中位数、两日期限融合、四模型及含GRU五模型、z-score均值／trimmed mean；TopK成员与排序解耦、嵌套提升、持仓留存、涨停偏移、trailing-IC自适应、因果收益映射。此行是方案类别，不是新的模型架构。"),
]


def neural_tuning_catalog():
    bank=ROOT/'analysis/neural_tuning_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    protocol=read(bank/'protocol.json');assert len(protocol['configurations'])==5
    completed=0
    for info_path in sorted(bank.glob('*/info_20*.json')):
        if not re.fullmatch(r'info_202[0-4]\.json',info_path.name):continue
        info=read(info_path);assert info['status']=='passed';completed+=1
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and completed==25
    status='25次年度训练及成熟边界、重载和前缀检查已完成' if audit.exists() else f'已完成{completed}/25次年度训练，训练与检查仍在进行'
    return [('MLP 标签中心与学习率匹配对照',
             '固定512/256/128结构、原种子、32轮、Dropout与权重衰减，比较float32标签偏移-0.5/0与学习率0.0005/0.001/0.002。原始偏移-0.5、学习率0.001配置复用为对照，新增五种配置；'+status+'。原始训练器对照权重与预测逐位一致；两种标签偏移都是有效训练目标。R35增量集成、R36独立主模型按实际完成的官方完整方案分取得排名。')]


def catboost_tuning_catalog():
    bank=ROOT/'analysis/catboost_tuning_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    protocol=read(bank/'protocol.json');assert len(protocol['configurations'])==5
    completed=0
    for info_path in sorted(bank.glob('*/info_20*.json')):
        if not re.fullmatch(r'info_202[0-4]\.json',info_path.name):continue
        assert read(info_path)['status']=='passed';completed+=1
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and completed==25
    status='25次年度训练及成熟边界、重载和前缀检查已完成' if audit.exists() else f'已完成{completed}/25次年度训练，其余训练与检查进行中'
    return [('CatBoost 学习率预算正则与深度匹配对照',
             '固定原始63特征、一日秩目标和深度6基准种子20261013；新增学习率0.025配600/1200轮、叶子L2=1/100、深度10共五种配置。'+status+'。训练样本、特征和提供标签须与原始基准逐位匹配；固定实际GPU模型并验证串行CPU推理，GPU重新拟合的非确定性仍保留披露。R37增量用途与R38独立完整方案按实际完成的官方评分取得排名。')]


def expanded_stacking_catalog():
    bank=ROOT/'analysis/expanded_stacking_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    protocol=read(bank/'protocol.json');configs=protocol['configurations']
    assert len(configs)==12 and all(len(c['members'])==55 for c in configs.values())
    completed=actual_fits=fixed_first=paired_reuses=0
    for model in sorted(configs):
        for year in range(2020,2025):
            info_path=bank/model/f'info_{year}.json'
            if not info_path.exists():continue
            info=read(info_path);assert info['status']=='passed';completed+=1
            actual_fits+=int(info['new_model_fits'])
            fixed_first+=int(year==2020)
            paired_reuses+=int(year>2020 and configs[model]['first_fold_policy']=='uniform')
    audit=bank/'oof_audit.json'
    if audit.exists():
        assert read(audit)['status']=='passed'
        assert (completed,actual_fits,fixed_first,paired_reuses)==(60,24,12,24)
    status=(f'已完成{completed}/60个年度预测产物、{actual_fits}次实际二层拟合；'
            f'{fixed_first}个首年固定输出和{paired_reuses}个后续年度配对复用均不计为新增训练')
    return [('Ridge 扩展55模型历史样本外预测集成',
             '在原45个子模型上加入五个MLP和五个CatBoost匹配对照，使用55个冻结模型的当日秩作为二层输入。秩与一日收益目标各比较三种正则强度；2021–2024仅用此前成熟的年度样本外预测及标签。2020分别使用对应原始特征Ridge或预先固定的55模型等权秩均值；两种首年策略共12种完整输出方案，后续年度系数按目标与正则强度配对复用。'+status+'。实际子模型重放、成熟边界、标签污染、独立求解器与完整交易日前缀检查通过。R39增量用途与R40独立完整方案按实际完成的官方评分取得排名，训练完成不赋予排名。')]


def additive_ridge_catalog():
    bank=ROOT/'analysis/additive_ridge_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    protocol=read(bank/'protocol.json');assert len(protocol['configurations'])==6
    preflight=read(ROOT/'analysis/additive_ridge_preflight_20261004/verification.json')
    assert preflight['status']=='passed'
    completed=0
    for info_path in sorted(bank.glob('*/info_20*.json')):
        if not re.fullmatch(r'info_202[0-4]\.json',info_path.name):continue
        assert read(info_path)['status']=='passed';completed+=1
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and completed==30
    status=('30次年度训练、原线性模型训练样本逐位匹配、成熟边界和实际80交易日前缀检查已完成'
            if audit.exists() else f'已完成{completed}/30次年度训练，年度训练与实际前缀检查仍在进行')
    return [('固定分段基函数加性Ridge 一日主模型',
             '原63个因果字段仅用过去成熟训练样本拟合均值和尺度，截断标准化值后固定展开z及max(z-k,0)，k=-1/0/1，共252列；不使用验证期分位数选择节点。秩与一日收益目标各比较三档正则强度，收益裁剪在对应过去训练折拟合。'+status+'。独立基函数、独立求解器、重载与批次前缀检查通过。R41增量用途与R42独立完整方案按完成的官方连接评分取得排名。')]


def fourier_ridge_catalog():
    bank=ROOT/'analysis/fourier_ridge_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    protocol=read(bank/'protocol.json');assert len(protocol['configurations'])==6
    assert read(ROOT/'analysis/fourier_ridge_preflight_20261004/verification.json')['status']=='passed'
    completed=0
    for info_path in sorted(bank.glob('*/info_20*.json')):
        if not re.fullmatch(r'info_202[0-4]\.json',info_path.name):continue
        assert read(info_path)['status']=='passed';completed+=1
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and completed==30
    status=('30次年度拟合、成熟边界及实际80交易日前缀检查已完成' if audit.exists()
            else f'已完成{completed}/30次年度拟合，其余训练与实际前缀检查正在进行')
    return [('原始字段与随机傅里叶特征Ridge 一日主模型',
             '过去成熟样本拟合原63字段的均值和尺度，标准化截断后追加128个固定种子高斯投影余弦特征，共191列；投影不从特征值或标签学习。固定种子20261004、正则0.1，秩与一日收益目标各比较长度尺度0.5/1/2。'+status+'。独立RBFSampler投影和相位逐位匹配，映射与独立求解器在1e-12容差内匹配；固定填充批次的重载与前缀预测逐位一致。R43增量用途与R44独立完整方案按完成的官方连接评分取得排名。')]


def additive_basis_catalog():
    bank=ROOT/'analysis/additive_basis_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    protocol=read(bank/'protocol.json');assert len(protocol['configurations'])==12
    assert read(ROOT/'analysis/additive_basis_preflight_20261004/verification.json')['status']=='passed'
    infos=[read(p) for p in bank.glob('*/info_202[0-4].json')];assert all(v['status']=='passed' for v in infos)
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and len(infos)==60
    future=ROOT/'analysis/additive_basis_future_models_qa_20261004/verification.json'
    future_text='完整训练模型重载与未来输入前缀检查等待年度训练完成。'
    if future.exists():
        assert read(future)['status']=='passed'
        future_text='12个成熟全训练模型与1599600行原始信号重载、80日模型前缀检查通过。'
    complete=ROOT/'analysis/additive_basis_complete_scheme_preflight_20261004/verification.json'
    complete_text='完整用途融合、独立替换及候选推理实现检查仍待完成。'
    if complete.exists():
        assert read(complete)['status']=='passed' and read(complete)['new_quality_scores']==0
        complete_text='实际完整5635800行前方案与八项指标复现、12种用途对照及四种独立组合冷前缀、共享因果校准和四条1599600行候选推理检查通过；两个基线CSV逐字节复现。原检查器遗漏前方案两层配置导致的失败记录保留，版本化检查器修正后通过。'
    return [('加性Ridge 固定折点与列数匹配对照（完整方案评分待完成）',
        '固定窄折点[-.5,0,.5]生成252列，宽五折点[-2,-1,0,1,2]生成378列；同一组63字段、两个一日目标和三档正则，共12个配置。训练样本、成熟边界、过去归一化及收益裁剪均与原线性对照一致。'
        +f'实际年度训练完成{len(infos)}/60次；'+future_text+complete_text+'独立基函数、求解器及直接预测误差检查通过；初次截距浮点对照失败记录保留。R51预定196条增量用途及R52预定258条独立主模型官方连接评分记录；完成评分、冻结及实际选中候选后取得排名，原始训练和实现检查不赋予质量排名。')]


def no_dropout_seed_catalog():
    native=ROOT/'analysis/no_dropout_seed_bank_20261004'
    virtual=ROOT/'analysis/no_dropout_ensemble_bank_20261004'
    if not (native/'protocol.json').exists():return []
    n=len(list(native.glob('*/info_202[0-4].json')));v=len(list(virtual.glob('*/info_202[0-4].json')))
    for bank,count in ((native,n),(virtual,v)):
        if (bank/'oof_audit.json').exists():assert read(bank/'oof_audit.json')['status']=='passed' and count==20
    future=ROOT/'analysis/no_dropout_seed_future_models_qa_20261004/verification.json'
    complete=ROOT/'analysis/no_dropout_seed_complete_scheme_preflight_20261004/verification.json'
    future_text='未来完整模型检查仍在运行。'
    if future.exists():
        assert read(future)['status']=='passed'
        future_text='八个成熟全训练原生或集成模型的1599600行重载与80日冷前缀检查通过。'
    complete_text='完整用途融合、独立方案、共享因果校准及候选推理实现检查仍待完成。'
    if complete.exists():
        assert read(complete)['status']=='passed' and read(complete)['new_quality_scores']==0
        complete_text='完整方案复现、因果前缀、校准及候选推理实现检查通过。'
    return [('无Dropout神经种子、训练轮数与等权集成（完整方案评分待完成）',
        f'以第31轮采用的无Dropout模型为匹配对照，固定结构、目标、过去样本和预处理，比较三个新种子的32轮模型及一个配对64轮模型；复用原模型组成三成员或五成员的原始信号均值及日内秩均值。完成{n}/20次实际年度拟合和{v}/20份零新增拟合的集成年度预测。'
        +future_text+complete_text+'第53、54轮预定148及178条完整官方连接评分；实际选中方案冻结并完成候选检查后取得质量排名。')]


def neural_interaction_catalog():
    bank=ROOT/'analysis/neural_interaction_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    configs=read(bank/'protocol.json')['configurations'];assert len(configs)==4
    assert read(ROOT/'analysis/neural_interaction_preflight_20261004/verification.json')['status']=='passed'
    infos=[read(p) for p in bank.glob('*/info_202[0-4].json')]
    assert all(info['status']=='passed' for info in infos)
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and len(infos)==20
    future=ROOT/'analysis/neural_interaction_future_models_qa_20261004/verification.json'
    complete=ROOT/'analysis/neural_interaction_complete_scheme_preflight_20261004/verification.json'
    future_text='成熟全训练与未来原始信号检查等待年度训练。'
    if future.exists():
        assert read(future)['status']=='passed';future_text='四个成熟全训练模型的1599600行重载及80日冷前缀检查通过。'
    complete_text='完整用途、独立方案、因果校准及候选推理实现检查仍待完成。'
    if complete.exists():
        assert read(complete)['status']=='passed' and read(complete)['new_quality_scores']==0
        complete_text='完整方案实现、校准及候选推理检查通过。'
    return [('无Dropout与学习率、训练轮数、权重衰减的匹配组合（完整方案评分待完成）',
        f'固定原种子、结构、目标和过去训练样本，比较学习率0.0005的32轮模型、原学习率64轮模型、学习率0.0005的64轮模型和权重衰减0.001的32轮模型。实际年度训练完成{len(infos)}/20次；'+future_text+complete_text
        +'第55、56轮预定100和98条完整官方连接评分，完成评分、冻结及候选检查后取得质量排名。')]


def four_model_count_metadata_note(family):
    proof=ROOT/f'analysis/{family}_scheme_count_metadata_audit_20261004/verification.json'
    if not proof.exists():return ''
    actual=read(proof)
    assert actual['status']=='passed_with_copied_display_label_clarified'
    assert actual['actual_native_models']==actual['actual_independent_standalone_composition_cases']==4
    assert actual['actual_baseline_plus_three_role_cases_per_model']==13
    assert actual['actual_fullfuture_candidate_cases']==4 and actual['new_quality_scores']==0
    assert actual['original_frozen_sources_andproofs_retained_unchanged']
    return '独立数量复核确认4个模型、13组基准与角色对照、4组独立组合对照及4个完整候选。'


def neural_width_catalog():
    bank=ROOT/'analysis/neural_width_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    configs=read(bank/'protocol.json')['configurations']
    assert len(configs)==4 and sorted(c['hidden'][0] for c in configs.values())==[1024,2048,4096,8192]
    assert read(ROOT/'analysis/neural_width_preflight_20261004/verification.json')['status']=='passed'
    infos=[read(p) for p in bank.glob('*/info_202[0-4].json')]
    assert all(info['status']=='passed' for info in infos)
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and len(infos)==20
    future=ROOT/'analysis/neural_width_future_models_qa_20261004/verification.json'
    complete=ROOT/'analysis/neural_width_complete_scheme_preflight_20261004/verification.json'
    future_text='成熟全训练与未来原始信号检查等待年度训练。'
    if future.exists():
        assert read(future)['status']=='passed';future_text='四个成熟全训练模型的1599600行重载及80日冷前缀检查通过。'
    complete_text='完整方案实现、因果校准及候选推理检查尚待完成。'
    if complete.exists():
        assert read(complete)['status']=='passed' and read(complete)['new_quality_scores']==0
        complete_text='完整方案实现、校准及候选推理检查通过。'
    complete_text+=four_model_count_metadata_note('neural_width')
    return [('更宽无Dropout神经网络（完整方案评分待完成）',
        f'固定原种子、目标、过去训练样本、学习率、32轮训练及批量，比较1024、2048、4096、8192宽度与已选中的512宽度对照。实际年度训练完成{len(infos)}/20次；'+future_text+complete_text
        +'第57、58轮预定100和98条完整官方连接评分，完成评分、冻结及候选检查后取得质量排名。单步资源检查不代表完整训练可行性。')]


def neural_width_resource_catalog():
    proof=ROOT/'analysis/neural_width_capacity_20261004/verification.json'
    if not proof.exists():return []
    value=read(proof);assert value['status']=='passed' and value['new_quality_scores']==0
    widths=value['successful_one_step_widths']
    catalog=[('神经网络单步资源诊断（未取得完整模型质量排名）',
        '已在实际成熟训练样本上完成512、1024、2048、4096、8192、16384宽度的固定32768行单步训练；'
        +f'成功宽度记录为{widths}。16384仅有单步诊断，尚无完整年度验证与官方质量分。'
        +'单步分配峰值不等于专用显存占用，未据此认定完整训练可行性或硬件最大容量。')]
    full=ROOT/'analysis/neural_width_future_resource_scope_audit_20261004.json'
    if full.exists():
        actual=read(full)
        assert actual['status']=='passed' and actual['new_quality_scores']==0
        assert actual['actual_completed_fulltraining_models']==4 and actual['actual_future_rows']==1599600
        catalog.append(('宽网络全训练与推理资源记录（正式质量比较待完成）',
            '1024、2048、4096、8192四个宽度的成熟全训练及全量预测重载、80日冷前缀检查通过。'
            +f"本次资源采样{actual['samples']}次，最低可用内存{actual['minimum_available_ram_GiB_sampled']:.3f} GiB；"
            +f"检查进程采样RSS峰值{actual['maximum_qa_python_rss_GiB_sampled']:.3f} GiB。"
            +'观测包含其他并行任务，无法据此比较各宽度的独立资源峰值。12 GiB启动预留没有保证整个运行期间持续保有该空间；本次成功不代表硬件最大容量。'
            +'这些记录不增加官方质量评分，完整方案比较由第57、58轮完成。'))
    plan=ROOT/'analysis/neural_width_frontier_prepared_plan_20261004.json'
    if plan.exists():
        frozen=read(plan);assert frozen['new_quality_scores']==0
        frontier=ROOT/'analysis/neural_width_frontier_20261004/verification.json'
        text='16384重复对照及32768、65536宽度对照已冻结，等待第60轮完成；尚无新增单步结果。'
        if frontier.exists():
            actual=read(frontier);assert actual['status'] in ('passed','failed') and actual['new_quality_scores']==0
            text=f"实际资源执行状态：{actual['status']}；成功单步宽度：{actual['successful_one_step_widths']}；实际CUDA内存分配异常宽度：{actual['actual_CUDA_OOM_widths']}；未尝试宽度：{actual['unattempted_widths']}。"
            qualified=[{'width':r['width'],'status':r['status'],'stop_reason':r.get('stop_reason')} for r in actual['execution_controls'] if r['status']!='completed']
            if qualified:text+=f'未完成对照记录：{qualified}。'
        audit=ROOT/'analysis/neural_width_frontier_scope_audit_20261004.json'
        text+='实际批次与资源记录验收已通过。' if audit.exists() and read(audit)['status']=='passed' else '实际批次与资源记录验收尚待完成。'
        catalog.append(('扩大宽度的资源边界对照（不计入质量排名）',text+'内存保护与超时属于执行规则；单步结果不代表完整年度训练或全局硬件极限。'))
    plan=ROOT/'analysis/official_worker_frontier_prepared_plan_20261004.json'
    if plan.exists():
        frozen=read(plan);assert frozen['new_quality_scores']==0
        execution=ROOT/'analysis/official_worker_frontier_execution_20261004/verification.json'
        text='8、10、12、16个评分进程的正反顺序对照已冻结，等待模型和GPU任务完成。'
        if execution.exists():
            actual=read(execution);assert actual['status']=='passed' and actual['new_quality_scores']==0
            details=[]
            for block in actual['actual_control_blocks']:
                proof=read(Path(block['source']))
                details.extend({'block':block['block'],'workers':r['workers'],'status':r['status'],'completed_jobs':r.get('jobs_completed',0)} for r in proof['execution_controls'])
            text=f'实际执行记录：{details}。'
        audit=ROOT/'analysis/official_worker_frontier_scope_audit_20261004.json'
        text+='所有实际完成作业的八项指标与同一冻结训练CSV一致。' if audit.exists() and read(audit)['status']=='passed' else '逐作业指标与资源验收尚待完成。'
        catalog.append(('官方评分进程容量对照（不计入质量排名）',text+'只对完成的对照计算吞吐；未启动、中止和完成分别记录，不据此判定全局硬件最大容量。'))
    return catalog


def portfolio_surrogate_catalog():
    plan=ROOT/'analysis/portfolio_surrogate_complete_output_search_plan_20261004.json'
    if not plan.exists():return []
    configs=read(plan)['model_configurations'];assert len(configs)==4
    assert read(ROOT/'analysis/portfolio_bank_implementation_preflight_20261004/verification.json')['status']=='passed'
    bank=ROOT/'analysis/portfolio_surrogate_bank_20261004'
    infos=[read(p) for p in bank.glob('*/info_202[0-4].json')]
    assert all(info['status']=='passed' and info['new_model_fits']==1 for info in infos)
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and len(infos)==20
    future=ROOT/'analysis/portfolio_surrogate_future_models_qa_20261004/verification.json'
    complete=ROOT/'analysis/portfolio_surrogate_complete_scheme_preflight_20261004/verification.json'
    future_text='成熟全训练模型及未来信号检查尚待完成。'
    if future.exists():
        assert read(future)['status']=='passed';future_text='四个成熟全训练模型的1599600行重载及80日冷前缀检查通过。'
    complete_text='完整方案、因果校准及候选推理检查尚待完成。'
    if complete.exists():
        assert read(complete)['status']=='passed';complete_text='完整方案、因果校准及候选推理检查通过。'
    complete_text+=four_model_count_metadata_note('portfolio_surrogate')
    recovery=ROOT/'analysis/portfolio_surrogate_complete_scheme_recovery_20261005/verification.json'
    if recovery.exists():
        recovered=read(recovery)
        assert recovered['status']=='passed' and recovered['actual_corrected_future_cases']==2
        assert recovered['new_model_fits']==0 and recovered['new_quality_scores']==0
        complete_text+='两个未来推理检查经独立修复后通过，原失败与已通过记录保留；修复未重训或新增质量评分。'
    resource_text=''
    resources=ROOT/'analysis/portfolio_surrogate_resource_scope_audit_20261004.json'
    if resources.exists():
        measured=read(resources)
        assert measured['status']=='passed' and measured['actual_completed_annual_fits']==20
        resource_text=(f"年度微调与启动等待窗口已完成{measured['samples']}次资源采样，最低可用内存{measured['minimum_available_ram_GiB_sampled']:.3f} GiB。"
            +'观测包含其他任务；14 GiB启动条件不保证持续空闲内存，也不构成硬件极限。')
    full_infos=[read(p) for p in bank.glob('*/info_2025.json')]
    assert all(info['status']=='passed' for info in full_infos)
    future_resources=ROOT/'analysis/portfolio_surrogate_future_resource_scope_audit_20261004.json'
    if future_resources.exists():
        measured=read(future_resources)
        assert measured['status']=='passed' and measured['actual_completed_fulltraining_models']==4
        resource_text+=(f"四模型全训练与推理窗口另采样{measured['samples']}次，最低可用内存{measured['minimum_available_ram_GiB_sampled']:.3f} GiB，单个检查进程峰值RSS {measured['maximum_qa_python_rss_GiB_sampled']:.3f} GiB。"
            +'采样包含并行评分任务，不能据此推断独立模型资源峰值或物理极限。')
    return [('收益与持仓重合度损失微调模型（完整方案评分待完成）',
        '复用各年度过去训练的512宽度模型和归一化参数；比较秩与收益训练损失、加入持仓重合度的训练损失、两档平滑温度及4/8轮微调。'
        +f'实际年度微调完成{len(infos)}/20次，全训练模型完成{len(full_infos)}/4个；原模型预训练复用不计为新增拟合。'+future_text+complete_text+resource_text
        +'第59、60轮预定100和98条完整官方评分。训练损失代理值不作为官方得分或质量排名。')]


def nystrom_ridge_catalog():
    plan=ROOT/'analysis/nystrom_ridge_complete_output_search_plan_20261004.json'
    if not plan.exists():return []
    configs=read(plan)['model_configurations'];assert len(configs)==4
    proof=read(ROOT/'analysis/nystrom_ridge_preflight_20261004/verification.json')
    assert proof['status']=='passed' and proof['actual_annual_fits']==0
    assert read(ROOT/'analysis/nystrom_ridge_search_generator_preflight_20261004/verification.json')['status']=='passed'
    assert read(ROOT/'analysis/nystrom_ridge_frozen_provenance_preflight_20261004/verification.json')['status']=='passed'
    correction=read(ROOT/'analysis/nystrom_ridge_complete_scheme_source_correction_audit_20261004.json')
    assert correction['status']=='passed_pre_execution_source_correction_audit'
    bank=ROOT/'analysis/nystrom_ridge_bank_20261004'
    infos=[read(p) for p in bank.glob('*/info_202[0-4].json')]
    assert all(info['status']=='passed' and info['new_model_fits']==1 for info in infos)
    future=ROOT/'analysis/nystrom_ridge_future_models_qa_20261004/verification.json'
    complete=ROOT/'analysis/nystrom_ridge_complete_scheme_preflight_20261004/verification.json'
    future_text='成熟全训练模型与未来原始预测检查尚待完成。'
    if future.exists():
        assert read(future)['status']=='passed';future_text='四个成熟全训练模型的1599600行重载与80日冷前缀检查通过。'
    complete_text='完整方案、因果校准及候选文件检查尚待完成。'
    if complete.exists():
        assert read(complete)['status']=='passed';complete_text='完整方案、因果校准及候选文件检查通过。'
    complete_text+=four_model_count_metadata_note('nystrom_ridge')
    return [('过去训练样本的Nyström核近似岭回归（完整方案评分待完成）',
        '在各年度成熟过去样本中选择64或128个核基点；分别拟合秩和一天收益率标签，固定RBF尺度、核权重及岭惩罚，追加到原63特征。'
        +f'四配置的数值、前缀、重载与未来标签污染预检通过；实际年度拟合完成{len(infos)}/20次。'
        +future_text+complete_text+'第61、62轮预定100和98条完整输出方案评分；预检不作为官方质量分。')]


def nonlinear_stacking_catalog():
    bank=ROOT/'analysis/nonlinear_stacking_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    configs=read(bank/'protocol.json')['configurations']
    assert len(configs)==12 and all(len(c['members'])==67 for c in configs.values())
    assert read(ROOT/'analysis/nonlinear_stacking_preflight_20261004/verification.json')['status']=='passed'
    infos=[read(p) for p in bank.glob('*/info_202[0-4].json')]
    assert all(info['status']=='passed' for info in infos)
    fitted=sum(info['new_model_fits'] for info in infos)
    audit=bank/'oof_audit.json'
    if audit.exists():
        assert read(audit)['status']=='passed' and len(infos)==60 and fitted==24
        checks='67个实际子模型的五年重放、成熟标签边界、重载及完整交易日前缀检查已通过'
    else:checks='年度拟合和实际子模型重放检查正在进行'
    return [('Ridge 扩展67模型历史样本外预测集成',
        '将55成员集成的输入扩展到67个冻结原始及虚拟模型，加入六个加性Ridge和六个随机傅里叶Ridge；只对过去成熟年度OOF预测拟合集成权重。秩及一日收益目标各三档正则强度；首年采用固定原始特征Ridge或预定67成员等权日内秩，后续年度拟合按两种首年策略配对复用。'
        +f'已完成{len(infos)}/60个年度预测产物和{fitted}/24次实际集成拟合；'+checks+'。R45增量用途和R46独立主模型取得完整官方连接分后进入排名。')]


def fourier_tuning_catalog():
    bank=ROOT/'analysis/fourier_tuning_bank_20261004'
    if not (bank/'protocol.json').exists():return []
    configs=read(bank/'protocol.json')['configurations'];assert len(configs)==10
    preflight=read(ROOT/'analysis/fourier_tuning_preflight_20261004/verification.json');assert preflight['status']=='passed'
    infos=[read(p) for p in bank.glob('*/info_202[0-4].json')];assert all(v['status']=='passed' for v in infos)
    audit=bank/'oof_audit.json'
    if audit.exists():assert read(audit)['status']=='passed' and len(infos)==50
    future=ROOT/'analysis/fourier_tuning_future_pipelines_qa_20261004/verification.json'
    future_text='完整候选推理实现检查尚在运行。'
    if future.exists():
        assert read(future)['status']=='passed'
        future_text='增量用途和独立主模型两条1599600行完整推理、575列便携模型及真实80日前缀检查已通过。'
    scope=ROOT/'analysis/fourier_tuning_resource_scope_audit_20261004.json'
    if scope.exists():assert read(scope)['status']=='passed'
    return [('傅里叶Ridge 容量正则与种子匹配对照',
        '保持原63个字段和长度尺度1，追加256/512随机傅里叶特征时将傅里叶分量总尺度固定为128；另外分别测试128维正则0.001/1和第二种子20261005，秩及一日收益各五种新配置。'
        +f'已完成{len(infos)}/50次年度拟合；独立RBFSampler及求解器、重载、批次前缀和原128维基准逐位一致检查通过。'+future_text+'R47增量用途与R48独立完整方案在完成官方连续验证评分后进入榜单。')]


def temporal_output_catalog():
    proof=ROOT/'analysis/final_temporal_context_preflight_20261004/verification.json'
    if not proof.exists():return []
    assert read(proof)['status']=='passed'
    return [('最终完整排序的因果平滑与曲率对照',
        '在完整模型、融合与持仓排序之后，对当日有效股票的最终日内秩进行幂变换及逐股因果EMA，再与当日值融合；状态跨年度持续，价格无效行保留原预测。独立标量实现、完整5635800行日期前缀、未来新增股票代码、1599600行候选和原基准八项官方指标检查通过。R49预定96条评分记录；收益映射随实际完整候选在过去成熟OOF中拟合，参数不使用测试标签选择。')]


def joint_layer_replay_catalog():
    proofs=[ROOT/'analysis/role_layer_replay_preflight_20261004/verification.json',
            ROOT/'analysis/role_layer_future_replay_qa_20261004/verification.json',
            ROOT/'analysis/selected_scheme_graph_preflight_v2_20261004/verification.json']
    if not all(path.exists() for path in proofs):return []
    for path in proofs:assert read(path)['status']=='passed'
    read(ROOT/'analysis/selected_scheme_graph_preflight_recovery_20261004.json')
    return [('后续全层联合重调的逐层回放准备',
        '逐层重算模块对照11个历史用途融合实现，通过5635800行单层与连续三层冷前缀检查，并用真实冻结模型逐字节复现1599600行R25候选CSV。方案编译器保留各层自己的历史留存与涨停偏移，独立主模型替换时清除旧分支。独立检查器曾因浮点常量对照失败，原记录保留，版本化修正后通过；预测算法未改。尚待R30—R49实际方案完成后组装完整来源图并作联合评分，因此本项没有新增模型训练或可排名分数。')]


def whole_scheme_runtime_catalog():
    proofs=[ROOT/'analysis/whole_scheme_runtime_preflight_20261004/verification.json',
            ROOT/'analysis/whole_scheme_future_runtime_qa_20261004/verification.json']
    if not all(path.exists() for path in proofs):return []
    for path in proofs:assert read(path)['status']=='passed'
    return [('完整方案联合重调引擎：实现检查完成，正式评分待前序方案',
        '完整5635800行验证重算逐元素复现R18、R24、R25、R26；修改较早模型权重后，所有后续层随之重新计算并通过独立对照。冻结模型实际重载后，完整1599600行未来CSV逐字节复现历史方案，并通过80日冷前缀。R50预设独立权重、正向与逆向逐层重调、各层留存和最终平滑五阶段，等待R30—R49真实选中方案；实现对照没有新增可排名质量分数。')]


def representatives(rows):
    selected = []

    def choose(label, match):
        candidates = [r for r in rows if match(r)]
        assert candidates, label
        result = max(candidates, key=lambda r: r["score"]).copy()
        result["name"] = label
        result["parameters"] = {"original_name": result["id"], **result["parameters"]}
        selected.append(result)

    for number,payload in sorted(LATER_ROUNDS.items(),reverse=True):
        choose(payload['round_label']+f'（R{number}）',lambda r,n=number:f'/optimization_20261003_r{n}/' in r['source'])

    if any(r["wave"] in ("77","78","79","80") for r in rows):
        choose("独立持仓排序器＋融合与TopK细调（R12）", lambda r:r["wave"] in ("77","78","79","80"))
    if any(r["wave"] in ("71","72","73","74","75","76") for r in rows):
        choose("模型权重、排序、留存和持仓融合搜索（R11）", lambda r:r["wave"] in ("71","72","73","74","75","76"))
    if any(r["wave"] in ("68","69","70") for r in rows):
        choose("留存优先级搜索：原规则胜出（R10）", lambda r:r["wave"] in ("68","69","70"))
    if any(r["wave"] in ("65","66","67") for r in rows):
        choose("Top与其余股票独立排序＋留存细调（R9）", lambda r:r["wave"] in ("65","66","67"))
    if any(r["wave"] in ("62","63","64") for r in rows):
        choose("无剪枝成员加权＋TopK细调（R8）", lambda r:r["wave"] in ("62","63","64"))
    if any(r["wave"] in ("59","60","61") for r in rows):
        choose("无剪枝四模型集成＋分组排序（R7）", lambda r:r["wave"] in ("59","60","61"))

    choose("TopK 90/180轮融合＋成员重排细调（R6）", lambda r: 56 <= int(r["wave"]) <= 58 if r["wave"].isdigit() else False)
    choose("TopK 90/180轮融合＋后处理细调（R5）", lambda r: r["wave"] in ["53", "54", "55"])
    choose("TopK 90/180轮融合＋后处理细调（R4）", lambda r: r["wave"] in ["50", "51", "52"])
    choose("TopK 90/180轮融合（R3）", lambda r: r["wave"] in ["47", "48", "49"])
    choose("TopK单检查点最佳：17.5%、105轮（完整方案）",
           lambda r: r["parameters"].get("recipe", {}).get("type") == "model")
    choose("TopK 单检查点／训练参数搜索（R2）", lambda r: r["wave"] in ["44", "45", "46"])
    choose("TopK 17.5%原版＋涨停偏移（R1）", lambda r: r["wave"] in ["40", "41", "42", "43"])
    choose("TopK 17.5%原版完整方案（正式交付所选）", lambda r: r["wave"] == "36" and r["name"] == "results/frac0.175")
    choose("TopK 20%完整方案", lambda r: r["wave"] == "31" and r["name"] == "results/frac0.20")
    choose("TopK 25%完整方案", lambda r: r["wave"] == "31" and r["name"] == "results/frac0.25")
    choose("嵌套TopK＋W5a／slow16完整方案", lambda r: r["wave"] == "15")
    choose("83特征TopK完整方案", lambda r: r["wave"] == "39" and "ext83" in r["name"])
    choose("TopK＋LambdaRank（graded、trunc500）完整方案", lambda r: r["wave"] == "37" and "lambdarank_graded_trunc500" in r["name"])
    base = [r for r in rows if r["wave"] == "1–3" and not r["known_restriction"]]
    for row in base:
        copy = row.copy()
        key = row["name"].removeprefix("results/")
        copy["name"] = BASIC_NAMES.get(key, key)
        selected.append(copy)
    choose("嵌套TopK＋Transformer单独排序臂（非独立Transformer）", lambda r: r["wave"] == "32" and "T-alone" in r["name"])
    rank(selected)
    valid_ranks={r["id"]:r["rank"] for r in rank([r.copy() for r in selected if not r["known_restriction"]])}
    for row in selected:
        row["rank_without_known_restrictions"]=valid_ranks.get(row["id"])
    return selected


BASIC_NAMES = {
    "peer67_slow16": "XGBoost 67同伴特征＋慢学习率×16种子（完整后处理）",
    "peer67_slow8": "XGBoost 67同伴特征＋慢学习率×8种子（完整后处理）",
    "slow_only8": "XGBoost 63特征＋慢学习率×8种子（完整后处理）",
    "base63_8": "XGBoost 63特征×8种子（完整后处理）",
    "topk": "早期LightGBM TopK 10%（独立主干＋完整后处理）",
    "hybrid": "早期TopK成员＋XGBoost排序混合完整方案",
    "top2_lightgbm": "LightGBM Top2主干（完整后处理）",
    "ensemble4_r4": "四模型集成（fold-local特征筛选修订）",
    "pooled_rms25": "LightGBM基准＋pooled收益辅助25%",
    "xgboost_single_seed2026": "XGBoost 单种子2026（完整后处理）",
    "xgb_two_mean": "XGBoost一日＋LightGBM两日目标（完整后处理）",
    "slow8_monthly": "XGBoost慢学习率8种子＋月度模型更新",
    "W11b_early_stop": "XGBoost早停（完整后处理）",
    "W12c_trailing_ic_two": "XGBoost一日＋LightGBM两日，过去20日IC自适应",
    "W5a_five_way_with_gru__final_sweep_eval": "含GRU五模型秩均值集成（完整后处理）",
    "W5b_gru_half_weight__final_sweep_eval": "含GRU半权重集成（完整后处理）",
    "W6a_daily_rank_features__final_sweep_eval": "LightGBM日内秩特征（完整后处理）",
    "W6b_daily_zscore_features__final_sweep_eval": "LightGBM日内z-score特征（完整后处理）",
    "W8a_zscore_mean__final_sweep_eval": "四模型z-score均值集成（完整后处理）",
    "W8b_trimmed_mean__final_sweep_eval": "四模型trimmed mean集成（完整后处理）",
    "raw__wave14_seed_average_20260927": "XGBoost种子秩均值（波14，完整后处理）",
    "raw__wave16_seed_curve_20260928": "XGBoost种子数量曲线（波16，完整后处理）",
    "raw_regime_switch_std20_high__wave19_three_axes_20260928": "XGBoost 20日波动状态切换，高波动臂",
    "raw_regime_switch_std20_low__wave19_three_axes_20260928": "XGBoost 20日波动状态切换，低波动臂",
    "raw_deployed67_slow__wave23_validation_20260928": "XGBoost同伴67特征慢学习率（slow16别名）",
    "raw_lr0025_rounds360__wave19_three_axes_20260928": "XGBoost 63特征lr0.025×360轮（slow8别名）",
    "raw_base63_plus_lags__wave21_peer_lags_20260928": "XGBoost 63特征＋滞后特征",
    "raw_peer67_lr0025_360__wave22_additivity_20260928": "XGBoost 67同伴特征＋lr0.025×360轮（波22）",
    "raw_blended_two_day_target__wave17_last_axes_20260928": "XGBoost混合两日训练目标",
    "raw_control63__wave23_validation_20260928": "XGBoost 63特征对照（波23）",
    "raw_base63_plus_peer__wave21_peer_lags_20260928": "XGBoost 63特征＋同伴信号",
    "raw_extended83__wave15_paired_features_20260927": "XGBoost扩展83特征",
    "raw_placebo67_slow__wave23_validation_20260928": "XGBoost 67特征同伴信号置换负对照",
    "raw_deterministic_100_100__wave18_deterministic_20260928": "XGBoost全行列采样确定性对照",
    "raw_tradable_only_rank_label__wave19_three_axes_20260928": "XGBoost只用可交易样本训练秩标签",
}
for _key in ["raw_base63__wave21_peer_lags_20260928", "raw_base63__wave22_additivity_20260928",
             "raw_base63_one_day__wave17_last_axes_20260928", "raw_base63_one_day__wave19_three_axes_20260928"]:
    BASIC_NAMES[_key] = "XGBoost 63特征一日基准（单种子别名对照）"


PAGE = r'''<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>全部尝试模型与排名 · 赛题五</title>
<style>
:root{font-family:system-ui,"Microsoft YaHei",sans-serif;color:#17233b;background:#f3f5fa}body{margin:0}main{max-width:1480px;margin:auto;padding:32px}h1{font-size:30px;margin:0 0 12px}p{line-height:1.7;margin:10px 0}.muted{color:#58657b}.stats{display:flex;gap:14px;flex-wrap:wrap;margin:22px 0}.stat{background:white;border:1px solid #e0e5ef;border-radius:12px;padding:16px 22px;min-width:180px}.stat b{display:block;font-size:28px;color:#163f93}.catalog{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:12px}.catalog article{background:white;border:1px solid #e0e5ef;border-radius:10px;padding:12px 17px}.catalog b{font-size:15px}.catalog p{font-size:13px}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:25px 0 12px}button,select,input{font:inherit;border:1px solid #ced6e5;background:white;border-radius:7px;padding:8px 12px}button{cursor:pointer}button.active{background:#163f93;color:white;border-color:#163f93}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:16px 0}input[type=search]{flex:1;min-width:240px}input[type=checkbox]{accent-color:#163f93}.table-wrap{overflow:auto;border:1px solid #dce3ef;border-radius:10px;background:white}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:11px 12px;border-bottom:1px solid #e8ecf3;vertical-align:top}th{background:#eaf0fa;white-space:nowrap}th button{border:0;background:transparent;padding:0;font-weight:600}td.num{font-variant-numeric:tabular-nums;white-space:nowrap}.name{min-width:280px;max-width:560px;overflow-wrap:anywhere}td small{display:block;color:#68758b;margin-top:5px}tr:hover{background:#f7f9fe}.first{background:#eff6ff}.restricted{color:#9f4922}.pager{display:flex;gap:12px;align-items:center;margin:16px 0}details{background:white;border:1px solid #dce3ef;border-radius:10px;padding:14px 18px;margin-top:22px}summary{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:60vh;overflow:auto;font:12px ui-monospace,Consolas,monospace}dialog{width:min(850px,88vw);border:1px solid #c7d2e5;border-radius:14px;box-shadow:0 15px 65px #17233b33}dialog::backdrop{background:#17233b55}a{color:#174792}@media(max-width:600px){main{padding:16px}h1{font-size:24px}.stat{min-width:130px}}
</style>
<main>
<h1>全部尝试模型与排名</h1>
<p class="muted">截至 __REPORT_DATE__ · 从已保存实验和评分文件汇总 · 排名对象是完整预测方案，含集成、后处理和重复对照。</p>
__PROVENANCE_BANNER__
<div class="stats"><div class="stat"><b>__VALIDATION_BEST__</b>排除已知限制后的连接验证最高分</div><div class="stat"><b>__CONNECTED_COUNT__</b>连接验证精确评分记录</div><div class="stat"><b>396</b>历史配置与预测清单记录</div><div class="stat"><b>0.417099224</b>已有CSV最高回顾测试分</div></div>
<p>主榜采用 2020–2024 年逐年向前验证，连接 1,212 个交易日，按 <b>S = 0.4 × Rank IC + 0.3 × 年化超额收益 + 0.3 × (1 − 平均换手)</b> 降序排列。训练目标 TopK 的比例变化不改变官方评分 Top 组前10%的定义。</p>
<p>历史测试清单、已写 CSV 测试分和年度等权均分分别展示。它们不能与主验证榜直接混排，也不能据此继续选模。主榜标记已知未来信息和旧剪枝限制；未逐项重新审计所有历史方案。相同分数并列，保留每一条来源记录；评分记录数不是独立模型数。</p>
<div class="catalog" id="catalog"></div>
<nav class="tabs" id="tabs"></nav>
<p id="description"></p>
<div class="controls"><input type="search" id="search" placeholder="搜索模型、种子、参数、波次或来源"><label><input type="checkbox" id="hide" checked> 隐藏已知受限／未产出记录</label><select id="pageSize"><option>100</option><option>250</option><option value="10000">全部</option></select></div>
<p id="count" class="muted"></p>
<div class="table-wrap"><table><thead><tr><th>分序</th><th>模型／完整方案</th><th><button id="sort">综合分 ↓</button></th><th>Rank IC</th><th>年化超额</th><th>平均换手</th><th>状态／来源</th></tr></thead><tbody id="body"></tbody></table></div>
<div class="pager"><button id="prev">上一页</button><span id="page"></span><button id="next">下一页</button></div>
<details><summary>清单覆盖、勘误和证据说明</summary><div id="evidence"></div></details>
<dialog id="detail"><button id="close">关闭</button><h3 id="detailTitle"></h3><a id="sourceLink">打开原始记录文件</a><pre id="detailText"></pre></dialog>
<p class="muted">每行点击“详情”可查看原始参数与源文件 JSON 定位。完整机器可读证据：<a href="all_model_rankings_20261003.json">all_model_rankings_20261003.json</a></p>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const report=JSON.parse(document.getElementById('data').textContent);
const views=[
 ['representative','主要路线对照','覆盖主要完整方案和独立主干的代表表。各行完整后处理不同；这不是对模型架构本身的因果比较。'],
 ['connected','全部连接验证','全部已存精确评分，含重复对照；分序按原始精确值竞争排名。隐藏受限记录时显示剔除已知限制后的分序。'],
 ['mlp_bounds','MLP验证区间','缺少四个年度边界换手观测，无法恢复唯一连接分。区间重叠，不能强行排列两者；分序区间将另一MLP的不确定位置计入。'],
 ['historical','历史全部配置／测试','2025-01-02 至 2026-06-05，343日历史重建帧。共396条清单，370条按原归档规则可排名，含别名和补充输出。历史筛选、预测期限等问题见参数与状态；此榜不提供当前提交资格。'],
 ['csv_test','已写CSV官方回顾分','官方evaluate.py已保存的7次实际CSV评分，343个有评分交易日。旧12位精度CSV出现并列塌缩，分数与17位重建文件不同；以实际文件为准。'],
 ['legacy_annual','旧年度均分','2020–2024五个年度等权、每年冷启动的诊断分。连接验证采用连续年度换手，不能直接混排。']
];
let current='representative',page=1,descending=true;
const $=id=>document.getElementById(id);
const create=(tag,text)=>{const e=document.createElement(tag);e.textContent=text;return e};
report.catalog.forEach(([name,text])=>{const e=document.createElement('article');e.append(create('b',name),create('p',text));$('catalog').append(e)});
views.forEach(([id,title])=>{const b=create('button',title);b.dataset.id=id;b.onclick=()=>{current=id;page=1;descending=true;render()};$('tabs').append(b)});
const number=n=>typeof n==='number'?n.toFixed(9):'—';
function render(){
 document.querySelectorAll('#tabs button').forEach(b=>b.classList.toggle('active',b.dataset.id===current));
 $('description').textContent=views.find(v=>v[0]===current)[2];
 const q=$('search').value.toLowerCase().trim(),hide=$('hide').checked;
 let rows=report[current].filter(r=>(!hide||!r.known_restriction)&&(!q||JSON.stringify(r).toLowerCase().includes(q)));
 rows.sort((a,b)=>{const x=a.score??a.upper,y=b.score??b.upper;if(x==null)return y==null?a.id.localeCompare(b.id):1;if(y==null)return -1;return (descending?y-x:x-y)||a.id.localeCompare(b.id)});
 const size=Number($('pageSize').value),pages=Math.max(1,Math.ceil(rows.length/size));page=Math.min(page,pages);
 $('count').textContent=`当前显示 ${rows.length.toLocaleString()} 条；此清单共 ${report[current].length.toLocaleString()} 条。`;
 $('body').replaceChildren();
 for(const r of rows.slice((page-1)*size,page*size)){
  const tr=document.createElement('tr');if(r.rank===1)tr.classList.add('first');if(r.known_restriction)tr.classList.add('restricted');
  let rankValue=r.rank;
  if((current==='connected'||current==='representative')&&hide)rankValue=r.rank_without_known_restrictions;
  const rankText=current==='mlp_bounds'?`${r.rank_lower}–${r.rank_upper}`:(rankValue??'—');
  tr.append(create('td',rankText));
  const n=create('td',r.name);n.className='name';n.append(create('small',r.id));tr.append(n);
  const score=create('td',r.lower!=null?`${number(r.lower)} ～ ${number(r.upper)}`:number(r.score));score.className='num';tr.append(score);
  for(const key of ['ic_mean','annual_excess','mean_turnover']){const td=create('td',number(r.metrics?.[key]));td.className='num';tr.append(td)}
  const last=create('td',r.status??'已存分数');last.append(create('small',`波次／组别：${r.wave??'—'}`));
  const b=create('button','详情');b.onclick=()=>{ $('detailTitle').textContent=r.name;$('detailText').textContent=JSON.stringify(r,null,2);$('sourceLink').href='file:///'+encodeURI(r.source.replaceAll('\\','/'));$('detail').showModal()};last.append(b);tr.append(last);$('body').append(tr);
 }
 $('page').textContent=`第 ${page} / ${pages} 页`;$('prev').disabled=page<=1;$('next').disabled=page>=pages;
 $('sort').textContent='综合分 '+(descending?'↓':'↑');
}
['search','hide','pageSize'].forEach(id=>$(id).addEventListener('input',()=>{page=1;render()}));
$('sort').onclick=()=>{descending=!descending;page=1;render()};$('prev').onclick=()=>{page--;render()};$('next').onclick=()=>{page++;render()};$('close').onclick=()=>$('detail').close();
for(const note of report.notes)$('evidence').append(create('p',note));
render();
</script></html>'''


def main():
    SOURCES.clear()
    connected, counts, failures = connected_inventory()
    historical, raw_configs = historical_inventory()
    bound_path = OLD / "mlp_connected_bound.json"
    bounds = []
    comparable = [r for r in connected if not r["known_restriction"]]
    for key, saved in read(bound_path)["arms"].items():
        lo, hi = saved["connected_score_lower"], saved["connected_score_upper"]
        bounds.append({"id": key, "name": key.upper(), "score": None, "lower": lo, "upper": hi,
                       "rank_lower": 1 + sum(r["score"] > hi for r in comparable),
                       "rank_upper": 2 + sum(r["score"] >= lo for r in comparable),
                       "metrics": {"ic_mean": saved["ic_mean_connected_exact"],
                                   "annual_excess": saved["annual_excess_connected_exact"]},
                       "status": "边界换手缺失；仅区间", "wave": "2020–2024",
                       "source": bound_path.as_posix(), "source_pointer": pointer(("arms", key)),
                       "parameters": saved, "known_restriction": False})
    legacy_path = ROOT / "results/model_comparison.json"
    legacy = []
    for i, saved in enumerate(read(legacy_path)["records"]):
        legacy.append({"id": saved["model_id"], "name": saved["label"], "score": saved["mean_2020_2024"],
                       "metrics": {}, "status": "年度等权诊断", "source": legacy_path.as_posix(),
                       "source_pointer": pointer(("records", i)), "parameters": saved, "known_restriction": False})
    for row in bounds:
        legacy.append({**row, "score": row["parameters"]["five_year_equal_weight_mean"],
                       "name": row["name"] + "（年度均分）", "lower": None, "upper": None,
                       "status": "年度等权诊断"})
    rank(legacy)
    csv_test = csv_disclosures()
    old_sum = sum(r["score_records"] for r in counts if "/connected_validation_20261002/" in r["source"])
    assert old_sum == 907
    old_rank_path = ROOT / "results/connected_all_model_ranking_20261003.json"
    old_count = read(old_rank_path)["scored_records"]
    assert old_count == 744
    read(OLD / "wave28_erratum_001.json")
    read(OLD / "wave21_erratum_001.json")
    missing = read(OLD / "connected_results_all.json").get("unscoreable", {})
    report = {
        "generated_at_local": datetime.now().astimezone().isoformat(timespec="seconds"),
        "method": "Read existing saved scores only. No training, predictions, test labels, or new test evaluation.",
        "ranking_rule": "Descending official composite; exact float ties use competition rank. Preserve repeats and aliases.",
        "selection_standard": (ROOT / "后续选模标准.md").as_posix(),
        "connected_period": "2020–2024; 1212 days; 5635800 rows; continuous year-boundary turnover",
        "summary": {"connected_exact_records": len(connected), "old_records_full_recursive": old_sum,
                    "old_flat_ranking_count": old_count, "previously_omitted_records": old_sum-old_count,
                    "recent_wave40_58_records": 249,
                    "repaired_wave59_61_records": sum(r["score_records"] for r in counts if "/optimization_20261003_r7/" in r["source"]),
                    "weighted_wave62_64_records": sum(r["score_records"] for r in counts if "/optimization_20261003_r8/" in r["source"]),
                    "role_wave65_67_records": sum(r["score_records"] for r in counts if "/optimization_20261003_r9/" in r["source"]),
                    "retention_priority_wave68_70_records": sum(r["score_records"] for r in counts if "/optimization_20261003_r10/" in r["source"]),
                    "multi_method_wave71_76_records": sum(r["score_records"] for r in counts if "/optimization_20261003_r11/" in r["source"]),
                    "independent_membership_wave77_80_records": sum(r["score_records"] for r in counts if "/optimization_20261003_r12/" in r["source"]),
                    "later_round_records": {str(n):sum(r['score_records'] for r in counts if f'/optimization_20261003_r{n}/' in r['source']) for n in sorted(LATER_ROUNDS)},
                    "connected_known_restriction_records": sum(r["known_restriction"] for r in connected),
                    "historical_inventory_records": len(historical), "historical_rankable_records": 370,
                    "raw_metadata_config_records": len(raw_configs), "official_written_csv_scores": len(csv_test)},
        "catalog": CATALOG+neural_tuning_catalog()+catboost_tuning_catalog()+expanded_stacking_catalog()+additive_ridge_catalog()+fourier_ridge_catalog()+additive_basis_catalog()+no_dropout_seed_catalog()+neural_interaction_catalog()+neural_width_catalog()+neural_width_resource_catalog()+portfolio_surrogate_catalog()+nystrom_ridge_catalog()+nonlinear_stacking_catalog()+fourier_tuning_catalog()+temporal_output_catalog()+joint_layer_replay_catalog()+whole_scheme_runtime_catalog(),
        "representative": representatives(connected), "connected": connected, "mlp_bounds": bounds,
        "historical": historical, "csv_test": csv_test, "legacy_annual": legacy,
        "original_raw_metadata_configs": raw_configs,
        "missing_connected_records": missing, "failed_scoring_records": failures,
        "score_source_counts": counts,
        "notes": [
            f"旧744条总榜漏掉163条嵌套或variants评分；补齐旧907条，加R1–R6的249条及修正管线R7–R{max([12,*LATER_ROUNDS])}的{len(connected)-1156}条，现有{len(connected)}条精确评分记录。补表和方案评分记录不代表新增同等数量的独立模型训练。",
            f"同一模型的不同集成、平滑、留存、涨停偏移、收益映射版本，以及重复基线均保留。相同分数不证明预测完全相同，故不按分数伪去重；不可将{len(connected)}条称为{len(connected)}个独立模型。",
            "隐藏已知限制仅排除记录中已明确的整段未来特征自训练与旧全局剪枝等问题，不表示对所有历史管线重新完成合规认证。",
            "MLP缺四个年度边界的换手观测，连接分只能恢复区间；两区间重叠。区间排名以连接记录清单而非独立模型计数，并将另一MLP的潜在位置计入。",
            "波28保留14条精确评分并附并列重排勘误；另有1条harness失败无评分。波21勘误更正是否需要重拟合的标志，不改变分数。",
            "历史396条包括13个种子分数统计均值、4项未产出独立候选、1项失败诊断和8条非因果自训练结果；按原归档规则剩370条预测记录（含别名）。Ridge五日预测和旧历史特征筛选记录不意味着符合当前一日提交要求。",
            "旧343日历史表以重建帧和连续状态评分；已写CSV榜引用官方evaluate.py的已存结果。波13/最终v2的内存数组分，与12位CSV分不可混为一谈；17位CSV分分别是0.41709922352428086和0.4169548613417022。",
            f"R6–R{max([12,*LATER_ROUNDS])}候选只有训练连接验证分，本轮没有查看测试标签、没有补打测试分。新候选文件单独保存，正式交付指针仍指向TopK17.5%原版；本汇总报告不更改交付指针。",
            "R10的35条评分包括27种不同配置和8条重复对照；选中补入、剔除优先级权重均为0的原规则，复现R9方案，本轮未获得提升。",
            "R11分别从同一个R10基准测试模型权重、slow16排序权重、留存优先级信号和持仓信号融合，再测试各方向最优设置的组合；独立方向与组合的分数分别保存。",
            "R12将持仓排序器与收益排序器分离，逐阶段细搜融合权重、独立持仓模型、TopK配比与后处理及输出参数；各阶段沿用此前最高分设置，不能把阶段差异当作独立因果贡献。",
        ],
    }
    standard_data = (ROOT / "后续选模标准.md").read_bytes()
    SOURCES[str(ROOT / "后续选模标准.md")] = {"path": (ROOT / "后续选模标准.md").as_posix(),
                                               "bytes": len(standard_data), "sha256": hashlib.sha256(standard_data).hexdigest()}
    report["source_manifest"] = list(SOURCES.values())
    # Evidence sources must remain untouched while this report is produced.
    for source in SOURCES.values():
        assert hashlib.sha256(Path(source["path"]).read_bytes()).hexdigest() == source["sha256"], source["path"]
    output_json = OUT / "all_model_rankings_20261003.json"
    output_html = OUT / "all_model_rankings_20261003.html"
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    embedded = json.dumps(report, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("</", "<\\/")
    valid_best=max(r["score"] for r in connected if not r["known_restriction"])
    banner=""
    if (ROOT/"results/validation_provenance_erratum_20261003.json").exists():
        banner='<p style="background:#fff1d6;border:1px solid #eac47c;border-radius:10px;padding:16px"><b>验证来源勘误：</b>此前最高分0.447406500及W5a派生方案继承了全时期剪枝特征的验证依赖，保留为历史诊断，默认隐藏。R7修正折内筛选对照后，选中了无剪枝四模型集成。<a href="validation_provenance_erratum_20261003.json">查看证据</a></p>'
        report["notes"].append("2026-10-03来源审计确认W5a含全时期剪枝成员，R1–R6及相关旧验证方案不再当作合规选模基准；R7以fold-local剪枝修正对照后另行搜索，最终赢家采用不含剪枝成员的四模型集成。")
        # Re-embed notes after the source audit note is appended.
        embedded=json.dumps(report,ensure_ascii=False,separators=(",",":"),allow_nan=False).replace("</","<\\/")
        output_json.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    page=(PAGE.replace("__DATA__",embedded).replace("__PROVENANCE_BANNER__",banner).replace("__REPORT_DATE__",datetime.now().strftime('%Y-%m-%d %H:%M'))
          .replace("__VALIDATION_BEST__",f"{valid_best:.9f}").replace("__CONNECTED_COUNT__",f"{len(connected):,}"))
    output_html.write_text(page, encoding="utf-8")
    print(json.dumps({"outputs": [output_html.as_posix(), output_json.as_posix()], "summary": report["summary"],
                      "validation_best": connected[0]["score"], "csv_best": csv_test[0]["score"],
                      "representatives": [{"rank": r["rank"], "name": r["name"], "score": r["score"]}
                                          for r in report["representative"][:15]]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

# 安装与运行

先跑通根目录的固定 XGBoost 基准，可以完整经历数据准备、特征构建、模型训练和预测输出。该入口使用 67 项特征、16 个 XGBoost 种子模型及一个 LightGBM 辅助模型。复杂的 37 模型研究方案和单模型基线有各自的冻结入口，见[复现指南](REPRODUCIBILITY.md)。

## 运行前需要什么

| 条件 | 说明 |
|---|---|
| Python | 原研究环境为 Python 3.12 |
| 操作系统 | 基准命令提供 Windows 与 Linux / macOS 写法；历史进程管理脚本依赖 Windows |
| 数据 | 自行取得原始行情 CSV，字段见[数据指南](DATA_GUIDE.md) |
| 计算资源 | 可用 CPU 训练；完整面板约 790 万训练行，特征矩阵与模型需要额外内存和磁盘 |
| GPU | 固定基准支持 `--device cuda`，需匹配的 XGBoost 与驱动；不是运行基准的前提 |

仓库未提供通用的最低内存配置或跨平台性能基准。请根据数据规模安排资源，先看脚本和配置，再启动全量训练。

## 获取代码

```shell
git clone https://github.com/Zagadka-3906/stock-return-prediction.git
cd stock-return-prediction
```

仓库含大量历史证据。只读主流程时，可采用稀疏检出，先获取通用代码和文档：

```shell
git clone --depth 1 --filter=blob:none --sparse https://github.com/Zagadka-3906/stock-return-prediction.git
cd stock-return-prediction
git sparse-checkout set src config docs tests tools
```

稀疏检出会省略未选择目录。阅读历史方案前，用 `git sparse-checkout add analysis experiments results` 补充相应源码；冻结证据按[复现指南](REPRODUCIBILITY.md)中的具体归档目录获取。

## 安装环境

<details open>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

后续直接调用虚拟环境的 Python，无需更改 PowerShell 执行策略或激活脚本。

</details>

<details>
<summary><strong>Linux / macOS · shell</strong></summary>

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

下面命令中的 `.\.venv\Scripts\python.exe` 对应替换为 `.venv/bin/python`。此处提供命令转换，未承诺全部历史脚本可跨平台运行。

</details>

基础依赖由 [requirements.txt](../requirements.txt)固定，主要包括 Polars、PyArrow、NumPy、SciPy、Pandas、LightGBM、XGBoost 和 Qlib。Qlib 仅提供所选 Alpha158 特征公式定义，无需另外下载它的市场数据。

历史实验的附加依赖见 [requirements-experiments.txt](../requirements-experiments.txt)。神经网络与 CatBoost 等研究还有独立环境依赖；这些不属于根目录固定基准的必需安装步骤。

## 准备数据

```text
data/raw/
├── 训练集.csv
└── 测试集_X.csv
```

训练数据需要 `y_ret_1d`，预测数据仅需行情字段。股票代码保留字符串，日期使用 `YYYYMMDD`；完整字段列表见[数据指南](DATA_GUIDE.md#字段约定)。

特征构建会读取训练和预测行情，按股票、日期排序，以便预测起点能够使用此前的行情历史。测试标签不会作为特征输入。处理自己的数据时，需要保持时间顺序和主键唯一，并满足固定推理入口的完整矩形面板要求。

## 构建 63 项基础特征

```powershell
.\.venv\Scripts\python.exe -B -X utf8 run.py features
```

主要产物为 `data/features.parquet` 和 `data/feature_manifest.json`。前者缓存基础特征，后者记录特征名称、数量与 Qlib 公式等信息。

当原始数据或特征实现变化时，显式重建缓存：

```powershell
.\.venv\Scripts\python.exe -B -X utf8 run.py features --rebuild-features
```

同伴特征使用独立缓存 `data/peer_features.parquet`。重建基础特征后，也应让同伴缓存与它保持同源；入口不会自动证明旧缓存与新数据一致。建议将旧缓存移至单独备份目录后重新生成，并使用新的模型输出目录。

## 训练固定集成

```powershell
.\.venv\Scripts\python.exe -B -X utf8 train_ensemble.py --threads 8 --device cpu
```

入口读取 [config/ensemble.json](../config/ensemble.json)，追加四项同伴特征，生成 `data/peer_features.parquet`，训练并保存：

```text
models/ensemble/
├── xgboost_seed2026.ubj
├── ...
├── xgboost_seed2041.ubj
└── auxiliary.txt
```

16 个 XGBoost 模型学习一天收益的横截面排名；LightGBM 辅助模型提供收益信号。已存在的模型文件默认复用。需要重新训练时可传 `--retrain`，该参数会替换配置指向的模型文件，应先确认工作目录。

可传入独立配置：

```powershell
.\.venv\Scripts\python.exe -B -X utf8 train_ensemble.py --config config/ensemble.json --threads 8 --device cpu
```

这里的配置接口支持该固定配方；实现会检查 67 项特征、种子唯一性和既定后处理参数，不能把它当成通用的任意模型搜索接口。

## 生成预测

```powershell
.\.venv\Scripts\python.exe -B -X utf8 predict.py --threads 8 --output outputs/baseline_predictions.csv
```

推理按日期和股票排序计算，再恢复输入行顺序。输出列为 `ts_code,trade_date,pred`，入口会检查记录数、主键顺序、重复与非有限值。成功后会打印行数、日期数、股票数、成员数和输出位置。

> [!NOTE]
> 固定 XGBoost 基准的输出是后处理排名的仿射变换：有效值为 `0.04 × (ranked − 0.5)`，无效价格哨兵值为 `−0.05`。这种变换保持排序，并不等同于经过经验校准的收益率预测。

## 查看参数与评分

```powershell
.\.venv\Scripts\python.exe -B -X utf8 run.py --help
.\.venv\Scripts\python.exe -B -X utf8 train_ensemble.py --help
.\.venv\Scripts\python.exe -B -X utf8 predict.py --help
```

`run.py all` 运行的是更早的 LightGBM 流程，其验证年份为 2022—2024。它与上述固定 XGBoost 基准、基线143和37模型方案分别对应不同实现。

评分函数为 `evaluate.evaluate(_submission_path, _data_dir)`。评分目录内的 `测试集_X.csv` 和 `测试集_Y.csv` 应由所评估的验证区间构成。训练内部研究只使用训练期留出的标签；具体调用和边界见[方法详解](METHODS.md#评分定义)。

下一步可阅读[系统架构](ARCHITECTURE.md)，理解每个入口背后的模块；如果目标是复算某份历史文件，请使用[复现指南](REPRODUCIBILITY.md)。

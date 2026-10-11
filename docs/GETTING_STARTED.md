# 使用与复现

## 先选择你要做的事

| 目的 | 入口 |
|---|---|
| 了解项目和结论 | [README](../README.md)、[关于项目](../ABOUT.md)、[成果与交付](RESULTS.md) |
| 核查最新提交文件 | 当前候选的交付指针、`submission_manifest.json` 和 `方案包核验.json` |
| 从头运行一个固定配方 | 根目录 `run.py features`、`train_ensemble.py`、`predict.py` 的67特征基准 |
| 复现最新37模型方案 | 取得最新方案包、原始数据及所需历史依赖后，按冻结协议恢复；不是执行根目录基准入口 |
| 继续新实验 | 阅读[模型与验证](METHODS.md)和[后续选模标准](../后续选模标准.md)，建立新的独立输出目录 |

## 1. 准备数据

需自行取得赛题数据，放在项目根目录下：

```text
data/raw/训练集.csv
data/raw/测试集_X.csv
```

训练集应包含 `ts_code, trade_date, open, high, low, close, vol, amount, flag_limit_up, flag_limit_down, y_ret_1d`。预测输入具有相同行情字段，不含收益标签。股票代码保持字符串，交易日期采用 `YYYYMMDD`。

正常训练、选模和推理不需要实际 `测试集_Y.csv`。为训练内部评分准备的同名X/Y副本来自训练集验证区间，其数据来源须与实际比赛测试集区别记录。

## 2. 安装基准环境

项目本机运行环境为Windows 11、Python 3.12；基础依赖版本记录在[requirements.txt](../requirements.txt)。以下是新环境的基准操作，命令在仓库根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

基础流程主要使用Polars、NumPy、SciPy、LightGBM、XGBoost和Qlib。Qlib用于提供所采用的Alpha158公式定义；特征在赛题数据上计算，不另行下载Qlib市场数据。

`requirements.txt`不覆盖全部研究脚本。历史搜索依赖见[requirements-experiments.txt](../requirements-experiments.txt)；最新神经网络方案还涉及PyTorch、CatBoost、joblib等库，CUDA版本须与设备兼容。本机实际使用PyTorch `2.11.0+cu128`、CatBoost `1.2.10`、joblib `1.6.0`，这些是已运行环境的记录。Windows隐藏工作流管理还使用psutil、PowerShell及Windows进程接口。

## 3. 运行67特征、16种子基准

```powershell
.\.venv\Scripts\python.exe -B -X utf8 run.py features
.\.venv\Scripts\python.exe -B -X utf8 train_ensemble.py --threads 8 --device cpu
.\.venv\Scripts\python.exe -B -X utf8 predict.py --threads 8 --output outputs/baseline_predictions.csv
```

第一步生成基础63特征缓存；集成流程追加4个同伴特征。第二步按[config/ensemble.json](../config/ensemble.json)训练16种子XGBoost集成及辅助模型。第三步从保存模型输出预测。已保存且符合配方的模型会按入口逻辑复用；`--retrain`会要求重新训练。

这一流程生成历史基准，不会生成最新 `0.45146122` 候选。`run.py all`运行更早的LightGBM基准，代码中的验证年份是2022—2024，也不等于后续2020—2024连接验证流程。

先查看入口参数：

```powershell
.\.venv\Scripts\python.exe -B -X utf8 run.py --help
.\.venv\Scripts\python.exe -B -X utf8 train_ensemble.py --help
.\.venv\Scripts\python.exe -B -X utf8 predict.py --help
```

## 4. 使用最新交付

最新交付位置、CSV和ZIP的SHA256见[成果与交付](RESULTS.md)及[机器可读状态](latest_results.json)。有本机方案包时，直接使用包中根目录 `submission.csv`；不必为提交再次训练模型。

方案包包含37个原生模型、选择配置、冻结源码和验证证据，但没有原始比赛数据或Python环境。冻结协议包含本机D/E盘绝对路径，部分流程依赖父方案与历史缓存。因此，ZIP是一份已核验交付及复现材料，不是跨机器解压后即可自动重新训练的安装包。

若要完整复现，先按[目录与记录](REPOSITORY_GUIDE.md)确定父方案、数据、配置和模型依赖，核验文件哈希，再恢复对应路径与环境。弃用权重已删除的历史方案需要重新训练或从另有保存的副本恢复，不能假定Git克隆中存在全部权重。带冻结哈希的源码副本应保持原样，新尝试使用新目录。

## 5. 理解评分入口

[evaluate.py](../evaluate.py)暴露 `evaluate(submission_path, data_dir)`，会从 `data_dir`读取名为 `测试集_X.csv` 和 `测试集_Y.csv` 的文件。脚本末尾的默认路径是原评分示例路径，不是通用命令行配置。

训练内部比较时，传入由训练期样本构造的独立评分目录；不要把实际测试答案放入选模流程。具体过滤规则和公式见[模型与验证](METHODS.md)。最新记录已保存官方指标，阅读文档或提交现成CSV无需重跑评分。

## 常见疑问

**为什么克隆后不能运行某轮脚本？** Git主要保存代码和记录；原始数据、二进制权重、预测缓存和旧运行路径可能未随克隆提供，部分弃用产物已经清理。

**为什么两个“最新方案”分数不同？** 一个是完整推理已通过的新候选，一个是正式完整榜登记已完成的交付。它们的资格状态不同，见[成果与交付](RESULTS.md)。

**18,959是模型数量吗？** 这是评分记录数量，包含对照、配置变化、复用与重复记录，不是独立模型或独立试验数量。

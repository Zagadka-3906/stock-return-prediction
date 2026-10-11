"""Keep the 41-model catalogue and restore required percentile input routing."""
import linear_model_sources_20261003 as previous
from causal_model_loading_20261004 import load_bundle
OUT=previous.OUT
CONFIGS=previous.CONFIGS
NEW_CONFIGS=previous.NEW_CONFIGS
YEARS=previous.YEARS
read,dump,sha,log=previous.read,previous.dump,previous.sha,previous.log
source_dir=previous.source_dir
model_path=previous.model_path
train_one=previous.train_one
predict_arrays=previous.predict_arrays
ranker_source=previous.ranker_source
verify=previous.verify


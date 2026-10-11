"""Use the tested objective-agnostic disk-map fitter with unchanged native GOSS parameters."""
from types import SimpleNamespace
import mature_training_memmap_20261006 as mapped
import train_gradient_sampling_bank_20261005 as original

CONFIGS = original.CONFIGS
engine = original.engine
ADAPTER = SimpleNamespace(matched=original, parameters=original.parameters)


def fit_preprocessed(artifact, cfg, mean, scale, clean_info):
    assert cfg['kind'] == 'lightgbm_gradient_sampling' and cfg['data_sample_strategy'] == 'goss'
    assert not cfg['linear_tree'] and cfg['num_boost_round'] == 300
    bundle = mapped.fit_preprocessed(ADAPTER, artifact, cfg, mean, scale, clean_info)
    # The shared fitter's numerical operations are objective-agnostic; its original
    # quantile-specific kind tag is replaced with the actual unchanged GOSS kind.
    bundle['kind'] = 'lightgbm_gradient_sampling'
    assert bundle['native_training_parameters'] == original.parameters(cfg)
    assert '[data_sample_strategy: goss]' in bundle['model_string']
    assert bundle['requested_and_actual_boosting_iterations'] == 300
    assert bundle['leaf_summary']['tree_count'] == 300
    assert bundle['leaf_summary']['leaves_with_linear_features'] == 0
    assert bundle['leaf_summary']['first_tree_constant'] and bundle['leaf_summary']['all_leaf_coefficients_finite']
    return bundle


predict_arrays = original.predict_arrays

"""Independent tree sums for verified identity-output L2, L1 and Huber objectives.

LightGBM4.7.0 RegressionL1loss/RegressionHuberLoss inherit the L2
ConvertOutput; without sqrt it returns the input unchanged.
https://github.com/microsoft/LightGBM/blob/v4.7.0/src/objective/regression_objective.hpp
"""
from pathlib import Path

SOURCE = Path(__file__).with_name('conditional_flag_rank_codec_20261006.py')
original = SOURCE.read_text(encoding='utf-8')
before = "    assert model['objective'].split()[0] == 'regression'"
after = "    assert model['objective'].split() in (['regression'], ['regression_l1'], ['huber'])"
assert original.count(before) == 1
text = original.replace(before, after)
assert text.replace(after, before) == original
namespace = {'__file__': __file__, '__name__': 'independent_identity_regression_tree_codec'}
exec(compile(text, str(SOURCE), 'exec'), namespace)
clean_matrix = namespace['clean_matrix']
predict_dump = namespace['predict_dump']

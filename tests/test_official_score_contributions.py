import unittest

import numpy as np
import pandas as pd

from analysis.official_score_contributions import composite, daily_contribution, paired_difference


class OfficialScoreContributionTests(unittest.TestCase):
    def frame(self, turnover):
        return pd.DataFrame({"trade_date": [20200102, 20200103, 20200106],
                             "rank_ic": [0.1, 0.2, 0.3], "excess": [0.01, 0.02, 0.03],
                             "turnover": turnover})

    def test_first_day_missing_turnover_keeps_two_day_denominator(self):
        candidate = self.frame([np.nan, 0.2, 0.4])
        baseline = candidate.assign(rank_ic=0.0, excess=0.0, turnover=[np.nan, 0.0, 0.0])
        # 0.4*0.2 + 0.3*252*0.02 - 0.3*mean([0.2,0.4]) = 1.502.
        self.assertAlmostEqual(paired_difference(candidate, baseline).mean(), 1.502, places=12)
        self.assertAlmostEqual(daily_contribution(candidate).mean(), composite(candidate) - 0.3)

    def test_each_arm_retains_its_own_missing_metric_denominators(self):
        candidate = self.frame([np.nan, 0.2, 0.4])
        baseline = self.frame([np.nan, np.nan, 0.7])
        candidate.loc[0, "rank_ic"] = np.nan
        baseline.loc[2, "excess"] = np.nan
        expected = (0.4 * (0.25 - 0.2) + 0.3 * 252 * (0.02 - 0.015)
                    - 0.3 * (0.3 - 0.7))
        self.assertAlmostEqual(paired_difference(candidate, baseline).mean(), expected, places=12)

    def test_equal_length_different_dates_are_rejected(self):
        candidate = self.frame([np.nan, 0.2, 0.4])
        baseline = candidate.copy()
        baseline.loc[2, "trade_date"] = 20200107
        with self.assertRaisesRegex(AssertionError, "aligned"):
            paired_difference(candidate, baseline)

    def test_missing_entire_metric_or_infinite_metric_is_rejected(self):
        for values in ([np.nan, np.nan, np.nan], [np.nan, np.inf, 0.4]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                daily_contribution(self.frame(values))


if __name__ == "__main__":
    unittest.main()

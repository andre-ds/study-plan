"""
Optimal binning algorithm given scenarios. Extensive form of the stochastic
continuous optimal binning.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2022

import numbers
import time

import numpy as np

from sklearn.utils import check_array

from ...information import solver_statistics
from ...logging import Logger
from ...binning.preprocessing import split_data_scenarios
from ..continuous_binning import ContinuousOptimalBinning
from .binning_scenarios import _check_X_Y_weights


logger = Logger(__name__).logger


def _check_parameters():
    pass


class SBContinuousOptimalBinning(ContinuousOptimalBinning):
    def __init__(self, name="", prebinning_method="cart", max_n_prebins=20,
                 min_prebin_size=0.05, min_n_bins=None, max_n_bins=None,
                 min_bin_size=None, max_bin_size=None, monotonic_trend=None,
                 min_mean_diff=0, max_pvalue=None,
                 max_pvalue_policy="consecutive", user_splits=None,
                 user_splits_fixed=None, special_codes=None, split_digits=None,
                 time_limit=100, verbose=False):

        self.name = name
        self.dtype = "numerical"
        self.prebinning_method = prebinning_method
        self.solver = "cp"

        self.max_n_prebins = max_n_prebins
        self.min_prebin_size = min_prebin_size

        self.min_n_bins = min_n_bins
        self.max_n_bins = max_n_bins
        self.min_bin_size = min_bin_size
        self.max_bin_size = max_bin_size

        self.monotonic_trend = monotonic_trend
        self.min_mean_diff = min_mean_diff
        self.max_pvalue = max_pvalue
        self.max_pvalue_policy = max_pvalue_policy

        self.user_splits = user_splits
        self.user_splits_fixed = user_splits_fixed
        self.special_codes = special_codes
        self.split_digits = split_digits

        self.time_limit = time_limit

        self.verbose = verbose

        # auxiliary
        self._n_scenarios = None
        self._n_records = None
        self._sums = None
        self._stds = None
        self._min_target = None
        self._max_target = None
        self._n_zeros = None
        self._n_records_cat_others = None
        self._n_records_missing = None
        self._n_records_special = None
        self._sum_cat_others = None
        self._sum_special = None
        self._sum_missing = None
        self._std_cat_others = None
        self._std_special = None
        self._std_missing = None
        self._min_target_missing = None
        self._min_target_special = None
        self._min_target_others = None
        self._max_target_missing = None
        self._max_target_special = None
        self._max_target_others = None
        self._n_zeros_missing = None
        self._n_zeros_special = None
        self._n_zeros_others = None
        self._problem_type = "regression"

        # info

        # timing
        self._time_total = None
        self._time_preprocessing = None
        self._time_prebinning = None
        self._time_solver = None
        self._time_optimizer = None
        self._time_postprocessing = None

        self._is_fitted = False

    def fit(self, X, Y, weights=None, check_input=False):
        """Fit the optimal binning given a list of scenarios.

        Parameters
        ----------
        X : array-like, shape = (n_scenarios,)
            Lit of training vectors, where n_scenarios is the number of
            scenarios.

        Y : array-like, shape = (n_scenarios,)
            List of target vectors relative to X.

        weights : array-like, shape = (n_scenarios,)
            Scenarios weights. If None, then scenarios are equally weighted.

        check_input : bool (default=False)
            Whether to check input arrays.

        Returns
        -------
        self : SBContinuousOptimalBinning
            Fitted optimal binning.
        """
        return self._fit(X, Y, weights, check_input)

    def fit_transform(self, x, X, Y, weights=None, metric="mean",
                      metric_special=0, metric_missing=0, show_digits=2,
                      check_input=False):
        """Fit the optimal binning given a list of scenarios, then
        transform it.

        Parameters
        ----------
        x : array-like, shape = (n_samples,)
            Training vector, where n_samples is the number of samples.

        X : array-like, shape = (n_scenarios,)
            Lit of training vectors, where n_scenarios is the number of
            scenarios.

        Y : array-like, shape = (n_scenarios,)
            List of target vectors relative to X.

        weights : array-like, shape = (n_scenarios,)
            Scenarios weights. If None, then scenarios are equally weighted.

        metric : str (default="mean"):
            The metric used to transform the input vector. Supported metrics
            are "mean" to choose the mean, "indices" to assign the
            corresponding indices of the bins and "bins" to assign the
            corresponding bin interval.

        metric_special : float or str (default=0)
            The metric value to transform special codes in the input vector.
            Supported metrics are "empirical" to use the empirical WoE or
            event rate, and any numerical value.

        metric_missing : float or str (default=0)
            The metric value to transform missing values in the input vector.
            Supported metrics are "empirical" to use the empirical WoE or
            event rate and any numerical value.

        show_digits : int, optional (default=2)
            The number of significant digits of the bin column. Applies when
            ``metric="bins"``.

        check_input : bool (default=False)
            Whether to check input arrays.

        Returns
        -------
        x_new : numpy array, shape = (n_samples,)
            Transformed array.
        """
        return self.fit(X, Y, weights, check_input).transform(
            x, metric, metric_special, metric_missing, show_digits,
            check_input)

    def _fit(self, X, Y, weights, check_input):
        time_init = time.perf_counter()

        # Check weights and input arrays
        _check_X_Y_weights(X, Y, weights)

        self._n_scenarios = len(X)

        if self.verbose:
            logger.info("Optimal binning started.")
            logger.info("Options: check parameters.")

        _check_parameters(**self.get_params())

        # Pre-processing
        if self.verbose:
            logger.info("Pre-processing started.")

        time_preprocessing = time.perf_counter()

        self._n_samples_scenario = [len(x) for x in X]
        self._n_samples = sum(self._n_samples_scenario)

        if self.verbose:
            logger.info("Pre-processing: number of samples: {}"
                        .format(self._n_samples))

        [x_clean, y_clean, x_missing, y_missing, x_special, y_special,
         w] = split_data_scenarios(X, Y, weights, self.special_codes,
                                   check_input)

        self._time_preprocessing = time.perf_counter() - time_preprocessing

        if self.verbose:
            n_clean = len(x_clean)
            n_missing = len(x_missing)
            n_special = len(x_special)

            logger.info("Pre-processing: number of clean samples: {}"
                        .format(n_clean))

            logger.info("Pre-processing: number of missing samples: {}"
                        .format(n_missing))

            logger.info("Pre-processing: number of special samples: {}"
                        .format(n_special))

            logger.info("Pre-processing terminated. Time: {:.4f}s"
                        .format(self._time_preprocessing))

        # Pre-binning
        if self.verbose:
            logger.info("Pre-binning started.")

        time_prebinning = time.perf_counter()

        if self.user_splits is not None:
            user_splits = check_array(
                self.user_splits, ensure_2d=False, dtype=None,
                force_all_finite=True)

            if len(set(user_splits)) != len(user_splits):
                raise ValueError("User splits are not unique.")

            sorted_idx = np.argsort(user_splits)
            user_splits = user_splits[sorted_idx]

            if self.user_splits_fixed is not None:
                self.user_splits_fixed = np.asarray(
                    self.user_splits_fixed)[sorted_idx]
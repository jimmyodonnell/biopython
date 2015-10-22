# coding=utf-8
import copy
import unittest

try:
    import numpy
except ImportError:
    from Bio import MissingPythonDependencyError
    raise MissingPythonDependencyError(
        "Install NumPy if you want to use Bio.NaiveBayes.")

from Bio import NaiveBayes


class NaiveBayesTest(unittest.TestCase):
    def setUp(self):
        # Using example from https://en.wikipedia.org/wiki/Naive_Bayes_classifier
        # height (feet), weight (lbs), foot size (inches)
        self.xs = [
            [6, 180, 12],
            [5.92, 190, 11],
            [5.58, 170, 12],
            [5.92, 165, 10],
            [5, 100, 6],
            [5.5, 150, 8],
            [5.42, 130, 7],
            [5.75, 150, 9],
        ]
        self.ys = [
            'male',
            'male',
            'male',
            'male',
            'female',
            'female',
            'female',
            'female',
        ]
        self.model = NaiveBayes.train(self.xs, self.ys)
        self.test = [6, 130, 8]

    def test_train_function_no_training_set(self):
        self.assertRaises(ValueError, NaiveBayes.train, [], self.ys)

    def test_train_function_input_lengths(self):
        ys = copy.copy(self.ys)
        ys.pop()
        self.assertRaises(ValueError, NaiveBayes.train, self.xs, ys)

    def test_train_function_uneven_dimension_of_training_set(self):
        xs = copy.copy(self.xs)
        xs[0] = [1]
        self.assertRaises(ValueError, NaiveBayes.train, xs, self.ys)

    def test_train_function_with_priors(self):
        model = NaiveBayes.train(self.xs, self.ys, priors={'male': 0.1, 'female': 0.9})
        result = NaiveBayes.calculate(model, self.test, scale=True)
        expected = -692.0
        self.assertEqual(expected, round(result['male']))

    def test_classify_function(self):
        expected = "female"
        result = NaiveBayes.classify(self.model, self.test)
        self.assertEqual(expected, result)

    def test_calculate_function_wrong_dimensionality(self):
        xs = self.xs[0]
        xs.append(100)
        self.assertRaises(ValueError, NaiveBayes.calculate, self.model, xs)

    def test_calculate_function_with_scale(self):
        result = NaiveBayes.calculate(self.model, self.test, scale=True)
        expected = -689.0
        self.assertEqual(expected, round(result['male']))
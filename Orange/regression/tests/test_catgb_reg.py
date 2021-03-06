import unittest

from Orange.data import Table
from Orange.evaluation import CrossValidation, RMSE
from Orange.preprocess.score import Scorer

try:
    from Orange.regression import CatGBRegressor
except ImportError:
    CatGBRegressor = None


@unittest.skipIf(CatGBRegressor is None, "Missing 'catboost' package")
class TestCatGBRegressor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.housing = Table("housing")

    def test_GBTrees(self):
        booster = CatGBRegressor()
        cv = CrossValidation(k=10)
        results = cv(self.housing, [booster])
        RMSE(results)

    def test_predict_single_instance(self):
        booster = CatGBRegressor()
        model = booster(self.housing)
        for ins in self.housing:
            pred = model(ins)
            self.assertGreater(pred, 0)

    def test_predict_table(self):
        booster = CatGBRegressor()
        model = booster(self.housing)
        pred = model(self.housing)
        self.assertEqual(pred.shape, (len(self.housing),))
        self.assertGreater(all(pred), 0)

    def test_predict_numpy(self):
        booster = CatGBRegressor()
        model = booster(self.housing)
        pred = model(self.housing.X)
        self.assertEqual(pred.shape, (len(self.housing),))
        self.assertGreater(all(pred), 0)

    def test_predict_sparse(self):
        sparse_data = self.housing.to_sparse()
        booster = CatGBRegressor()
        model = booster(sparse_data)
        pred = model(sparse_data)
        self.assertEqual(pred.shape, (len(sparse_data),))
        self.assertGreater(all(pred), 0)

    def test_set_params(self):
        booster = CatGBRegressor(n_estimators=42, max_depth=4)
        self.assertEqual(booster.params["n_estimators"], 42)
        self.assertEqual(booster.params["max_depth"], 4)
        model = booster(self.housing)
        params = model.cat_model.get_params()
        self.assertEqual(params["n_estimators"], 42)
        self.assertEqual(params["max_depth"], 4)

    def test_scorer(self):
        booster = CatGBRegressor()
        self.assertIsInstance(booster, Scorer)
        booster.score(self.housing)


if __name__ == "__main__":
    unittest.main()

import sys
sys.path.append("/Users/masakitashiro/Documents/machine-learning/app_spell/for_dev/")
from ml.model_api import Predictor

def test_model_api():
    predictor = Predictor()
    print(predictor.predict("he is an special man.", lang="eng"))
    print(predictor.predict("彼さ立派な人間で批判に値します。"))
    del predictor

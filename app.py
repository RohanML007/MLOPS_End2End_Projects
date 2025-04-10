import os
import warnings
import sys


import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
from mlflow.models.signature import infer_signature
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

os.environ["MLFLOW_TRACKING_URI"] = "http://ec2-3-88-102-20.compute-1.amazonaws.com:5000/"

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

if __name__ == "__main__":
    
    #Data Ingestion --> Reading the wine quality dataset
    csv_url = (
        "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-red.csv"
    )

    try:
        data = pd.read_csv(csv_url, sep=";")
    except Exception as e:
        logger.exception("Unable to download the data")

    #Split the data into train and test sets
    train, test = train_test_split(data)  #By default it takes 0.25 as test size
    x_train = train.drop(["quality"], axis=1)
    y_train = train[["quality"]]
    x_test = test.drop(["quality"], axis=1)
    y_test = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(x_train, y_train)

        predicted_qualities = lr.predict(x_test)
        (rmse, mae, r2) = eval_metrics(y_test, predicted_qualities)

        print("ElasticNet Model (alpha = {:f}, l1_ratio = {:f}):".format(alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param('alpha', alpha)
        mlflow.log_param('l1_ratio', l1_ratio)
        mlflow.log_metric('rmse', rmse)
        mlflow.log_metric('mae', mae)
        mlflow.log_metric('r2', r2)

        #For the remote AWS server we need to do the setup
        remote_server_uri = "http://ec2-3-88-102-20.compute-1.amazonaws.com:5000/"
        mlflow.set_tracking_uri(remote_server_uri)
        
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            #Registering the model
            mlflow.sklearn.log_model(lr, "model", registered_model_name="ElasticNetWineModel")
        else:
            mlflow.sklearn.log_model(lr, "model") #MLflow can log the model but cannot register it in case we are logging locally, because the model registry needs a remote backend.
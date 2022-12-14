# Import libraries
import mlflow
import argparse
import glob
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


# define functions
def main(args):
    # enable auto logging
    mlflow.autolog()

    # read data
    df = get_csvs_df(args.training_data)

    # process data
    X_train, X_test, y_train, y_test = process_data(df)

    # train model
    model = train_model(args.reg_rate, X_train,  # noqa: F841
                        X_test, y_train, y_test)
    # run_id = mlflow.active_run().info.run_id
    # print(run_id)
    # mlflow.register_model()
    # register model using mlflow model
    # model_uri = f'runs:/{run_id}/{args.model_name}'
    # mlflow.register_model(model_uri, model_name)


def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


def process_data(df):
    # split dataframe into X and y
    X, y = df[['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
               'TricepsThickness', 'SerumInsulin', 'BMI', 'DiabetesPedigree',
               'Age']].values, df['Diabetic'].values

    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=0)

    # return splits and encoder
    return X_train, X_test, y_train, y_test


def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    model = LogisticRegression(C=1/reg_rate,
                               solver="liblinear").fit(X_train, y_train)

    # return model
    return model


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    parser.add_argument("--reg_rate", dest='reg_rate',
                        type=float, default=0.01)
    print("args parsed!!")
    # parse args
    args = parser.parse_args()

    # return args
    return args


# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")

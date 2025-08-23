import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle

data = './diabetes.csv'
df = pd.read_csv(data)
df.shape

df.head()
X = df.drop('Outcome',axis=1) # predictor feature coloumns
y = df.Outcome


X_train , X_test , y_train , y_test = train_test_split(X, y, test_size = 0.20, random_state = 10)

print('Training Set :',len(X_train))
print('Test Set :',len(X_test))
print('Training labels :',len(y_train))
print('Test Labels :',len(y_test))

from sklearn.impute import SimpleImputer
#impute with mean all 0 readings
fill = SimpleImputer(missing_values = 0 , strategy ="mean")#impute with mean all 0 readings

#fill = Imputer(missing_values = 0 , strategy ="mean", axis=0)

X_train = fill.fit_transform(X_train)
X_train = fill.fit_transform(X_train)
X_test = fill.transform(X_test)


# Define the model hyperparameters
params = {
    "solver": "lbfgs",
    "max_iter": 22,
    "multi_class": "auto",
    "random_state": 123,
}

# Train the model
lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

# Predict on the test set
y_pred = lr.predict(X_test)

report = classification_report(y_test, y_pred)
print(report)

report_dict = classification_report(y_test, y_pred, output_dict=True)
print(report_dict)


import dagshub
dagshub.init(repo_owner='edurekajuly24gcp', repo_name='dagshub-demo', mlflow=True)


import mlflow

mlflow.set_experiment("LR experiments 23_08")
#mlflow.set_tracking_uri(uri="http://127.0.0.1:5000/")

with mlflow.start_run():
    mlflow.set_tag("author", "AJ")  # Replace with your actual name
    mlflow.log_params(params)
    mlflow.log_metrics({
        'accuracy': report_dict['accuracy'],
        'recall_class_0': report_dict['0']['recall'],
        'recall_class_1': report_dict['1']['recall'],
        'f1_score_macro': report_dict['macro avg']['f1-score']
    })
    # Save the model to a file
    filename = 'logistic_regression_model.pkl'
    pickle.dump(lr, open(filename, 'wb'))
    # Log the model file as an artifact
    mlflow.log_artifact(filename, "logistic_regression")
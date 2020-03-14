import ml_model


def test_mlMSE(model, X, y):
    '''
    Tests the function mlMSE
    '''
    print("Testing ml_model.mlMSE")
    mse = ml_model.mlMSE(model, X, y)
    print(f"MSE for sample dataset is: {mse}")
    assert 0.0 < mse and mse < 1.5


def main():
    '''
    Testing the functions in ml_model.py
    '''
    filename = "sample.csv"
    X, y_test, df = ml_model.load_dataset(filename)
    test_model, test_X_test, test_y_test = ml_model.mlTrain(X, y_test)
    test_mlMSE(test_model, test_X_test, test_y_test)
    print("Tests All Passed: ML")


if __name__ == "__main__":
    main()

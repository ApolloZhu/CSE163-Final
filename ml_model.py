import graphviz
import pandas as pd
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def plot_tree(model, X):
    '''
    Modified based on CSE 163 implementation.

    This function takes a model and the X values for a dataset
    and plots a visualization of the decision tree
    '''
    dot_data = export_graphviz(
        model, out_file=None,
        feature_names=X.columns,
        rotate=True, filled=True, rounded=True,
        special_characters=True
    )
    return graphviz.Source(dot_data)


def mlTrain(X, y):
    '''
    Take feature and labels as input and returns
    the trained model, test features, and labels
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    score_mse = mlMSE(model, X_train, y_train)
    print(f"    MSE for train: {score_mse}")
    return model, X_test, y_test


def mlMSE(model, X_test, y_test):
    '''
    Calculate the mean square error between the X_test
    and the value predicted using y_test for the model
    '''
    return mean_squared_error(y_test, model.predict(X_test))


def load_dataset(filename, dropna=True, adjusted=False):
    '''
    Load in dataset from a csv file
    '''
    df = pd.read_csv(filename)
    # Remove all rows where Score/Members/Favorites has no data
    labels = ["Score", "Members", "Favorites"]
    if dropna:
        df = pd.DataFrame(df.dropna(subset=labels))

    non_features = [
        "ID", "Name", "Year", "English", "Japanese", "Broadcast",
    ] + labels
    if adjusted:
        non_features += ["Episodes", "Duration"]
    X = df[df.columns.difference(non_features)].fillna(0)
    X = pd.get_dummies(X)
    X.columns = X.columns.str.replace("&", "and")
    return X, df["Score"], df


def predict_future_anime(model, X, adjusted=False, future="future.csv"):
    '''
    Returns the predicted scores using the given model for the given future,
    substituting 0 as values for missing features if necessary.
    '''
    future_anime, _, df = load_dataset(future, dropna=False, adjusted=adjusted)
    missing_dummies = set(X.columns) - set(future_anime.columns)
    future_anime = future_anime.assign(**dict.fromkeys(missing_dummies, 0))
    return model.predict(future_anime), df


def validatedMLTrain(adjusted=False):
    '''
    Return a trained model and its feature set
    '''
    X, y_score, df = load_dataset("full.csv", adjusted=adjusted)
    score_model, score_X_test, score_y_test = mlTrain(X, y_score)

    score_mse = mlMSE(score_model, score_X_test, score_y_test)
    print(f"    MSE for test : {score_mse}")

    # Compare against current season (winter 2020)
    # indices = df[(df["Year"] == 2020) & (df["Season"] == "winter")].index
    # score_mse = mlMSE(score_model, X.loc[indices, :], y_score.loc[indices])
    # print(f"\tMSE for current season is: {score_mse}")
    return score_model, X


def main():
    '''
    Training our model to predict for score
    '''
    print("Model, All Features")
    score_model, X = validatedMLTrain()
    plot_tree(score_model, X).render("model")
    # Predict for future season
    raw, df = predict_future_anime(score_model, X)
    print("Model, No Duration/Episodes")
    score_model, X = validatedMLTrain(adjusted=True)
    adjusted, _ = predict_future_anime(score_model, X, adjusted=True)
    df["Score"] = raw
    df["Score (adjusted)"] = adjusted
    df["Score (difference)"] = adjusted - raw
    df.to_csv("predictions.csv")


if __name__ == "__main__":
    main()

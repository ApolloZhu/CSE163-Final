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
        # class_names=y.unique(),
        filled=True, rounded=True,
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
    return model, X_test, y_test


def mlMSE(model, X_test, y_test):
    '''
    Calculate the mean square error between the X_test
    and the value predicted using y_test for the model
    '''
    return mean_squared_error(y_test, model.predict(X_test))


def load_dataset(filename, dropna=True):
    df = pd.read_csv(filename)
    # Remove all rows where Score/Members/Favorites has no data
    labels = ["Score", "Members", "Favorites"]
    if dropna:
        df = pd.DataFrame(df.dropna(subset=labels))

    filt_lst = [
        "ID", "Name", "Year", "English", "Japanese", "Broadcast",
    ] + labels
    X = df[df.columns.difference(filt_lst)].fillna(0)
    X = pd.get_dummies(X)
    X.columns = X.columns.str.replace("&", " and ")
    return X, df["Score"], df


def populate_future(filename, model, features, future="future.csv"):
    '''
    Fills the score column of future season where Score is unknown
    and save the results to the given filename.
    '''
    future_anime, _, df = load_dataset(future, dropna=False)
    missing_dummies = set(features) - set(future_anime.columns)
    future_anime = future_anime.assign(**dict.fromkeys(missing_dummies, 0))
    df["Score"] = model.predict(future_anime)
    df.to_csv(filename)


def main():
    '''
    Training our model for score, members, and favorites
    '''
    X, y_score, df = load_dataset("full.csv")
    score_model, score_X_test, score_y_test = mlTrain(X, y_score)
    score_mse = mlMSE(score_model, score_X_test, score_y_test)

    plot_tree(score_model, score_X_test).render("model")
    print(f"MSE for entire dataset is: {score_mse}")

    indices = df[(df["Year"] == 2020) & (df["Season"] == "winter")].index
    score_mse = mlMSE(score_model, X.loc[indices, :], y_score.loc[indices])
    print(f"MSE for current season is: {score_mse}")

    populate_future("predictions.csv", score_model, X.columns)


if __name__ == "__main__":
    main()

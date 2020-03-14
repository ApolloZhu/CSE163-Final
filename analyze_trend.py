import pandas as pd
import seaborn as sns
# https://matplotlib.org/examples/color/colormaps_reference.html
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from build_dataset import basic_headers


def analyze_trend(df, prefix=""):
    # Discard anything that doesn"t have a user rating (score)
    df = pd.DataFrame(df.dropna(subset=["Score"]))
    # Set desired sorting order for season
    df["Season"] = pd.Categorical(df["Season"],
                                  ["winter", "spring", "summer", "fall"])
    # Keep the 10 most popular anime in each season and sum all genres
    grouped = df.groupby(["Year", "Season"]) \
        .apply(lambda season: season.nlargest(5, "Score", keep="all")) \
        .reset_index(drop=True) \
        .groupby(["Year", "Season"]).sum().dropna()
    # Filter columns to contain only genres in the figure
    only_genres = grouped[grouped.columns.difference(basic_headers)]
    plot_trend(only_genres, prefix)
    plot_heatmap(only_genres, prefix)


def normalize(df):
    '''
    Returns the percentage instead of raw counts
    '''
    return df.div(df.sum(axis=1), axis=0)


def drop_if(condition, df):
    columns_to_drop = df.columns[condition(df)]
    return df.drop(columns_to_drop, axis=1)


def plot_trend(df, prefix):
    count = min(20, len(df))
    recent = df.tail(count)

    def not_minimum_requirement(df):
        return (df >= 1).sum() < count * 0.4
    normalized = normalize(drop_if(not_minimum_requirement, recent))
    plot_stacked_area(normalized, filename=f"{prefix}genres trend recent.png")


def plot_stacked_area(df, filename):
    df = df.reindex(df.sum().sort_values(ascending=False).index, axis=1)
    # Select different color pallets depending on number of genres.
    cmap = cm.gist_ncar if len(df.columns) > 20 else cm.tab20
    # Make sure it"s long enough to include everything
    df.plot.area(figsize=(20, 10), fontsize=10, rot=45, cmap=cmap)
    plt.margins(0)
    plt.ylim([0, 1])
    plt.legend(loc="upper left")
    plt.savefig(filename, bbox_inches="tight")


def plot_heatmap(df, prefix):
    normalized = normalize(df).transpose()
    sns.set()
    plt.style.use("dark_background")
    plt.figure(figsize=(40, 20))
    sns.heatmap(
        normalized,
        square=True,
        cbar_kws={"fraction": 0.01},  # shrink color bar
        cmap=cm.afmhot
    )
    plt.tick_params(labelright=True)
    plt.xticks(rotation=45, horizontalalignment="right")
    plt.yticks(rotation=0)
    plt.savefig(f"{prefix}genres heatmap.png", bbox_inches="tight")


if __name__ == "__main__":
    df = pd.read_csv("full.csv")
    analyze_trend(df)

import pandas as pd
import seaborn as sns
# https://matplotlib.org/examples/color/colormaps_reference.html
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from build_dataset import basic_headers


def only_genres_for_top_n(df, n):
    grouped = df.groupby(["Year", "Season"]) \
        .apply(lambda season: season.nlargest(n, "Score", keep="all")) \
        .reset_index(drop=True) \
        .groupby(["Year", "Season"]).sum().dropna()
    return grouped[grouped.columns.difference(basic_headers)]


def analyze_trend(df, prefix=""):
    # Discard anything that doesn"t have a user rating (score)
    df = pd.DataFrame(df.dropna(subset=["Score"]))
    # Set desired sorting order for season
    df["Season"] = pd.Categorical(df["Season"],
                                  ["winter", "spring", "summer", "fall"])
    only_genres = only_genres_for_top_n(df, 5)
    plot_trend(only_genres, prefix, top_n=5)
    # Keep the 10 most popular anime in each season and sum all genres
    only_genres = only_genres_for_top_n(df, 10)
    # Filter columns to contain only genres in the figure
    plot_trend(only_genres, prefix, top_n=10)
    plot_heatmap(only_genres, prefix)


def normalize(df):
    '''
    Returns the percentage instead of raw counts
    '''
    return df.div(df.sum(axis=1), axis=0)


def drop_if(condition, df):
    columns_to_drop = df.columns[condition(df)]
    return df.drop(columns_to_drop, axis=1)


def plot_trend(df, prefix, top_n):
    # Plot at most 20 seasons
    count = min(20, len(df))
    recent = df.tail(count)

    def not_minimum_requirement(df):
        """
        Must be in 40% of the seasons popular genres to count as popular.
        """
        return (df >= 1).sum() < count * 0.4
    normalized = normalize(drop_if(not_minimum_requirement, recent))
    plot_stacked_area(normalized, top_n,
                      f"{prefix}genres trend recent (top {top_n}).png")


def plot_stacked_area(df, top_n, filename):
    sns.set()
    df = df.reindex(df.sum().sort_values(ascending=False).index, axis=1)
    # Select different color pallets depending on number of genres.
    cmap = cm.gist_ncar if len(df.columns) > 20 else cm.tab20
    # Make sure it"s long enough to include everything
    df.plot.area(figsize=(20, 10), fontsize=10, cmap=cmap)
    plt.margins(0)
    plt.ylim([0, 1])
    plt.legend(loc="upper left")
    plt.title(f"Popular Generes for Top {top_n} Anime in Previous {len(df)} Seasons")
    plt.savefig(filename, bbox_inches="tight")


def plot_heatmap(df, prefix):
    """
    Plots a legible (high contrast) heatmap for the given data frame
    and save the result to `{prefix}genres heatmap.png`
    """
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
    plt.title(f"Popular Generes for Top 10 Anime Over Time")
    plt.savefig(f"{prefix}genres heatmap.png", bbox_inches="tight")


if __name__ == "__main__":
    df = pd.read_csv("full.csv")
    analyze_trend(df)

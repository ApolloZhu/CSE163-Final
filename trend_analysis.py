import pandas as pd
# https://matplotlib.org/examples/color/colormaps_reference.html
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from build_dataset import basic_headers

def analyze_trend(df):
    # Discard anything that doesn't have a user rating (score)
    df = pd.DataFrame(df.dropna(subset=['Score']))
    # Set desired sorting order for season
    df['Season'] = pd.Categorical(df['Season'],
                                  ["winter", "spring", "summer", "fall"])
    # Keep the 10 most popular anime in each season and sum all genres
    grouped = df.groupby(['Year', 'Season']) \
        .apply(lambda season: season.nlargest(10, 'Score', keep='all')) \
        .reset_index(drop=True) \
        .groupby(['Year', 'Season']).sum().dropna()
    # Filter columns to contain only genres in the figure
    only_genres = grouped[grouped.columns.difference(basic_headers)]
    # Get the percentage instead of raw counts
    normalized = only_genres.div(only_genres.sum(axis=1), axis=0)
    normalized.plot.area(figsize=(20,20), fontsize=10, rot=45) #, cmap=cm.brg)
    # The list is quite long, need to include them all
    plt.savefig("trend.png", bbox_inches='tight')

if __name__ == "__main__":
    df = pd.read_csv('full.csv')
    analyze_trend(df)

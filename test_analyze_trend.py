import analyze_trend
import pandas as pd


def main():
    '''
    Test trend analysis on a smaller dataset
    '''
    print("Testing analyze_trend.analyze_trend")
    df = pd.read_csv("sample.csv")
    analyze_trend.analyze_trend(df, "test-")
    print("Tests All Passed: Data Viz")


if __name__ == "__main__":
    main()

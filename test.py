import test_ml_model
import test_build_dataset
import test_analyze_trend


def main():
    test_ml_model.main()
    test_build_dataset.main()
    test_analyze_trend.main()
    print("Tests All Passed")


if __name__ == "__main__":
    main()

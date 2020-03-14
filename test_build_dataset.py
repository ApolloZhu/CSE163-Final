import build_dataset as build


def test_parse_duration():
    '''
    Make sure parse_duration works as documented
    '''
    print("Testing build_dataset.parse_duration")
    assert build.parse_duration("3 hr. 2 min. 1 sec. per ep.") == 183
    assert build.parse_duration("1 hr. 45 min.") == 105
    assert build.parse_duration("23 min. per ep.") == 23
    assert build.parse_duration("42 sec. per ep.") == 1
    assert build.parse_duration("29 sec. per ep.") == 1
    assert build.parse_duration("Unknown") is None
    assert build.parse_duration("N/A") is None
    # The following two are supposed to print ERROR
    assert build.parse_duration("0 sec. per ep.") is None
    assert build.parse_duration("???") is None


def main():
    test_parse_duration()
    print("Tests All Passed: Web Scraping")


if __name__ == "__main__":
    main()

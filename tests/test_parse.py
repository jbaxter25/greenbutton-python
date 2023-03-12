from greenbutton.parse import parse_feed


def test_parse_yields_expected_results():
    ups = parse_feed(
        "C:/Users/jdbax/projects/my-greenbutton-python/tests/testdata/cc_customer_11.xml"
    )

    pass

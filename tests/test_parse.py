from greenbutton.parse import parse_feed
import os


def test_parse_yields_expected_results():
    test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    for root, dirs, files in os.walk(test_data_dir):
        for file in files:
            parse_feed(str(os.path.join(root, file)))
            print(os.path.join(root, file))

    pass

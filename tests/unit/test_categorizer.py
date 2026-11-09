from expense_tracker.categorizer import categorize


def test_categorize_uber_as_transport():
    assert categorize("Uber ride to airport") == "transport"


def test_categorize_lidl_as_groceries():
    assert categorize("Lidl weekly shop") == "groceries"


def test_categorize_unknown_description_as_other():
    assert categorize("Cinema tickets") == "other"

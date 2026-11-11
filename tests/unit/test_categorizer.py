import pytest

from expense_tracker.categorizer import categorize


CATEGORY_CASES = [
    ("Uber ride to airport", "transport"),
    ("Late night taxi home", "transport"),
    ("TAXI Oslo S", "transport"),
    ("Bolt scooter", "transport"),
    ("Ruter monthly ticket", "transport"),
    ("Vy train to Bergen", "transport"),
    ("Flytoget to Gardermoen", "transport"),
    ("Lidl weekly shop", "groceries"),
    ("REMA 1000 Grünerløkka", "groceries"),
    ("rema 1000 majorstuen", "groceries"),
    ("Kiwi minipris", "groceries"),
    ("Coop Extra Storo", "groceries"),
    ("Meny Aker Brygge", "groceries"),
    ("Cinema tickets", "other"),
    ("Netflix subscription", "other"),
    ("Haircut", "other"),
    ("Birthday gift", "other"),
    ("Gym membership", "other"),
    ("Dentist appointment", "other"),
    ("Navy blue sweater", "other"),
    ("Heavy metal concert", "other"),
]


@pytest.mark.parametrize(
    ("description", "expected"),
    CATEGORY_CASES,
    ids=[description for description, _ in CATEGORY_CASES],
)
def test_categorize(description, expected):
    assert categorize(description) == expected


def test_categorize_rejects_blank_description():
    with pytest.raises(ValueError, match="description"):
        categorize("   ")

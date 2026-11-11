import re

KEYWORDS = {
    "transport": ["uber", "taxi", "bolt", "ruter", "vy", "flytoget"],
    "groceries": ["lidl", "rema", "kiwi", "coop", "meny"],
}


def categorize(description: str) -> str:
    if not description.strip():
        raise ValueError("description must not be empty")
    words = set(re.findall(r"\w+", description.lower()))
    for category, keywords in KEYWORDS.items():
        if any(keyword in words for keyword in keywords):
            return category
    return "other"

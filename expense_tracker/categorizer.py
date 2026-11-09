KEYWORDS = {
    "transport": ["uber", "taxi"],
    "groceries": ["lidl", "rema"],
}


def categorize(description: str) -> str:
    text = description.lower()
    for category, keywords in KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "other"

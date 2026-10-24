CATEGORIES = [
    "urgent-important",
    "important-not-urgent",
    "urgent-not-important",
    "neither",
]


CATEGORY_LABELS = {
    "urgent-important": "Urgent + Important",
    "important-not-urgent": "Important, Not Urgent",
    "urgent-not-important": "Urgent, Not Important",
    "neither": "Neither",
}


def create_empty_categories():
    return {category: [] for category in CATEGORIES}


def classify_email(urgent, important):
    if urgent == "YES" and important == "YES":
        return "urgent-important"

    if urgent == "NO" and important == "YES":
        return "important-not-urgent"

    if urgent == "YES" and important == "NO":
        return "urgent-not-important"

    return "neither"
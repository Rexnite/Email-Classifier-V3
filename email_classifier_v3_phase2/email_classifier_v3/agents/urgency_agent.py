import re
from agents.ollama_client import ask_ollama, sanitize_yes_no


PROMOTIONAL_KEYWORDS = [
    "discount",
    "offer",
    "sale",
    "buy now",
    "limited offer",
    "coupon",
    "deal",
    "restaurant",
    "kfc",
    "mcdonald",
    "zomato",
    "swiggy",
    "shop now",
    "promo code",
    "exclusive deal",
    "flat off",
    "% off",
    "cashback",
    "free delivery",
    "order now",
    "limited time offer",
    "new arrivals",
    "clearance sale",
    "festival sale",
    "profile views",
    "new invitations",
    "people viewed your profile",
]


URGENT_KEYWORDS = [
    "asap",
    "urgent",
    "immediately",
    "within 24 hours",
    "within 48 hours",
    "within 2 days",
    "reply within",
    "respond within",
    "action required",
    "final reminder",
    "deadline",
    "due today",
    "due tomorrow",
    "by end of day",
    "eod",
    "submit today",
    "submit tomorrow",
    "expires today",
    "expires tomorrow",
    "meeting today",
    "meeting tomorrow",
    "interview today",
    "interview tomorrow",
    "appointment today",
    "appointment tomorrow",
    "payment due",
    "account locked",
    "unauthorized access",
    "security warning",
]


def is_promotional_email(subject, body):
    text = f"{subject} {body}".lower()

    return any(keyword in text for keyword in PROMOTIONAL_KEYWORDS)


def rule_based_urgency(subject, body):
    text = f"{subject} {body}".lower()

    if is_promotional_email(subject, body):
        if not any(
            keyword in text
            for keyword in [
                "payment failed",
                "payment deducted",
                "refund",
                "account locked",
                "unauthorized",
                "security",
                "order failed",
                "delivery failed",
            ]
        ):
            return "NO"

    for keyword in URGENT_KEYWORDS:
        if keyword in text:
            return "YES"

    if re.search(r"\bby\s+\d{1,2}\s*(am|pm)\b", text):
        return "YES"

    if re.search(r"\bdue\s+(by\s+)?\d{1,2}\s*(am|pm)\b", text):
        return "YES"

    if re.search(r"\bwithin\s+\d{1,2}\s+(hour|hours|day|days)\b", text):
        return "YES"

    return None


def evaluate_urgency(subject, body, model):
    rule_result = rule_based_urgency(subject, body)

    if rule_result:
        return rule_result

    prompt = f"""
You are an Urgency Triage Agent.

Your task is to decide whether this email requires real action from the user soon.

Answer YES if the email requires action within about 48 hours or has an immediate consequence.

Urgent signals:
- urgent
- asap
- immediate
- reply within 24 hours
- reply within 48 hours
- respond within 24 hours
- respond within 48 hours
- action required
- deadline today or tomorrow
- due today or tomorrow
- meeting today or tomorrow
- interview today or tomorrow
- appointment today or tomorrow
- payment due soon
- account locked
- unauthorized access
- important security warning requiring action
- final reminder

Answer NO if:
- it is only a newsletter
- it is only a promotion
- it is only a social notification
- it is only LinkedIn profile views
- it is only generic invitations
- it is a sale/discount/food/shopping offer using fake urgency

Important distinction:
Marketing urgency is NOT real urgency.
"Sale ends today" is not urgent.
"Reply within 48 hours" is urgent.
"Action required" is urgent.
"Payment failed" is urgent.
"Security alert: new login" is urgent.

Examples:

Subject: Urgent reply within 48 hours
Body: What's up?
Urgent: YES

Subject: Meeting tomorrow at 5 PM
Body: Please attend the scheduled client meeting.
Urgent: YES

Subject: Submit assignment by 6 PM today
Body: Please upload before deadline.
Urgent: YES

Subject: KFC offer ends today
Body: Order now and get 50 percent off.
Urgent: NO

Subject: LinkedIn profile views
Body: You're getting noticed.
Urgent: NO

Subject: You have 3 new invitations
Body: See who reached out.
Urgent: NO

Respond ONLY YES or NO.

Email Subject:
{subject}

Email Body:
{body}

Urgent:
"""

    raw_response = ask_ollama(prompt, model)
    return sanitize_yes_no(raw_response)
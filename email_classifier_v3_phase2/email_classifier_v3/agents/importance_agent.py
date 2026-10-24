from agents.ollama_client import ask_ollama, sanitize_yes_no


PROMOTIONAL_KEYWORDS = [
    "discount",
    "offer",
    "sale",
    "coupon",
    "cashback",
    "shop now",
    "buy now",
    "limited offer",
    "restaurant",
    "kfc",
    "mcdonald",
    "zomato",
    "swiggy",
    "myntra",
    "flipkart",
    "amazon sale",
    "food delivery",
    "shoe sale",
    "clothing sale",
    "profile views",
    "people viewed your profile",
    "new invitations",
]


IMPORTANT_KEYWORDS = [
    "reply within",
    "respond within",
    "action required",
    "deadline",
    "due",
    "submit",
    "approval",
    "confirm",
    "timesheet",
    "invoice",
    "payment",
    "payment failed",
    "payment deducted",
    "refund",
    "billing",
    "security alert",
    "account warning",
    "password changed",
    "new login",
    "unauthorized access",
    "account locked",
    "internship",
    "project",
    "assignment",
    "shared with you",
    "google sheets",
    "google docs",
    "bank alert",
    "receipt",
    "verification",
    "meeting invite",
    "interview",
    "professor",
    "college",
    "university",
    "recruiter",
    "client",
    "mentor",
    "official",
    "document",
    "visa",
    "admission",
]


LOW_VALUE_SOCIAL_KEYWORDS = [
    "profile views",
    "you're getting noticed",
    "you are getting noticed",
    "new invitations",
    "see who reached out",
    "people viewed your profile",
    "followers",
    "likes",
    "reactions",
]


def is_promotional_email(subject, body, sender):
    text = f"{subject} {body} {sender}".lower()

    return any(keyword in text for keyword in PROMOTIONAL_KEYWORDS)


def is_low_value_social_email(subject, body, sender):
    text = f"{subject} {body} {sender}".lower()

    return any(keyword in text for keyword in LOW_VALUE_SOCIAL_KEYWORDS)


def rule_based_importance(subject, body, sender):
    text = f"{subject} {body} {sender}".lower()

    if is_low_value_social_email(subject, body, sender):
        if not any(
            keyword in text
            for keyword in [
                "job",
                "interview",
                "recruiter",
                "hiring",
                "application",
                "offer letter",
                "internship",
                "client",
            ]
        ):
            return "NO"

    for keyword in IMPORTANT_KEYWORDS:
        if keyword in text:
            return "YES"

    if is_promotional_email(subject, body, sender):
        if not any(
            keyword in text
            for keyword in [
                "payment failed",
                "payment deducted",
                "refund",
                "billing",
                "fraud",
                "order failed",
                "delivery failed",
                "account locked",
                "security",
            ]
        ):
            return "NO"

    return None


def evaluate_importance(subject, body, sender, model):
    rule_result = rule_based_importance(subject, body, sender)

    if rule_result:
        return rule_result

    prompt = f"""
You are an Importance Evaluation Agent.

Your task is to decide whether this email matters enough that ignoring it could create a real consequence.

Answer YES if ignoring the email could cause:
- missed work
- missed internship/client/project action
- missed academic action
- missed deadline
- missed meeting/interview
- financial loss
- payment or billing issue
- account or security risk
- official document issue
- visa/admission/college issue
- missed direct personal/professional reply
- reputational or professional consequence

Important signals:
- direct reply requested
- reply within a time limit
- action required
- deadline
- due
- submit
- approve
- confirm
- meeting
- interview
- internship
- project
- client
- mentor
- professor
- recruiter
- official document
- payment/refund/billing
- security/account warning

Answer NO if:
- it is only a promotion
- it is only a newsletter
- it is only a generic advertisement
- it is only a LinkedIn profile view notification
- it is only a generic LinkedIn invitation notification
- it is only social engagement
- it has no clear required action or consequence

Hard rules:
- If an email asks for a reply within 48 hours, answer YES.
- If an email asks for confirmation, approval, submission, or action, answer YES.
- LinkedIn profile views are NOT important.
- Generic LinkedIn invitations are NOT important unless they mention job, interview, recruiter, hiring, application, internship, or client.
- Promotions are NOT important unless they involve payment failure, refund, fraud, billing, delivery failure, or account/security issue.

Examples:

Sender: Pranjal Sarkar
Subject: Urgent reply within 48 hours
Body: What's up?
Important: YES

Sender: LinkedIn
Subject: You have 3 new invitations
Body: See who reached out.
Important: NO

Sender: LinkedIn
Subject: 9 profile views
Body: You're getting noticed.
Important: NO

Sender: security@google.com
Subject: Security alert
Body: New sign-in detected.
Important: YES

Sender: support@kfc.com
Subject: Payment deducted but order failed
Body: Your payment was deducted but order failed.
Important: YES

Sender: offers@kfc.com
Subject: KFC offer ends today
Body: Order now and get 50 percent off.
Important: NO

Respond ONLY YES or NO.

Email Sender:
{sender}

Email Subject:
{subject}

Email Body:
{body}

Important:
"""

    raw_response = ask_ollama(prompt, model)
    return sanitize_yes_no(raw_response)
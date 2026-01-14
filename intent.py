def detect_intent(message: str, use_pdf: bool):
    msg = message.lower().strip()

    # =========================
    # DOCUMENT SUMMARY INTENT
    # =========================
    summary_keywords = [
        "summarize",
        "summary",
        "give overview",
        "explain the document",
        "summarise",
        "brief the document"
    ]

    if use_pdf and any(k in msg for k in summary_keywords):
        return "DOCUMENT_SUMMARY"

    # =========================
    # DOCUMENT QUESTION ANSWERING
    # =========================
    if use_pdf:
        return "DOCUMENT_QA"

    # =========================
    # SYSTEM / META MESSAGES
    # =========================
    system_keywords = [
        "i uploaded",
        "i have uploaded",
        "hello",
        "hi",
        "thanks",
        "thank you"
    ]

    if any(k in msg for k in system_keywords):
        return "SYSTEM_MESSAGE"

    # =========================
    # DEFAULT: GENERAL CHAT
    # =========================
    return "GENERAL_CHAT"

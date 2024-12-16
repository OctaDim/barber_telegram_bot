from dataclasses import dataclass


@dataclass
class ENROLL_SRCS_BUTTONS:
    ENROLL_SERVICE: str = "☝️ Enroll"
    CANCEL_SERVICE: str = "🚫 Cancel"
    ENROLL_ONE_MORE: str = "✅️+1  Enroll again"
    CANCEL_ALL_SERVICES: str = "⏹ Cancel all Services"
    # IMPORTANT: Two spaces or special symbol to be unique among inl and reply buttons!!!
    RETURN_TO_MASTERS: str = "↩️  Return"  # Two spaces after icon to be unique!!!
    CONTINUE_ENROLL_SERVICES: str = "👉 Continue Enroll Services"

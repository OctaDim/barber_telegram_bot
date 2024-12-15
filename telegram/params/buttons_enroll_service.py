from dataclasses import dataclass


@dataclass
class ENROLL_SRCS_BUTTONS:
    ENROLL_SERVICE: str = "☝️ Enroll"
    CANCEL_SERVICE: str = "🚫 Cancel"
    ENROLL_ONE_MORE: str = "✅️+1  Enroll again"
    CANCEL_ALL_SERVICES: str = "⏹ Cancel all Services"
    RETURN_TO_MASTERS: str = "↩️ Return"  # !!!MUST BE UNIQUE AMONG REPLY BUTTONS!!!
    CONTINUE_ENROLL_SERVICES: str = "👉 Continue Enroll Services"

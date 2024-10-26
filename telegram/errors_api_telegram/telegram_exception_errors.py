from dataclasses import dataclass


@dataclass
class TG_EXCEPT_ERRORS:
    MSG_NOT_MODIFIED = "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"

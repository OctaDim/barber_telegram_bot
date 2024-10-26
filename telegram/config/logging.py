from dataclasses import dataclass


@dataclass
class LOGGING:
    ORM_RAW_SQL_CONSOLE: bool = False
    EXECUTION_TIME: bool = False
    LAZY_IMPORT_LOGS: bool = True

import importlib
from types import ModuleType

from telegram.config.logging import LOGGING


class DynamicLazyImport:
    _lazy_imported_paths = []

    @property
    def imported_paths(self):
        return self._lazy_imported_paths

    def __call__(self, full_import_path: str) -> object | ModuleType:

        if full_import_path not in self._lazy_imported_paths:
            module_name, obj_name = full_import_path.rsplit('.', 1)

            try:
                lazy_module = importlib.import_module(name=module_name)
                lazy_object = getattr(lazy_module, obj_name)

            except ModuleNotFoundError as error:
                if LOGGING.LAZY_IMPORT_LOGS:
                    print(f"\n\tERROR INFO: Lazy import ERROR. Module not found. "
                          f"Path(name) error\n\t{error}\n")

            except AttributeError as error:
                if LOGGING.LAZY_IMPORT_LOGS:
                    print(f"\n\tERROR INFO: Lazy import ERROR. Object not found. "
                          f"Path(name) error\n\t{error}\n")

            else:
                self._lazy_imported_paths.append(full_import_path)
                if LOGGING.LAZY_IMPORT_LOGS:
                    print(f"\n\tTEST INFO: Lazy import successful\n"
                          f"\tImported module: '{full_import_path}'\n")
                return lazy_object

        return None

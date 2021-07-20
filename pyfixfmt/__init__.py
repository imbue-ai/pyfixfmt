import glob
from argparse import ArgumentParser
from functools import lru_cache
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional

import autoflake
import black
import toml
from isort import SortImports

# TODO: Should make this configurable somehow?
#   Can use this as well: black.find_project_root
PYPROJECT_TOML = "./pyproject.toml"


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--file-glob")
    arg_parser.add_argument("--verbose", action="store_true")

    args = arg_parser.parse_args()

    file_glob = args.file_glob

    if args.verbose:
        print("File Glob: ", file_glob)

    files_to_evaluate = glob.glob(file_glob)

    for file in files_to_evaluate:
        file_path = Path(file)
        if args.verbose:
            print("Formatting: ", file_path)

        run_all_fixers_on_path(file_path)


def run_all_fixers_on_path(file_path: Path) -> None:
    with file_path.open("r") as file_reader:
        original_source = file_reader.read()

    source = run_all_fixers_on_str(file_path, original_source)

    if original_source != source:
        with file_path.open("w") as file_writer:
            file_writer.write(source)


def run_all_fixers_on_str(file_path: Optional[Path], source: str) -> str:
    source = run_autoflake(file_path, source)
    source = run_isort(file_path, source)
    source = run_black(file_path, source)

    return source


def run_autoflake(path: Optional[Path], file_source: str, remove_unused_imports: bool = True) -> str:
    # Just skip some files completely.
    if _do_any_files_match(path, _get_do_not_do_anything_with_imports()):
        return file_source

    # For safe keeping, we're going to make sure that we don't remove unused imports from unexpected places
    if _do_any_files_match(path, _get_do_not_remove_imports()):
        remove_unused_imports = False

    fixed_source = autoflake.fix_code(
        file_source,
        additional_imports=None,
        expand_star_imports=False,
        remove_all_unused_imports=remove_unused_imports,
        ignore_init_module_imports=False,
    )

    return fixed_source


def run_isort(path: Optional[Path], file_source: str) -> str:
    # Just skip some files completely.
    if _do_any_files_match(path, _get_do_not_do_anything_with_imports()):
        return file_source

    default_isort_config = {
        "line_length": 119,
        "case_sensitive": True,
        "skip_glob": "node_modules,mypydir",
        "force_single_line": True,
        "default_section": "FIRSTPARTY",
        "indent": "    ",
        "known_first_party": "tests",
    }

    isort_config = _get_pyproject_configuration().get("tool", {}).get("isort", {})

    for key, value in default_isort_config.items():
        isort_config[key] = isort_config.get(key, value)

    output = SortImports(file_contents=file_source, **isort_config).output
    if output is None:
        return file_source
    else:
        return output


def run_black(_path: Optional[Path], file_source: str) -> str:
    mode = _get_black_config()

    try:
        return black.format_file_contents(src_contents=file_source, fast=True, mode=mode)
    except black.NothingChanged:
        return file_source


def _do_any_files_match(path: Optional[Path], files: Iterable[str]) -> bool:
    if path is None:
        return False

    absolute_path = str(path.absolute())
    return any(do_not_remove_file in absolute_path for do_not_remove_file in files)


@lru_cache()
def _get_pyproject_configuration() -> None:
    try:
        return toml.load(PYPROJECT_TOML)
    except (toml.TomlDecodeError, OSError):
        return {}


@lru_cache()
def _get_formatter_configuration() -> Dict[str, Any]:
    pyproject_configuration = _get_pyproject_configuration()

    return pyproject_configuration.get("tool", {}).get("formatters", {}).get("python", {})


@lru_cache()
def _get_do_not_remove_imports() -> List[str]:
    default_do_not_remove_imports = ["__init__.py"]
    formatter_configuration = _get_formatter_configuration()

    return formatter_configuration.get("do_not_remove_imports", default_do_not_remove_imports)


@lru_cache()
def _get_do_not_do_anything_with_imports() -> List[str]:
    default_do_not_do_anything_with_imports = []
    formatter_configuration = _get_formatter_configuration()

    return formatter_configuration.get("ignore_import_changes", default_do_not_do_anything_with_imports)


@lru_cache()
def _get_black_config() -> black.FileMode:
    default_config = {
        "target_versions": ["PY36"],
        "line_length": 119,
    }

    config = _get_pyproject_configuration()

    for key, value in default_config.items():
        config[key] = config.get(key, value)

    return black.FileMode(
        target_versions={black.TargetVersion[x] for x in config["target_versions"]}, line_length=config["line_length"],
    )


if __name__ == "__main__":
    main()

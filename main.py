import os
from pathlib import Path


def build_directory_tree(root_dir, max_depth=None, current_depth=0, exclude_dirs=None):
    """
    Рекурсивно строит дерево папок для заданной директории.

    Args:
        root_dir (str|Path): Корневая директория для построения дерева
        max_depth (int, optional): Максимальная глубина рекурсии. None - без ограничений
        current_depth (int, optional): Текущая глубина рекурсии (для внутреннего использования)
        exclude_dirs (list, optional): Список имен папок для исключения

    Returns:
        dict: Дерево папок в виде вложенных словарей
    """
    if exclude_dirs is None:
        exclude_dirs = []

    root_dir = Path(root_dir)
    if not root_dir.is_dir():
        raise ValueError(f"'{root_dir}' is not a valid directory")

    tree = {"name": root_dir.name, "type": "directory", "path": str(root_dir), "children": []}

    if max_depth is not None and current_depth >= max_depth:
        return tree

    try:
        with os.scandir(root_dir) as entries:
            for entry in entries:
                if entry.name.startswith('.') or entry.name in exclude_dirs:
                    continue

                if entry.is_dir():
                    child_tree = build_directory_tree(
                        entry.path,
                        max_depth,
                        current_depth + 1,
                        exclude_dirs
                    )
                    tree["children"].append(child_tree)
                elif entry.is_file():
                    tree["children"].append({
                        "name": entry.name,
                        "type": "file",
                        "path": str(Path(entry.path)),
                        "size": entry.stat().st_size
                    })
    except PermissionError:
        tree["error"] = "Permission denied"

    # Сортируем: сначала папки, потом файлы
    tree["children"].sort(key=lambda x: (x["type"] != "directory", x["name"].lower()))

    return tree


def print_directory_tree(tree, indent="", last=True, show_files=True):
    """
    Печатает дерево папок в консоли в удобочитаемом формате.

    Args:
        tree (dict): Дерево папок
        indent (str): Отступ для текущего уровня
        last (bool): Является ли последним элементом в родительской папке
        show_files (bool): Показывать ли файлы
    """
    # Рисуем префикс для текущего элемента
    prefix = "└── " if last else "├── "
    print(indent + prefix + tree["name"])

    new_indent = indent + ("    " if last else "│   ")

    if "children" in tree:
        for i, child in enumerate(tree["children"]):
            if child["type"] == "directory":
                print_directory_tree(child, new_indent, i == len(tree["children"]) - 1, show_files)
            elif show_files and child["type"] == "file":
                file_prefix = "└── " if i == len(tree["children"]) - 1 else "├── "
                print(new_indent + file_prefix + child["name"] + f" ({child['size']} bytes)")


if __name__ == "__main__":
    directory_tree = build_directory_tree(r"C:\Users\andre\CodeReviewer\src\code_reviewer\splitters")
    print_directory_tree(directory_tree)

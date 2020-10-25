from carService.models import Category


def get_category_path(category: Category, path: str):
    category_parent = category.parent
    if category_parent:
        path = path + '>' + category_parent.name
        if category_parent.parent:
            get_category_path(category_parent, path)

    return path

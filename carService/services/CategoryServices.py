from carService.models import Category


def get_category_path(category: Category, path: str):
    category_parent = category.parent
    if category_parent:
        path = path + '>' + category_parent.name
        if category_parent.parent:
            return get_category_path(category_parent, path)

    return path


def factorial(x):
    """This is a recursive function
    to find the factorial of an integer"""

    if x == 1:
        return 1
    else:
        return x * factorial(x - 1)

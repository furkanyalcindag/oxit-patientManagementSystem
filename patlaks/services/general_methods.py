from patlaks.models import Menu


def getMenu(request):
    menus = Menu.objects.all()
    return {'menus': menus}
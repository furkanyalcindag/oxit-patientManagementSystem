import traceback

from django.contrib import auth, messages
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your Views here.
from accounts.serializers.UserSerializer import GroupSerializer


def index(request):
    return render(request, 'accounts/index.html')


# def login(request):
# return render(request, 'registration/login.html')


def login(request):
    if request.user.is_authenticated is True:
        return redirect('booqe:add-blog')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            # return render(request, 'patient/:patient/index', context={})
            return redirect('booqe:add-blog')

        else:
            messages.add_message(request, messages.SUCCESS, 'todo')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


class GroupAPI(APIView):
    def get(self, request, format=None):

        if request.GET.get('id') is None:
            groups = Group.objects.all()

            arr = []
            for group in groups:
                api_data = dict()
                api_data['id'] = group.id
                api_data['groupName'] = group.name
                arr.append(api_data)

            serializer = GroupSerializer(arr, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            group = Group.objects.get(id=int(request.GET.get('id')))
            api_data = dict()
            api_data['id'] = group.id
            api_data['groupName'] = group.name

            serializer = GroupSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            serializer = GroupSerializer(data=request.data, context={'request', request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "group is created"}, status=status.HTTP_200_OK)
            else:
                errors_dict = dict()
                for key, value in serializer.errors.items():
                    if key == 'studentNumber':
                        errors_dict['Öğrenci Numarası'] = value

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            instance = Group.objects.get(id=request.GET.get('id'))
            serializer = GroupSerializer(data=request.data, instance=instance,
                                         context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "group is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            id = request.GET.get('id')
            group = Group.objects.get(id=int(id))
            users = User.objects.filter(groups__name__in=[group.name])
            if len(users) == 0:
                # GroupUrlMethod.objects.filter(group=group).delete()
                group.delete()
                return Response({"message": "user is deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "user is deleted"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)






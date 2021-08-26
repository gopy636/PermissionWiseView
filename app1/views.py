from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .serializers import *
from app1.models import AppUser
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from django.core import serializers
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

@api_view(['POST'])
def create_user(request):
    data=JSONParser().parse(request)
    password = data.get('password',None)
    first_name = data.get('first_name',None)
    last_name = data.get('last_name',None)
    email = data.get('email')
    date_of_birth = data.get('date_of_birth',None)
    photo_url = data.get('photo_url',None)
    is_admin = data.get('is_admin',None)
    if (email is None) or (password is None):
        return Response({"msg":"username and password are required fields"},status=status.HTTP_406_NOT_ACCEPTABLE)
    if is_admin is None:
        return Response({"msg":"please select user as admin or not"},status=status.HTTP_406_NOT_ACCEPTABLE)
    app_user =  AppUser.objects.filter(email = email)
    if len(app_user) ==0:
        user=AppUser.objects.create_user(
                                    username= email,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    is_admin=is_admin,
                                    email = email,
                                    date_of_birth = date_of_birth,
                                    photo_url = photo_url)

        return Response({"msg":f"user created {first_name}"},status=200)
    else:
            return Response({"message":"email already exist","response":[]},status=500)


# @api_view(['POST'])
# def details(request):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     data=JSONParser().parse(request)
#     email = data.get('email',None)
#     password = data.get('password',None)
#     page_size = data.get("page_size",10)
#     page =data.get("page",10)
#     if (email is None) or  (password is None):
#         return Response({"msg":"email and password are required to login"},status=404)
#     try:
#         app_obj = AppUser.objects.get(email = email)
#         if (not app_obj.check_password(password)):
#             return Response("password not match")
#     except Exception as e:
#         return Response({"message": e.__str__(), "response": e.__str__()}, status=400)
#     if app_obj.is_admin == True:
#         a_obj = AppUser.objects.all()
#         app_user_data = AppUserSerializer(a_obj,many=True).data

#         paginator = Paginator(app_user_data, page_size)
#         try:
#             institute_data = paginator.page(page)
#         except PageNotAnInteger:
#             institute_data = paginator.page(1)
#         except EmptyPage:
#             institute_data = paginator.page(paginator.num_pages)
#         meta_data = {
#                         "current_page": institute_data.number,
#                         "total_pages": paginator.num_pages
#                         }
#         list1 = list()
#         for institute_map in institute_data.object_list:
#             list1.append(institute_map)
#         return Response({"message":"success","response":{'test_template_data':list1,"meta_data":meta_data}},status =200)
#     else:
#         return Response({"error": "False",
#                              "message": "success",
#                              "response": {
#                                  #"user_name": app_obj.user_name,
#                                  "email":app_obj.email,
#                                  "date_of_birth":app_obj.date_of_birth,
#                                  "first_name":app_obj.first_name,
#                                  "last_name":app_obj.last_name,
#                                  "is_admin":app_obj.is_admin,
#                                  "photo_url":app_obj.photo_url,
#                              }}, status=200)


@api_view(['GET'])
def user_list(request):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    try:
        print(request.user)
        app_user = AppUser.objects.filter(id=request.user.id)
        for i in app_user:
            if i.is_admin == True:
                 a_obj = AppUser.objects.all()
                 app_user_data = AppUserSerializerAdmin(a_obj, many=True).data
                 return Response({"message": "success", "response": {'admin_data': app_user_data}}, status=200)
            else:
                return Response("not admin user ")
    except Exception as e:
            print(e)
    return Response({"status": 500, "message":"something went wrong"})



class LogInAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data["email"]
                password = serializer.data["password"]
                app_obj = AppUser.objects.get(email=email)
                if app_obj is None:
                    return Response({"status": 400, "result": "Account does not exist"})
                app_obj.check_password(password)
                jwt_token = RefreshToken.for_user(app_obj)
                return Response({"status": 200,
                 "result": "Login successfull", 
                 "token": str(jwt_token.access_token)
                 })
            return Response({"status": 400, "error": serializer.errors})
        except Exception as e:
            print(e)
        return Response({"status": 500, "message":"something went wrong"})

@api_view(['GET'])
def details(request):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    try:
         print(request.user)
         app_user = AppUser.objects.filter(id=request.user.id)
         for i in app_user:
             if i.is_admin == True:
                 a_obj = AppUser.objects.all()
                 app_user_data = AppUserSerializer(a_obj, many=True).data
                 return Response({"message": "success", "response": {'admin_data': app_user_data}}, status=200)
             else:
                #serialized_qs = serializers.serialize('json', app_user)
                serializer=AppUserSerializer(i).data
                return Response({"message": "success", "response": {
                    'data': serializer}}, status=200)
    except Exception as e:
             print(e)
             return Response({"error":"Unable to access"}, status=400)

        

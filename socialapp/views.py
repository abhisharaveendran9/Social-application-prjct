from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from socialapp.serializers import UserSerializer,UserProfileSerializer,PostSerializer,CommentSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from socialapp.models import UserProfile,Posts,Comments
from rest_framework.decorators import action

# Create your views here.

class UserRegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self,request,*args,**kwargs):
        serializer=UserProfileSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    #api/v1/users/profile/{1}/follow
    #request.user=mohanlal
    #id=1 asif
    @action(methods=["post"],detail=True)
    def follow(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user_to_follow=User.objects.get(id=id)
        profile=UserProfile.objects.get(user=request.user)
        profile.following.add(user_to_follow)
        return Response({"msg":"ok"})

    #api/v1/users/profile/my_followings  , method GET
    @action(methods=["get"],detail=False)
    def my_followings(self,request,*args,**kwargs):
        # user=request.user
        # user_profile=UserProfile.object.get(user=user)
        # followings=user_profile.following.all()
        get_followings=request.user.following.all()
        serializer=UserProfileSerializer(get_followings,many=True)
        return Response(data=serializer.data)



class PostsView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    #localhost:8000/api/v1/posts/{postpk}/add_comment
    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        user=request.user
        serializer=CommentSerializer(data=request.data,
                                     context={"post":post,
                                              "user":user
                                              })
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # localhost:8000/api/v1/posts/{postpk}/get_comment
    @action(methods=["get"], detail=True)
    def get_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        comments=post.comments_set.all()
        serializer=CommentSerializer(comments,many=True)
        return Response(data=serializer.data)

    # localhost:8000/api/v1/posts/{postpk}/add_like
    @action(methods=["post"],detail=True)
    def add_like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        post.liked_by.add(request.user)
        return Response({"message":"ok"})
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from demo.models import Blog
from demo.serializers import BlogModelSerializer


@csrf_exempt
def blog_list(request):
    if request.method == 'GET':
        posts = Blog.objects.all()
        serializer = BlogModelSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BlogModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)


@csrf_exempt
def blog_detail(request, pk):
    """try:
        post = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return HttpResponse(status=404)"""

    if request.method == 'GET':
        try:
            post = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return HttpResponse(status=404)
        serializer = BlogModelSerializer(post)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        try:
            post = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return HttpResponse(status=404)
        data = JSONParser().parse(request)
        serializer = BlogModelSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.error, status=400)

    elif request.method == 'DELETE':
        try:
            post = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return HttpResponse(status=404)
        post.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def post_list(request, format=None):
    """List all blog post or create new one"""
    """We can return multiple type response using format as xml, json
    we just have to call as /blog/4.json/"""
    if request.method == 'GET':
        posts = Blog.objects.all()
        serializer = BlogModelSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlogModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk, format=None):
    """detail for a single post"""
    try:
        post = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogModelSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BlogModelSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostList(APIView):
    def get(self, request, format=None):
        posts = Blog.objects.all()
        serializer = BlogModelSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BlogModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    """Retrieve, update and delete operations, Now we don't have access to pk outside get/put/delete
    methods hence we have to fetch object using pk in every function. To reuse the code we can
    over ride our get_object method which below methods will nee to retrieve object using pk"""

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = BlogModelSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = BlogModelSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostListUsingMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """Mixin provides the functionality of create and list while genericAPIView core functionality
    of view class"""
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetailUsingMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostListGenericClassBasedView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer


class PostDetailGenericClassBasedViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer

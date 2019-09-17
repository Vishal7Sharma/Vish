from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from demo.views import (blog_detail, blog_list, post_list, post_detail,
                        PostList, PostDetail, PostDetailUsingMixin, PostListUsingMixin,
                        PostListGenericClassBasedView, PostDetailGenericClassBasedViews,
                        UserList, UserDetail, UserViewSet, PostViewSet, api_root)

"""urlpatterns = [
    path('blog/', PostListGenericClassBasedView.as_view()),
    path('blog/<int:pk>/', PostDetailGenericClassBasedViews.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
"""
""" Because the api can chooses the content type of response based on client request, it 
will by default return an html response in browser
MAKE SURE YOU HAVE REST_FRAMEWORK IN SETTINGS-> INSTALLED_APPS, THEN ONLY IT WILL BE ABLE TO 
CREATE AN HTML RESPONSE OF YOUR SERIALIZER/MODEL/RESPONSE.
"""

# Creating multiple views from view set by binding this to http methods and actions for each view

"""post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

# creating url patterns and adding actions 
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('posts/', post_list, name='post-list'),
    path('posts/<int:pk>/', post_detail, name='post-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])"""

""" We are using view set so we dont have to design our URL conf
Conventions for wiring up resources into views and urls can be handled automatically using router"""

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)
# The API urls are not determined by router
urlpatterns = [
    path('', include(router.urls)),
]
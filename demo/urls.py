from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from demo.views import (blog_detail, blog_list, post_list, post_detail,
                        PostList, PostDetail, PostDetailUsingMixin, PostListUsingMixin,
                        PostListGenericClassBasedView, PostDetailGenericClassBasedViews
                        )

urlpatterns = [
    path('blog/', PostListGenericClassBasedView.as_view()),
    path('blog/<int:pk>/', PostDetailGenericClassBasedViews.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

""" Because the api can chooses the content type of response based on client request, it 
will by default return an html response in browser
MAKE SURE YOU HAVE REST_FRAMEWORK IN SETTINGS-> INSTALLED_APPS, THEN ONLY IT WILL BE ABLE TO 
CREATE AN HTML RESPONSE OF YOUR SERIALIZER/MODEL/RESPONSE.
"""

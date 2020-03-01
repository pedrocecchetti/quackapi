from .models import BlogPost
from rest_framework.viewsets import ModelViewSet
from .serializers import BlogPostSerializer

# Create your views here
class PostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

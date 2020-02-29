import uuid

from django.db import models


class BlogPost(models.Model):
    """
    This Class implements all the information related to all the blog posts that will
    be hosted on a post
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=128, verbose_name='Título')
    text = models.TextField(verbose_name='Texto Completo')

    author = models.ForeignKey(to='users.User', on_delete=models.SET_NULL, null=True)

    # Monitoring
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ultima atualização")

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return f'{self.title - self.author.get_full_name()}'

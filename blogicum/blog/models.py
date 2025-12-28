from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Класс 1 - ОТДЕЛЬНО
class Category(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

# Класс 2 - ОТДЕЛЬНО (не внутри Category!)
class Location(models.Model):
    name = models.CharField(max_length=256)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Класс 3 - ОТДЕЛЬНО (не внутри Location!)
class Post(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']  # Сортировка: старые → новые

    def __str__(self):
        return f'Комментарий {self.author} к посту {self.post.id}'
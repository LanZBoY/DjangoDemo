from django.db import models

# Create your models here.
from django.urls import reverse
import uuid


class Genre(models.Model):
    # 設定種類名稱，help_text 代表幫助使用者提示要輸入什麼
    name = models.CharField(max_length=200, help_text='輸入書本種類')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    # 在網站 https://media.prod.mdn.mozit.cloud/attachments/2019/02/09/16479/e26dc9174dd40f177acaca19a33b4667/local_library_model_uml.png
    # 外鍵 第一個參數代表你對外指定的資料表，on_delete 則可以設定 如果被指定的那個資料表被刪除了這邊的欄位設定為什麼
    # null 如果為True代表 django會將欄位不輸入的地方填入null值 預設為False
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='輸入有關這本書的描述')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 個字 格式參照:<a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='選擇這本書的種類')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    # 在管理端網站當中如果建立這個method則會顯示 這個APP相關的URL
    # 利用 URL mapper來達到轉換的效果
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """UUID 代表在資料庫中每一本書有一個特殊的識別值，如果設定參數default = uuid.uuid4 則會自動建立 特殊識別值"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='對於這本書在這個資料庫的Unique ID')
    # 外鍵對應Bool model
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    # 如果
    due_back = models.DateField(null=True, blank=True)
    # Enum 用法
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    # 在這裡定義 choices 參數為 Enum LOAN_STATUS 代表這個是可選的四種狀態，而default為m
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='顯示書本的租借狀態',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

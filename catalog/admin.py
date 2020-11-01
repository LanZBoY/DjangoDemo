from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
# 管理端如果不註冊 model則會發現 如果有些地方外鍵需要指定到 其他model會發現 無法自定義的增加
# 這邊同時也呈現了管理端 是否可以修該這些model的差別 體現了django 對於 權限管控的強大功能
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Language)

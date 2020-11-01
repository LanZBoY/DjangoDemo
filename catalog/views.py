from django.http import Http404
from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre


# Create your views here.
def index(request):
    # 在指定物件撈出所有資料並回傳個數
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # 找書本 status 狀態為 'a' 個數
    # 這邊可以發現filter部分 會因為你的model有不同的輸入參數，再根據不同的輸入參數輸出不同的結果
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # 在預設 如果沒有的情況下all() method 是可以省略的
    # 但根據軟體工程物件導向設計原則 不建議省略
    num_authors = Author.objects.count()
    # 將要寫入html的
    # session 機制說明，這個session主要存在伺服器中，會根據瀏覽器的使用者資訊做不同的計算
    # 在資料結溝中他主要是key,value的結構
    num_visits = request.session.get('num_visits', 0);
    request.session['num_visits'] = num_visits + 1;
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }
    # 利用 render() 來渲染html 以及將context內容傳到html模板中
    return render(request, 'index.html', context=context)


# 我自己創的function
# def getBooks(request):
#     books_list = Book.objects.all()
#
#     context = {
#         'books': books_list
#     }
#     return render(request, 'book.html', context=context)


def getAuthors(request):
    authors_list = Author.objects.all()
    context = {
        'authors': authors_list
    }

    return render(request, 'authors.html', context=context)


# 用class繼承泛型.ListView的方式書本寫法
class BookListView(generic.ListView):
    # 透過overwrite的方式將model 設定為Book 指定說 這裡要render傳入的參數為Book
    model = Book
    # context_object_name 設定在context進去到 template render時 所設定的變數名稱
    # 這邊可以隨意定義名稱，而在HTML上面也要注意模板問題
    context_object_name = 'my_book_list'
    # 這邊向資料庫取得 所有書本的資料
    # queryset 利用overwrite的方式可以定義要哪一個資料
    # 這邊要注意的是因為原始碼本身就有將model找全部資料的method
    # 所以這邊如果定義 queryset = Book.objects.all() 這行是沒有意義的
    # 但如果要讓code的可讀性更佳，或是如果你只想列幾個書本的話可以利用filter method的方式來達到特化的效果
    queryset = Book.objects.all()
    # 設定分頁參數
    # 在django架構中，設定這個參數他會在__init__時設定好取得的大小分頁
    # 如果對於細節有興趣，請對 下面變數成員用Ctrl + 左鍵 取得reference
    paginate_by = 10
    # 目前需要了解一下如果不特別定義的話這個東西到底怎麼運作
    template_name = 'book_list.html'

    # 預設本來就會根據原始Model的形式回傳物件內容
    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        # 透過這個method 可以知道，他不僅繼承的原本的,method
        # 而且還可以彈性的增加資料的項目
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = '就是一些資料'
        return context


class BookDetailView(generic.DetailView):
    # 所以根據上面所說的理解，正常來說
    # 這個class 可以簡化為1行(當然上面的也可以，只是不建議這麼做)
    model = Book
    # 這裡要注意一點 如果沒有特別定義
    # 以這個專案來說他預設會找 DjangoDemo/catalog/*
    # note:這邊還不確定 其運作原理 剛剛稍微試了一下 不是我想的那樣 但是錯誤卻說找不到在catalog/book_detail.html那理論是應該將檔案放到catalog/下面就可以運作但不是如此
    # 裡面的看有沒有要的東西
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "Authors_List"
    queryset = Author.objects.all()
    paginate_by = 10
    template_name = "Author_List.html"

    def get_queryset(self):
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        return context


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "author_detail.html"
    # queryset = Book.objects.filter(author_id=Author.pk)
    #
    # def get_queryset(self):
    #     return Book.objects.filter(author_id=Author.pk)
    #
    # def get_context_data(self, **kwargs):
    #     context = super(AuthorDetailView,self).get_context_data(**kwargs)
    #     context['book'] = self.queryset

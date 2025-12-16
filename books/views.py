from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseForbidden
from .models import Category, SubCategory, Book
from .forms import BookUploadForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import mimetypes

def paginate_queryset(request, queryset, per_page=12):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    return page_obj

def home(request):
    categories = Category.objects.all()
    recent_books = Book.objects.order_by('-uploaded_at')[:8]
    return render(request, 'books/home.html', {'categories': categories, 'recent_books': recent_books})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'books/category_list.html', {'categories': categories})


def subcategory_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = category.subcategories.all()
    return render(request, 'books/subcategory_list.html', {'category': category, 'subcategories': subcategories})


# def book_list(request, category_slug, subcategory_slug=None):
#     category = get_object_or_404(Category, slug=category_slug)
#     if subcategory_slug:
#         subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category)
#         books = subcategory.books.all()
#     else:
#         books = category.books.all()
#     return render(request, 'books/book_list.html', {'category': category, 'books': books})
def book_list(request, category_slug, subcategory_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category)
        books_qs = subcategory.books.order_by('-uploaded_at').all()
    else:
        books_qs = category.books.order_by('-uploaded_at').all()

    # optional inline search within category/subcategory
    q = request.GET.get('q', '')
    if q:
        books_qs = books_qs.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q) |
            Q(description__icontains=q)
        )

    page_obj = paginate_queryset(request, books_qs, per_page=12)
    return render(request, 'books/book_list.html', {
        'category': category,
        'books': page_obj,  # page object
        'q': q
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


# Download using FileResponse so large files stream efficiently
def book_download(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Optionally restrict downloads to logged-in users
    # if not request.user.is_authenticated:
    # return HttpResponseForbidden('Login required to download')
    fpath = book.file.path
    mime_type, _ = mimetypes.guess_type(fpath)
    response = FileResponse(open(fpath, 'rb'), as_attachment=True, filename=book.file.name.split('/')[-1])
    if mime_type:
        response['Content-Type'] = mime_type
    return response


@login_required
def upload_book(request):
# Only allow staff to upload in this example. Remove staff check if you want all users to upload.
    if not request.user.is_staff:
        return HttpResponseForbidden('Only staff may upload books')


    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books:home')
    else:
        form = BookUploadForm()
    return render(request, 'books/upload.html', {'form': form})


# # New: site-wide search view
# def search(request):
#     q = request.GET.get('q', '').strip()
#     results = Book.objects.none()
#     if q:
#         results = Book.objects.filter(
#             Q(title__icontains=q) |
#             Q(author__icontains=q) |
#             Q(description__icontains=q) |
#             Q(category__name__icontains=q) |
#             Q(subcategory__name__icontains=q)
#         ).order_by('-uploaded_at')

#     page_obj = paginate_queryset(request, results, per_page=12)
#     return render(request, 'books/search_results.html', {
#         'q': q,
#         'books': page_obj
#     })

def search_results(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    return render(request, 'books/search_results.html', {
        'query': query,
        'results': results
    })
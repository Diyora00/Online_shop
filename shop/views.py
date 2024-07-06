from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from shop.forms import *
from django.contrib import messages
from shop.models import Product, Category, Order, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# from django.contrib.auth.decorators import login_required


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    search_post = request.GET.get('search')
    order = request.GET.get('order')

    p = Paginator(products, 4)
    page_number = request.GET.get('page', 1)

    try:
        products = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        products = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        products = p.page(p.num_pages)

    if search_post:
        products = products.filter(Q(name__icontains=search_post) | Q(price__icontains=search_post))

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if order == 'expensive':
        products = products.order_by('-price')
    elif order == 'cheap':
        products = products.order_by('price')

    context = {
        'products': products,
        'categories': categories,
        'order': order,
    }
    return render(request, 'shop/product-list.html', context)


# Create your views here.
def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    pk = product.category_id
    products = Product.objects.all()
    search_post = request.GET.get('search')

    if search_post:
        products = products.filter(Q(name__icontains=search_post) | Q(price__icontains=search_post))
        return render(request, 'shop/product-list.html', {'products': products})
    products = products.filter(category_id=pk)
    products = products.exclude(id=product.id)[0:4]

    # comments = Comment.objects.all()
    # comments = comments.filter(product_id=product.id)

    comments = product.comments.all().filter(is_appropriate=True)

    context = {'product': product, 'products': products, 'comments': comments}

    return render(request, 'shop/detail.html', context)


def make_order(request, slug):
    product = Product.objects.get(slug=slug)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        quantity = request.POST.get('quantity')
        order = Order(name=name, email=email, quantity=quantity, product_id=product.id)
        if form.is_valid():
            order.save()
            messages.add_message(request, messages.SUCCESS, 'Order successfully added!.')
            return redirect('product_details', slug=slug)
    else:
        form = OrderForm(request.GET)

    return render(request, 'shop/detail.html', {'form': form, 'product': product})


def add_comment(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.product = product
            comments.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been added.')
            return redirect('product_details', slug=product_slug)
    else:
        form = CommentModelForm(request.GET)

    return render(request, 'shop/detail.html', {'form': form, 'product': product})


# @login_required(login_url='/products/')
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        form.slug = request.POST.get('slug')

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product added successfully.')
            return redirect('products')
    else:
        form = AddProductForm()
    return render(request, 'shop/add_product.html', {'form': form})


def delete_product(request, slug):
    product = Product.objects.get(slug=slug)
    if request.method == 'POST':
        product.delete()
        messages.add_message(request, messages.SUCCESS, 'Product deleted successfully.')
        return redirect('products')

    return render(request, 'shop/delete_product.html', {'product': product})


def update_product(request, slug):
    product = Product.objects.get(slug=slug)
    form = AddProductForm(instance=product)

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product updated successfully.')
            return redirect('products')

    return render(request, 'shop/update_product.html', {'form': form, 'product': product})


def about(request):
    return render(request, 'shop/about.html')

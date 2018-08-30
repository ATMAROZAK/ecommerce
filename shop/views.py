from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Subcategory

# Страница с товарами
def ProductList(request, category_slug=None, subcategory_slug=None):
    category = None
    subcategory = None
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug: #Если есть категория
        category = get_object_or_404(Category, slug=category_slug)

        if subcategory_slug: #Если есть категория и подкатегория
            subcategory = get_object_or_404(Subcategory, slug=subcategory_slug, category=category)
            products = products.filter(subcategory=subcategory)
            return render(request, 'shop/list.html', {
                'categories': categories,
                'subcategories': subcategories,
                'products': products,
                'category' : category,
                'subcategory' : subcategory
            })

        else: #Если есть категория но нет подкатегории
            products = products.filter(category=category)
            return render(request, 'shop/list.html', {
                'categories': categories,
                'subcategories': subcategories,
                'products': products,
                'category': category
            })

    else: #Если нет категории
        return render(request, 'shop/index.html', {
            'categories': categories,
            'subcategories' : subcategories,
            'products': products,
        })

# Страница товара
def ProductDetail(request, brand_slug, slug):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    product = get_object_or_404(Product, brand__slug=brand_slug, slug=slug, available=True)
    return render(request, 'shop/detail.html', {'product': product,
                                                'categories' : categories,
                                                'subcategories': subcategories})
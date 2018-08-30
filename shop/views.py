from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Subcategory

# Страница с товарами
def ProductList(request, category_slug=None, subcategory_slug=None):
    category = None
    subcategory = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug: #Если есть категория
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = Subcategory.objects.filter(category=category)

        if subcategory_slug: #Если есть категория и подкатегория
            subcategory = get_object_or_404(Subcategory, slug=subcategory_slug, category=category)
            products = products.filter(subcategory=subcategory)
            return render(request, 'shop/list.html', {
                'subcategories': subcategories,
                'products': products
            })

        else: #Если есть категория но нет подкатегории
            products = products.filter(category=category)
            return render(request, 'shop/list.html', {
                'subcategories': subcategories,
                'products': products
            })

    else: #Если нет категории
        subcategories = Subcategory.objects.all()
        return render(request, 'shop/list.html', {
            'categories': categories,
            'subcategories' : subcategories,
            'products': products
        })

# Страница товара
def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'base.html', {'product': product})
from django.shortcuts import render, get_object_or_404


from .models import Category, Product

def category_list(request):
    print(f"{Category.image if Category.image else 'No Image File'}")
    categories = Category.objects.all()
    return render(request, 'product/category_list.html', {'categories': categories})


def product_list(request, category_slug=None):
    """
    View to display a list of products, optionally filtered by a category.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'product/product_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

# # You might also want a product detail view
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # logic for cart can be added here
    return render(request, 'product/product_detail.html', {'product': product})
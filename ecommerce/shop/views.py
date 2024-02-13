from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Count
from .models import Campaign, Category, Product,Size,Color
from customer.models import Review
from customer.models import Customer
from django.core.paginator import Paginator
from django.db.models import Avg
from .filters import ProductFilter










def home(request):
    slide_campaigns = Campaign.objects.filter(is_slide=True)[:3]
    nonslide_campaigns = Campaign.objects.filter(is_slide=False)[:4]
    categories = Category.objects.annotate(product_count=Count('products'))
    featured_products = Product.objects.filter(featured=True)[:8]
    recent_products = Product.objects.all().order_by('-created')[:8]
    return render(request, 'home.html', {
        'slide_campaigns': slide_campaigns,
        'nonslide_campaigns': nonslide_campaigns,
        'categories': categories,
        'featured_products': featured_products,
        'recent_products': recent_products
    })



def product_list(request):
    products = Product.objects.all().annotate(avg_star=Avg('reviews__star_count'))

    search_input = request.GET.get('search')
    if search_input:
        products = products.filter(title__icontains=search_input)

    sorting_input = request.GET.get('sorting')
    if sorting_input:
        products = products.order_by(sorting_input)

    
    
    product_filter=ProductFilter(request.GET,queryset=products)
    products=product_filter.qs
    page_by_input = int(request.GET.get('page_by', 3))
    page_input = request.GET.get('page', 1)
    paginator = Paginator(products, page_by_input)


    try:
        page = paginator.page(page_input)
        products=page.object_list
    except:
        page=paginator.page(1)
        products=page.object_list

    colors=Color.objects.all().annotate(product_count=Count('products'))
    sizes=Size.objects.all().annotate(product_count=Count('products'))

    

    return render(request, 'product-list.html', {
        'products': page.object_list,
        'page': page,
        'paginator':paginator,
        'sizes':sizes,
        'colors':colors,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    has_review = False

    if request.user.is_authenticated and hasattr(request.user, 'customer'):
        has_review = Review.objects.filter(customer=request.user.customer, product=product).exists()

    other_products = Product.objects.exclude(pk=product.pk).order_by('?')[:5]

    return render(request, 'product-detail.html', {
        'product': product,
        'other_products': other_products,
        'has_review': has_review
    })


def review(request, pk):
    if request.method == 'POST':
        if not hasattr(request.user, 'customer'):
           Customer.objects.create(user=request.user)
        customer = request.user.customer
        product = get_object_or_404(Product, pk=pk)
        if Review.objects.filter(customer=customer, product=product).exists():
            return HttpResponse(status=403)
        star_count = int(request.POST.get('star_count'))
        comment = request.POST.get('comment')
        review = Review.objects.create(
            customer=customer, product=product,
            comment=comment, star_count=star_count
        )
        return redirect('shop:product-detail', pk=pk)
    return redirect('shop:product-detail', pk=pk)

    
 


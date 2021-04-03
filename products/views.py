from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Product, Category


class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/product_list.html'
    paginate_by = 10


class ProductCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/category.html'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(ProductCategory, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['active'] = 'shop'
        return context


def stock_alerts_view(request):
    """Getting a list of products with less than 10 stock"""
    alerts_list = Product.objects.filter(stock__in=range(0, 11))

    page = request.GET.get('page', 1)
    paginator = Paginator(alerts_list, 8)

    try:
        alerts = paginator.page(page)
    except PageNotAnInteger:
        alerts = paginator.page(1)
    except EmptyPage:
        alerts = paginator.page(paginator.num_pages)

    context = {
        'alerts': alerts
    }

    return render(request, 'products/stock_alerts.html', context)

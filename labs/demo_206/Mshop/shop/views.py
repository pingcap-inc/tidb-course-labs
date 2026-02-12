"""
Shop views - same logic and intent as demo_205 Laravel (ProductsController, TransactionController).
"""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.conf import settings

from .models import Product, ProductType, PayType, Transaction
from .forms import ProductUpdateForm, BuyForm

User = get_user_model()

# --- Helpers (i18n strings matching Laravel shop.php) ---
def _t(key, default=''):
    from .locale_strings import get
    return get(key, default)


# --- Products (same as ProductsController) ---

def product_list(request):
    """List products for sell (status S). Paginate 10."""
    qs = Product.objects.filter(status=Product.STATUS_S).exclude(name='').order_by('-updated_at')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    base = request.build_absolute_uri(reverse('shop:product_list')).split('?')[0]
    return render(request, 'shop/products/list_product.html', {
        'title': _t('product.Book-list'),
        'page_obj': page_obj,
        'pagination_base_path': base,
    })


def product_manage(request):
    """Manage products (admin list). Exclude deleted and blank name. Paginate 10."""
    qs = Product.objects.exclude(status=Product.STATUS_D).exclude(name='').order_by('-created_at')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    base = request.build_absolute_uri(reverse('shop:product_manage')).split('?')[0]
    return render(request, 'shop/products/manage_product.html', {
        'title': _t('product.Book-management'),
        'page_obj': page_obj,
        'pagination_base_path': base,
    })


def product_create(request):
    """Create a new product (draft) and redirect to edit."""
    Product.objects.filter(name='').delete()
    Product.objects.filter(price=0).delete()
    product = Product.objects.create(
        status=Product.STATUS_C,
        name='',
        introduction='',
        photo=None,
        price=0,
        remain_count=0,
    )
    return redirect('shop:product_edit', product_id=product.pk)


def product_show(request, product_id):
    """Show single product and buy form."""
    product = get_object_or_404(Product, pk=product_id)
    pay_types = PayType.objects.all()
    buy_quantity_choices = list(range(1, min(product.remain_count, 10) + 1)) if product.remain_count else [1]
    return render(request, 'shop/products/show_product.html', {
        'title': _t('product.Product-details'),
        'product': product,
        'pay_types': pay_types,
        'buy_quantity_choices': buy_quantity_choices,
    })


def product_edit(request, product_id):
    """Edit product form."""
    product = get_object_or_404(Product, pk=product_id)
    product_types = ProductType.objects.all()
    photo_display = product.photo or ''
    prefix = getattr(settings, 'URL_PREFIX', '') or ''
    if photo_display and not photo_display.startswith('http'):
        photo_display = f"{prefix}{photo_display}" if prefix else photo_display
    form = ProductUpdateForm(instance=product)
    return render(request, 'shop/products/edit_product.html', {
        'title': _t('product.Book-update'),
        'product': product,
        'product_types': product_types,
        'photo_display': photo_display,
        'form': form,
    })


def product_update(request, product_id):
    """Update product (POST). Same validation as Laravel."""
    product = get_object_or_404(Product, pk=product_id)
    if request.method != 'POST':
        return redirect('shop:product_edit', product_id=product_id)
    form = ProductUpdateForm(request.POST, request.FILES, instance=product)
    if not form.is_valid():
        photo_display = product.photo or ''
        prefix = getattr(settings, 'URL_PREFIX', '') or ''
        if photo_display and not photo_display.startswith('http'):
            photo_display = f"{prefix}{photo_display}" if prefix else photo_display
        return render(request, 'shop/products/edit_product.html', {
            'title': _t('product.Book-update'),
            'product': product,
            'product_types': ProductType.objects.all(),
            'photo_display': photo_display,
            'form': form,
        })
    photo_path = product.photo
    if request.FILES.get('photo_upload'):
        import uuid
        f = request.FILES['photo_upload']
        ext = f.name.split('.')[-1] if '.' in f.name else 'png'
        name = f"{uuid.uuid4().hex[:12]}.{ext}"
        media_root = getattr(settings, 'MEDIA_ROOT', None) or (settings.BASE_DIR / 'media')
        full_dir = media_root / 'assets' / 'images'
        full_dir.mkdir(parents=True, exist_ok=True)
        full_path = full_dir / name
        with open(full_path, 'wb') as out:
            for chunk in f.chunks():
                out.write(chunk)
        photo_path = f'/assets/images/{name}'
    form.save(photo_path=photo_path)
    return redirect('shop:product_manage')


def product_destroy(request, product_id):
    """Soft delete: set status to D."""
    if request.method != 'POST':
        return redirect('shop:product_manage')
    product = get_object_or_404(Product, pk=product_id)
    product.status = Product.STATUS_D
    product.save(update_fields=['status'])
    return redirect('shop:product_manage')


def product_buy(request, product_id):
    """Process purchase - same transaction logic as Laravel executeTransaction."""
    product = get_object_or_404(Product, pk=product_id)
    if request.method != 'POST':
        return redirect('shop:product_show', product_id=product_id)
    form = BuyForm(request.POST)
    if not form.is_valid():
        messages.error(request, form.errors.as_text())
        return redirect('shop:product_show', product_id=product_id)
    buy_count = form.cleaned_data['buy_count']
    pay_type_id = form.cleaned_data['pay_with']
    user_id = 1  # hardcoded as in Laravel
    user = get_object_or_404(User, pk=user_id)
    pay_type = get_object_or_404(PayType, pk=pay_type_id)
    try:
        with db_transaction.atomic():
            product = Product.objects.select_for_update().get(pk=product_id)
            remain = product.remain_count - buy_count
            if remain < 0:
                raise ValueError(_t('Message.Insufficient-goods') or 'Insufficient quantity of goods, unable to purchase.')
            product.remain_count = remain
            product.save(update_fields=['remain_count'])
            total_price = buy_count * product.price
            txn = Transaction.objects.create(
                user=user,
                product=product,
                price=product.price,
                buy_count=buy_count,
                total_price=total_price,
                pay_type=pay_type,
            )
        messages.success(request, _t('Message.Purchase-successfully') or 'Purchase Successful!')
        return redirect('shop:transaction_show', transaction_id=txn.pk)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('shop:product_show', product_id=product_id)


# --- Transactions (same as TransactionController) ---

def transaction_list(request):
    """All transactions, ordered by created_at desc, then id desc. Paginate 10. Path for pagination."""
    qs = Transaction.objects.select_related('product', 'user', 'pay_type').order_by('-created_at', '-id')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    base = request.build_absolute_uri(reverse('shop:transaction_list')).split('?')[0]
    return render(request, 'shop/transactions/list_transaction.html', {
        'title': _t('transaction.Transactions-list'),
        'page_obj': page_obj,
        'pagination_base_path': base,
    })


def transaction_show(request, transaction_id):
    """Single transaction detail."""
    txn = get_object_or_404(Transaction.objects.select_related('product', 'user', 'pay_type'), pk=transaction_id)
    return render(request, 'shop/transactions/show_transaction.html', {
        'title': _t('transaction.Order-details'),
        'transaction': txn,
    })


def transaction_list_user(request, user_id):
    """Transactions for one user. Paginate 10."""
    qs = Transaction.objects.filter(user_id=user_id).select_related('product', 'user', 'pay_type').order_by('-created_at', '-id')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    base = request.build_absolute_uri(reverse('shop:transaction_list_user', kwargs={'user_id': user_id})).split('?')[0]
    return render(request, 'shop/transactions/list_user_transaction.html', {
        'title': _t('transaction.Your-histroy-orders'),
        'page_obj': page_obj,
        'pagination_base_path': base,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Products, Inventory
from .forms import ProductForm
import csv
from django.core.paginator import Paginator
from datetime import datetime
import zoneinfo
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@login_required
def index(request):
    products = Products.objects.select_related("inventory").filter(user=request.user).order_by("id")
    paginator = Paginator(products, 10)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    current = page_obj.number
    total = paginator.num_pages
    page_range = []
    for i in range(1, total + 1):
        if i == 1 or i == total or (current - 2 <= i <= current + 2):
            page_range.append(i)
        elif page_range[-1] != "...":
            page_range.append("...")
    context = {"page_obj": page_obj, "page_range": page_range}
    return render(request, "inventory/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            logger.info("form is valid")
            with transaction.atomic():
                body = request.POST
                name = body.get("name")
                sku = body.get("sku")
                description = body.get("description")
                price = int(body.get("price").replace(",", ""))
                user_id = request.user.id
                product = Products(
                    name=name,
                    sku=sku,
                    description=description,
                    price=price,
                    user_id=user_id,
                )
                product.save()
                quantity = body.get("quantity")
                inventory = Inventory(quantity=quantity, product=product)
                inventory.save()
            messages.success(request, "商品の追加に成功しました")
            return redirect("inventory-index")
    else:
        form = ProductForm(
            initial={
                "name": "",
                "sku": "",
                "description": "",
                "price": "",
                "quantity": "",
            }
        )
    context = {"form": form}
    return render(request, "inventory/create.html", context)


@login_required
def detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id, user=request.user)
    form = ProductForm(
        initial={
            "name": product.name,
            "sku": product.sku,
            "description": product.description,
            "price": product.price,
            "quantity": product.inventory.quantity,
        }
    )
    context = {"form": form, "product_id": product.id}
    return render(request, "inventory/detail.html", context)


@login_required
def update(request, product_id):
    product = get_object_or_404(Products, pk=product_id, user=request.user)
    inventory = get_object_or_404(Inventory, pk=product.inventory.id)
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        logger.info("form is valid")
        with transaction.atomic():
            body = request.POST
            product.name = body.get("name")
            product.sku = body.get("sku")
            product.description = body.get("description")
            product.price = int(body.get("price").replace(",", ""))
            product.save()
            inventory.quantity = body.get("quantity")
            inventory.save()
        form = ProductForm(
            initial={
                "name": product.name,
                "sku": product.sku,
                "description": product.description,
                "price": product.price,
                "quantity": inventory.quantity,
            }
        )
        messages.success(request, "更新に成功しました")
    context = {"form": form, "product_id": product.id}
    return render(request, "inventory/detail.html", context)


@login_required
def delete(request, product_id):
    product = get_object_or_404(Products, pk=product_id, user=request.user)
    sku = product.sku
    product.delete()
    messages.success(request, f"「{sku}」の削除に成功しました")
    return redirect("inventory-index")


@login_required
def download(request):
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    JST = zoneinfo.ZoneInfo("Asia/Tokyo")
    now = datetime.now(JST)
    now_str = now.strftime("%Y%m%d%H%M%S")
    response["Content-Disposition"] = f'attachment; filename="products_{now_str}.csv"'
    products = Products.objects.select_related("inventory").filter(user=request.user)
    writer = csv.writer(response)
    # ヘッダー行
    writer.writerow(["ID", "商品名", "SKU", "商品説明", "価格", "在庫数"])
    # データ行
    for product in products:
        writer.writerow(
            [
                product.id,
                product.name,
                product.sku,
                product.description,
                product.price,
                product.inventory.quantity,
            ]
        )
    return response

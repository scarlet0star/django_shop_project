from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.db import transaction
from .models import *
from .forms import *


@login_required
def product_list(request):
    products = Product.objects.all()

    return render(request, 'product/product_list.html', {'products': products})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:products')
    else:
        form = ProductCreateForm()

    return render(request, 'product/product_create.html', {'form': form})


@login_required
@transaction.atomic
def inbound_create(request):
    if request.method == "POST":
        form = InboundCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:inbounds')
    else:
        form = InboundCreateForm()

    return render(request, 'product/inbound_create.html', {"form": form})


@login_required
def inbound_list(request):
    inbounds = Inbound.objects.all()
    return render(request, "product/inbound_list.html", {"inbounds": inbounds})


@login_required
@transaction.atomic
def outbound_create(request):
    if request.method == "POST":
        form = OutboundCreateForm(request.POST)

        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            inbound_qs = Inbound.objects.filter(product=product)
            inbound_total = sum([inbound.quantity for inbound in inbound_qs])

            outbound_qs = Outbound.objects.filter(product=product)
            outbound_total = sum(
                [outbound.quantity for outbound in outbound_qs])

            available_quantity = inbound_total - outbound_total

            if quantity > available_quantity:
                messages.error(
                    request, f"선택한 제품의 가능한 최대 수량은 {available_quantity}개 입니다.")
                return redirect('product:outbound_create')
            else:
                form.save()
                return redirect('product:outbounds')
    else:
        form = OutboundCreateForm()

    return render(request, 'product/outbound_create.html', {"form": form})


@login_required
def outbound_list(request):
    outbounds = Outbound.objects.all()
    return render(request, "product/outbound_list.html", {"outbounds": outbounds})


@login_required
def inventory(request):
    inventory = Inventory.objects.all()

    return render(request, 'product/inventory_list.html', {'inventory': inventory})


@login_required
def inventory_create(request):
    products = Product.objects.all()

    for product in products:
        inbound_qs = Inbound.objects.filter(product=product)
        outbound_qs = Outbound.objects.filter(product=product)

        inbound_total = sum([inbound.quantity for inbound in inbound_qs])
        outbound_total = sum([outbound.quantity for outbound in outbound_qs])

        inventory, created = Inventory.objects.get_or_create(product=product)
        inventory.quantity = inbound_total - outbound_total
        inventory.save()

    return redirect('product:inventory')

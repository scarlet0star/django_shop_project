from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
def inbound_create(request, inbound_id):
    inbound = None

    if inbound_id:
        inbound = get_object_or_404(Inbound, id=inbound_id)

    if request.method == "POST":
        form = InboundCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:inbound_list')
    else:
        form = InboundCreateForm(instance=inbound)

    return render(request, 'product/inbound_create_update.html', {"form": form})


@login_required
def inbound_list(request):
    inbounds = Inbound.objects.all()
    return render(request, "product/inbound_list.html", {"inbounds": inbounds})


@login_required
@transaction.atomic
def outbound_create(request, outbound_id):
    outbound = None

    if outbound_id:
        outbound = get_object_or_404(Outbound, id=outbound_id)

    if request.method == "POST":
        form = OutboundCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:outbound_list')
    else:
        form = OutboundCreateForm(instance=outbound)

    return render(request, 'product/outbound_create_update.html', {"form": form})


@login_required
def outbound_list(request):
    outbounds = Outbound.objects.all()
    return render(request, "product/inbound_list.html", {"inbounds": outbounds})


@login_required
def inventory(request):
    inventory = Inventory.objects.all()

    return render(request, 'product/inventory_list.html', {'inventory': inventory})

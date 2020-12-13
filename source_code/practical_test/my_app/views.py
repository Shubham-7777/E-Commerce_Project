from contextlib import redirect_stderr

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Item, OrderItem, Order, ShippingAddress
from django.utils import timezone
from .forms import CheckOutForm

# Create your views here.
"""class HomeView(TemplateView):
    template_name = "my_app/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        obj = Item.objects.all()
        context["home_object"] = context
        return context"""


class HomeView(ListView):
    model = Item
    context_object_name = 'home_object'
    template_name = "my_app/home.html"


class CheckOutView(ListView):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = CheckOutForm()
        template_name = "my_app/test.html"
        context = {"checkout_form": form,
                   "checkout_obj": order
                   }
        # return redirect("my_app:checkout_url_name")
        return render(self.request, template_name, context)

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        template_name = "my_app/test.html"
        # print(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                e_mail = form.cleaned_data.get('e_mail')
                phone_number = form.cleaned_data.get('phone_number')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                address_line1 = form.cleaned_data.get('address_line1')
                address_line2 = form.cleaned_data.get('address_line2')
                postal_code = form.cleaned_data.get('postal_code')
                payment_options = form.cleaned_data.get('payment_options')
                shipping_address = ShippingAddress(
                    user=self.request.user,
                    e_mail=e_mail,
                    phone_number=phone_number,
                    country=country,
                    city=city,
                    state=state,
                    address_line1=address_line1,
                    address_line2=address_line2,
                    postal_code=postal_code,
                    payment_options=payment_options
                )
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
                print("The form is valid")
                messages.info(self.request, "Order Successful")
                # return redirect("my_app:checkout_url_name")
                return render(self.request, template_name)
            else:
                messages.warning(self.request, "Page not coming through")
                return render(self.request, template_name)
                # return redirect("my_app:checkout_url_name")
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect("/")


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order_object = Order.objects.get(user=self.request.user, ordered=False)
            context = {"cart_object": order_object}
            template_name = 'my_app/cart_test.html'
            return render(self.request, template_name, context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an Active Order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    context_object_name = 'detail_object'
    template_name = 'my_app/single_product.html'


@login_required()
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated ")
            return redirect("my_app:cart_url_name")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect("my_app:detail_page_url_name", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("my_app:detail_page_url_name", slug=slug)


@login_required()
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            # order_item.delete()
            messages.info(request, "This item removed from your cart.")
            return redirect("my_app:cart_url_name")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("my_app:detail_page_url_name", slug=slug)

    else:
        messages.info(request, "You don't have an active order!")
        return redirect("my_app:detail_page_url_name", slug=slug)


@login_required()
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_item.quantity -= 1
            order_item.save()
            # order_item.delete()
            messages.info(request, "This item quantity was updated.")
            return redirect("my_app:cart_url_name")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("my_app:detail_page_url_name", slug=slug)
    else:
        messages.info(request, "You do not have an active order!")
        return redirect("my_app:detail_page_url_name", slug=slug)

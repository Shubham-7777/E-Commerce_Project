from django.urls import path
from .views import (HomeView,
                    ItemDetailView,
                    CartView,
                    CheckOutView)

from .views import (add_to_cart,
                    remove_from_cart,
                    remove_single_item_from_cart
                    )

app_name = "my_app"

urlpatterns = [
    path("", HomeView.as_view(), name='home_page_url'),
    path("detail/<slug>/", ItemDetailView.as_view(), name='detail_page_url_name'),
    path("cart/", CartView.as_view(), name="cart_url_name"),
    path("add_to_cart/<slug>/", add_to_cart, name="add_to_cart_url_name"),
    path("checkout/", CheckOutView.as_view(), name="checkout_url_name"),
    path("remove_from_cart/<slug>/", remove_from_cart, name="remove_from_cart_url_name"),
    path("remove_single_item_from_cart/<slug>/", remove_single_item_from_cart,
         name="remove_single_item_from_cart_url_name")
]

# path("home/", home_view, name='home_page_url'),
# path("product/", ItemListView.as_view(), name='product_page_url'),

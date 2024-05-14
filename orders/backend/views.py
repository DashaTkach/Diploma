from django.db.models import Sum, F
from django.http import JsonResponse
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from yaml import load as load_yaml, Loader

from .forms import RegisterUserForm, LoginUserForm
from .serializers import *
from .import_data import Command
from .utils import DataMixin
from .models import *


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        if self.request.user.role == 1:
            return reverse_lazy('suppliers')
        else:
            return reverse_lazy('login')


def logout_user(request):
    logout(request)
    return redirect('login')


def dowload_add_info(request):
    with open('backend/shops_data/shop1.yaml', 'r', encoding='UTF-8') as file:
        data = load_yaml(file, Loader=Loader)
        if request.method == 'POST':
            some = Command()
            res = some.get_data(data)
            return render(request, 'dowload_add_info.html', {'text': res})
        return render(request, 'dowload_add_info.html', {'numbers': [1, 2]})


class SupplierSerializerViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = SupplierSerializer


class SupplierProductInfoView(GenericAPIView):
    http_method_names = ['get', 'put', ]
    queryset = ProductInfo.objects.all()
    serializer_class = SupplierProductInfoSerializer

    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs["id"]
            if id:
                product_info_object = ProductInfo.objects.get(id=id)
                serializer = SupplierProductInfoSerializer(product_info_object)
        except:
            products = self.get_queryset()
            serializer = SupplierProductInfoSerializer(products, many=True)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        product_info_object = ProductInfo.objects.get(id=id)

        data = request.data

        product_info_object.price = data["price"]
        product_info_object.price_rrc = data["price_rrc"]
        product_info_object.quantity = data["quantity"]

        product_info_object.save()

        serializer = SupplierProductInfoSerializer(product_info_object)
        return Response(serializer.data)


class ProductInfoView(ListAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = SupplierProductInfoSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['id', ]


class ContactView(GenericAPIView):
    http_method_names = ['get', 'post', 'put', 'delete', ]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get(self, request, *args, **kwargs):
        contact = Contact.objects.filter(
            user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        item = Contact.objects.create(
            city=data['city'],
            street=data['street'],
            house=data['house'],
            structure=data['structure'],
            building=data['building'],
            apartment=data['apartment'],
            user=request.user.id,
            phone=data['phone'],
        )
        item.save()
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        contact_object = Contact.objects.get(id=id)
        data = request.data

        contact_object.city = data['city']
        contact_object.street = data['street']
        contact_object.structure = data['structure']
        contact_object.building = data['building']
        contact_object.apartment = data['apartment']
        contact_object.phone = data['phone']
        contact_object.house = data['house']

        contact_object.save()
        serializer = OrderItemSerializer(contact_object)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        if id:
            Contact.objects.delete(id=id)
        return JsonResponse({'Status': True})


class OrderItemCreateView(GenericAPIView):
    http_method_names = ['post', ]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        item = OrderItem.objects.create(
            product_info=data['product_info'],
            quantity=data['quantity'],
            shop=data['shop'],
            user=request.user.id
        )
        item.save()
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)


class BasketView(GenericAPIView):
    http_method_names = ['get', 'post', 'put', 'delete', ]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        basket = Order.objects.filter(  # стоимость всего заказа получаем
            user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        order = Order.objects.create(
            user=request.user.id,
            contact=data['contact'],
            state='basket',
            shop=data['shop']
        )
        for order_item in OrderItem.objects.filter(user=request.user.id):
            order_item.order = order.id
            order_item.save()
        serializer = OrderItemSerializer(order)
        return Response(serializer.data)


class OrderItemListView(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['id', ]

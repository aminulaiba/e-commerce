from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated


from cart.views import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from .permission import IsOrderManagement



# Create your views here.
# for checking whether the user is authenticated and belongs to the oms group
def is_order_managment(user):
    return user.is_authenticated and user.groups.filter(name='Order Management System').exists()

def login_orderpage(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and is_order_managment(user=user):
            login(request, user)
            messages.success(request, "Successfully Logged In! :)")
            return redirect('orders') 
        else:
            messages.error(request, "Wrong username or password.")
            return redirect('oms-login')
    return render(request, 'order_management/login.html')

def logout_orderpage(request):
    logout(request)
    messages.success(request, ("Successfully LogOut!"))
    return redirect('oms-login')

@login_required(login_url='oms-login')
def orders(request):
    # this will authorization
    if not is_order_managment(user=request.user):
        return HttpResponseForbidden('You are not authorized to access this page.')
    return render(request, 'order_management/orders.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOrderManagement])
def get_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    status = request.query_params.get('status')
    search = request.query_params.get('search')
    page = int(request.query_params.get('page', 1))
    page_size = 10

    # Filtered by status
    if status != 'all':
        orders = orders.filter(delivery_status=status)

    # Search
    if search:
        if search.isdigit():
            orders = orders.filter(id=int(search))
        else:
            orders = orders.filter(user__username__istartswith=search)

    # Paginations
    paginator = Paginator(orders, page_size)
    pageObject = paginator.get_page(page)

    serialised_orders = OrderSerializer(pageObject.object_list, many=True)

    # Manually build paginated response
    response_data = {
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "current_page": pageObject.number,
        "has_next": pageObject.has_next(),
        "has_previous": pageObject.has_previous(),
        "results": serialised_orders.data
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOrderManagement])
def quick_dashbord_counts(request):
    quickStates = Order.objects.aggregate(
        processing=Count('id', filter=Q(delivery_status='processing')),
        shipped=Count('id', filter=Q(delivery_status='shipped')),
        delivered=Count('id', filter=Q(delivery_status='delivered')),
        refunded=Count('id', filter=Q(delivery_status='refunded')),
    )
    return Response(quickStates)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsOrderManagement])
def get_orders_details(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'GET':
        items = order.items.all()
        serilized_details = OrderItemSerializer(items, many=True)
        return Response(serilized_details.data)
    elif request.method == 'POST':
        print(request.data)                     # <--- see all data
        status = request.data.get('status')     # <--- get status
        tracking = request.data.get('tracking')
        order.delivery_status = status
        order.save()
        return Response({"message": "Order updated successfully"})








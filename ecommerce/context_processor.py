from .models import *
def cart_price(request):
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
        items=order.order.all()
        cartItems=order.get_total_item
        return {
        
        'order':order,
        'cartItems':cartItems
        
    }
    else:
        items=[]
        #if user is not logged in
        order={
            'get_total':0,'get_total_item':0
        }
        return {
        
        'order':order,
        
        
        }
    return {}
        
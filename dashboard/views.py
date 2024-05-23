from django.shortcuts import render,redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from .models import Product,Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your pdf file here.
def product_pdf(request):
    #Create a byte stream buffer
    buf = io.BytesIO()
    #create a canva
    c = canvas.Canvas(buf, pagesize=letter,bottomup=0 )
    #create a text object

    

    textob= c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont('Helvetica', 14)



    items = Product.objects.all()
    lines=[]
        
    for item in items:
        lines.append(item.name)
        lines.append(item.category)
        lines.append(str(item.quantity))
        lines.append('================================================')


    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf,as_attachment=True,filename= 'product.pdf')

# Create your views here.
@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    

    orders_count= orders.count()
    product_count= products.count()
    workers_count= User.objects.all().count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form':form,
        'products':products,
        'product_count':product_count,
        'workers_count':workers_count,
        'orders_count':orders_count,
        
    }
    return render(request,'dashboard/index.html', context)

@login_required
def staff(request):

    workers = User.objects.all()
    workers_count= workers.count()

    items = Product.objects.all()
    product_count = items.count()

    orders = Order.objects.all()
    orders_count = orders.count()

    context = {
        'workers': workers,
        'workers_count': workers_count,
        'product_count': product_count,
        'orders_count': orders_count,

    }
    return render(request,'dashboard/staff.html',context)

def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers': workers,

    }
    return render(request,'dashboard/staff_detail.html',context)

@login_required
def product(request):
    items = Product.objects.all()
    product_count = items.count()

    workers = User.objects.all()
    workers_count= workers.count()

    orders = Order.objects.all()
    orders_count = orders.count()

    if request.method == 'POST':
        form = ProductForm(request.POST) 
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name') 
            messages.success(request, f'{product_name} have been added')
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context={
        'items':items,
        'form':form,
        'workers_count': workers_count,
        'product_count': product_count,
        'orders_count': orders_count,
    }
    return render(request,'dashboard/product.html', context)

@login_required
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()

    workers = User.objects.all()
    workers_count= workers.count()

    items = Product.objects.all()
    product_count = items.count()
    
    context = {
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request,'dashboard/order.html',context)

@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request,'dashboard/product_delete.html')


@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method=='POST':
        form =ProductForm(request.POST, instance=item)
        if form.is_valid():
             form.save()
             return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)  
    context = {
        'form':form,
    }
    return render(request,'dashboard/product_update.html',context)

    
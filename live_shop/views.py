from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProductForm
from .models import Product
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
# Create your views here



def home(request):
    
    return render(request, 'home.html')



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def seller_dashboard(request):
    # Vérifie si l'utilisateur est un vendeur
    if not request.user.profile.is_seller:
        messages.error(request, "Accès refusé. Vous devez être vendeur.")
        return redirect('home')
    products = Product.objects.filter(seller=request.user).exclude(id__isnull=True)
    return render(request, 'seller_dashboard.html', {'products': products})

   

@login_required
def add_product(request):
    if not request.user.profile.is_seller:
        messages.error(request, "Accès refusé.")
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Produit ajouté avec succès !")
            return redirect('seller_dashboard')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


@login_required
def become_seller(request):
    if request.method == 'POST':
        request.user.profile.is_seller = True
        request.user.profile.save()
        messages.success(request, "Félicitations ! Vous êtes maintenant vendeur 🎉")
        return redirect('seller_dashboard')
    return render(request, 'become_seller.html')


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if not request.user.profile.is_seller:
        messages.error(request, "Accès refusé.")
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifié avec succès !")
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if not request.user.profile.is_seller:
        messages.error(request, "Accès refusé.")
        return redirect('home')

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Produit '{product_name}' supprimé.")
        return redirect('seller_dashboard')

    return render(request, 'confirm_delete.html', {'product': product})


def product_catalog(request):
    products = Product.objects.filter(stock__gt=0).select_related('seller')
    return render(request, 'product_catalog.html', {'products': products})
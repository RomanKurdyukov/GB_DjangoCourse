from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryAdminEditForm, VcAdminAddForm
from authapp.forms import ShopUserRegisterForm, ProductCategoryAddForm, ProductAddForm, ProductEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, VendorCode
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)


def user_create(request):
    title = 'создание пользователя'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'user_form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


def user_update(request, pk):
    title = 'редактирование пользователя'

    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    context = {
        'title': title,
        'user_form': edit_form
    }

    return render(request, 'adminapp/user_update.html', context)


def user_delete(request, pk):
    title = 'удаление пользователя'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {
        'title': title,
        'user_to_delete': user
    }

    return render(request, 'adminapp/user_delete.html', context)


class CategoryMain(ListView):
    model = ProductCategory

    template_name = 'adminapp/categories.html'

    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryUpdate(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryAdminEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')


class CategoryDelete(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoryCreate(CreateView):
    model = ProductCategory
    form_class = ProductCategoryAddForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')


class ProductByCatView(ListView):

    model = Product

    template_name = 'adminapp/products.html'

    context_object_name = 'products'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Товары в категории..'
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductAddForm
    template_name = 'adminapp/product_update.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['category'] = self.kwargs['pk']
        initial['vendor_code'] = VendorCode.objects.filter(code=self.kwargs['vc']).values_list('id', flat=True)[0]
        return initial

    def get_success_url(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = 1
        return reverse('adminapp:products', kwargs={'pk': pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение товара...'
        return context

    def get_success_url(self):
        if 'cat' in self.kwargs:
            pk = self.kwargs['cat']
        else:
            pk = 8
        return reverse('adminapp:products', kwargs={'pk': pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        if 'cat' in self.kwargs:
            pk = self.kwargs['cat']
        else:
            pk = 8
        return reverse('adminapp:products', kwargs={'pk': pk})

    def delete(self, request, *args, **kwargs):
        Product.objects.filter(id=self.kwargs['pk']).delete()
        return HttpResponseRedirect(self.get_success_url())


class ProductDisableView(DeleteView):
    model = Product
    template_name = 'adminapp/product_disable.html'

    def get_success_url(self):
        if 'cat' in self.kwargs:
            pk = self.kwargs['cat']
        else:
            pk = 8
        return reverse('adminapp:products', kwargs={'pk': pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

class VendorCodeCreateView(CreateView):
    model = VendorCode
    form_class = VcAdminAddForm
    template_name = 'adminapp/vc_create.html'

    def get_success_url(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = 8
        vc = self.object.code
        return reverse('adminapp:product_create', kwargs={'pk': pk, 'vc': vc})

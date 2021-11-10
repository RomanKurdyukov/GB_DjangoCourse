from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryAdminEditForm
from authapp.forms import ShopUserRegisterForm, ProductCategoryAddForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
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


# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     content = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', content)


class CategoryMain(ListView):
    model = ProductCategory

    template_name = 'adminapp/categories.html'

    queryset = ProductCategory.objects.all()

    context_object_name = 'categories'

    def get_context_data(self, **kwargs):

        context = super(CategoryMain, self). get_context_data(**kwargs)
        context['counter'] = Product.objects.filter(category__pk=self.kwargs.get('id')).count()
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


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass

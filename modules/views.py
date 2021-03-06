from django.utils.timezone import now
from django.shortcuts import render, redirect, Http404, reverse
from functools import partial, wraps

from django.contrib.auth.models import Group
from django.views.generic import FormView, View
from django.forms.formsets import formset_factory
from django.core.exceptions import ObjectDoesNotExist

from modules.forms import (OperatorSaleShopModule, SelfSaleShopModule,
                           ModuleCategoryCreateForm, ModuleCategoryCreateNameForm,
                           ShopModuleConfigForm)
from modules.models import OperatorSaleModule, SelfSaleModule, Category, CategoryProduct
from borgia.utils import (GroupPermissionMixin, GroupLateralMenuFormMixin,
                          ShopFromGroupMixin, ShopModuleMixin,
                          GroupLateralMenuMixin, shop_from_group,
                          lateral_menu)
from shops.models import Shop, Product
from finances.models import Sale, SaleProduct
from users.models import User


class SaleShopModuleInterface(GroupPermissionMixin, FormView,
                              GroupLateralMenuFormMixin):
    """
    Generic FormView for handling invoice concerning product bases through a
    shop.

    :param self.template_name: template, mandatory.
    :param self.form_class: form class, mandatory.
    :param self.module_class: module class, mandatory.
    :param self.perm_codename: permission to check
    :type self.template_name: string
    :type self.form_class: Form class object
    :type self.module_class: ShopModule class object
    :type self.perm_codename: string
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            self.shop = Shop.objects.get(name=kwargs['shop_name'])
            self.module = self.module_class.objects.get(shop=self.shop)
        except ObjectDoesNotExist:
            raise Http404
        if self.module.state is False:
            raise Http404
        return super(SaleShopModuleInterface,
                     self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        kwargs = super(SaleShopModuleInterface,
                       self).get_form_kwargs(**kwargs)
        kwargs['module'] = self.module
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SaleShopModuleInterface,
                        self).get_context_data(**kwargs)
        context['shop'] = self.shop
        context['categories'] = self.module.categories.all()
        return context

    def form_valid(self, form):
        """
        Create a sale and like all products via SaleProduct objects.
        """
        sale = Sale.objects.create(
            operator=self.request.user,
            sender=self.client,
            recipient=User.objects.get(pk=1),
            module=self.module,
            shop=self.shop
        )
        for field in form.cleaned_data:
            if field != 'client':
                invoice = form.cleaned_data[field]
                if invoice > 0 and isinstance(invoice, int):
                    try:
                        category_product = CategoryProduct.objects.get(pk=field.split('-')[0])
                        SaleProduct.objects.create(
                            sale=sale,
                            product=category_product.product,
                            quantity=category_product.quantity * invoice,
                            price=category_product.get_price() * invoice
                        )
                    except ObjectDoesNotExist:
                        pass
        sale.pay()
        return sale_shop_module_resume(
            self.request, sale, self.group, self.shop, self.module, self.success_url
        )


class SelfSaleShopModuleInterface(SaleShopModuleInterface):
    """
    Sale interface for SelfSaleModule.
    """
    template_name = 'modules/shop_module_sale_interface.html'
    form_class = SelfSaleShopModule
    module_class = SelfSaleModule
    perm_codename = 'use_selfsalemodule'
    lm_active = None

    def get_form_kwargs(self, **kwargs):
        kwargs = super(SelfSaleShopModuleInterface,
                       self).get_form_kwargs(**kwargs)
        kwargs['client'] = self.request.user

        self.lm_active = 'lm_selfsale_interface_module_' + self.shop.name
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SelfSaleShopModuleInterface, self).get_context_data(**kwargs)
        context['type'] = "self_sale"
        return context

    def form_valid(self, form):
        self.client = self.request.user
        self.success_url = reverse(
            'url_module_selfsale',
            kwargs={
                'group_name': self.group.name,
                'shop_name': self.shop.name
            }
        )
        return super(SelfSaleShopModuleInterface, self).form_valid(form)


class OperatorSaleShopModuleInterface(SaleShopModuleInterface):
    """
    Sale interface for SelfOperatorModule.
    """
    template_name = 'modules/shop_module_sale_interface.html'
    form_class = OperatorSaleShopModule
    module_class = OperatorSaleModule
    perm_codename = 'use_operatorsalemodule'
    lm_active = 'lm_operatorsale_interface_module'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(OperatorSaleShopModuleInterface,
                       self).get_form_kwargs(**kwargs)
        kwargs['client'] = None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(OperatorSaleShopModuleInterface, self).get_context_data(**kwargs)
        context['type'] = "operator_sale"
        return context

    def form_valid(self, form):
        try:
            self.client = User.objects.get(
                username = form.cleaned_data['client'])
        except ObjectDoesNotExist:
            raise forms.ValidationError('Utilisateur inconnu')
        except KeyError:
            raise forms.ValidationError('Utilisateur non sélectionné')

        self.success_url = reverse(
            'url_module_operatorsale',
            kwargs={
                'group_name': self.group.name,
                'shop_name': self.shop.name
            }
        )
        return super(OperatorSaleShopModuleInterface, self).form_valid(form)


def sale_shop_module_resume(request, sale, group, shop, module, success_url):
    template_name = 'modules/shop_module_sale_resume.html'

    # Context construction, based on LateralMenuViewMixin and
    # GroupPermissionMixin in borgia.utils
    context = {
        'group': group,
        'shop': shop,
        'module': module,
        'sale': sale,
        'delay': module.delay_post_purchase,
        'group_name': group.name,
        'success_url': success_url
    }
    context['nav_tree'] = lateral_menu(
        request.user,
        group,
        None)
    if (request.user.groups.all().exclude(
            pk__in=[1, 5, 6]).count() > 0):
        context['first_job'] = request.user.groups.all().exclude(
            pk__in=[1, 5, 6])[0]
    context['list_selfsalemodule'] = []
    for s in Shop.objects.all().exclude(pk=1):
        try:
            m = SelfSaleModule.objects.get(shop=s)
            if m.state is True:
                context['list_selfsalemodule'].append(s)
        except ObjectDoesNotExist:
            pass

    # Check if you should logout after sale
    if module.logout_post_purchase:
        context['success_url'] = reverse('url_logout')

    return render(request, template_name, context=context)


class SaleShopModuleResume(GroupPermissionMixin, View,GroupLateralMenuMixin):
    sale = None
    delay = None
    success_url = None
    context = None
    template_name = 'modules/shop_module_sale_resume.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.sale = kwargs['sale_pk']
        except KeyError:
            raise Http404
        try:
            self.delay = kwargs['delay']
        except KeyError:
            pass
        try:
            self.success_url = kwargs['success_url']
        except KeyError:
            pass
        return super(SaleShopModuleResume,
                     self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['sale'] = self.sale
        context['delay'] = self.delay
        context['success_url'] = self.success_url
        return render(request, self.template_name, context=context)


class SelfSaleShopModuleWorkboard(GroupPermissionMixin, ShopFromGroupMixin,
                                  ShopModuleMixin, View,
                                  GroupLateralMenuMixin):
    """
    View of the workboard of an SelfSale module of a shop.

    :param kwargs['group_name']: name of the group, mandatory
    :type kwargs['group_name']: string
    :raises: Http404 if the group_name doesn't match a group
    """
    template_name = 'modules/shop_module_sale_workboard.html'
    perm_codename = None
    lm_active = 'lm_selfsale_module'
    module_class = SelfSaleModule

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['type'] = "self_sale"
        return render(request, self.template_name, context=context)


class OperatorSaleShopModuleWorkboard(GroupPermissionMixin, ShopFromGroupMixin,
                                      ShopModuleMixin, View,
                                      GroupLateralMenuMixin):
    """
    View of the workboard of an OperatorSale module of a shop.

    :param kwargs['group_name']: name of the group, mandatory
    :type kwargs['group_name']: string
    :raises: Http404 if the group_name doesn't match a group
    """
    template_name = 'modules/shop_module_sale_workboard.html'
    perm_codename = None
    lm_active = 'lm_operatorsale_module'
    module_class = OperatorSaleModule

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['type'] = "operator_sale"
        return render(request, self.template_name, context=context)


class ShopModuleCategoryCreate(GroupPermissionMixin, ShopFromGroupMixin,
                                ShopModuleMixin,
                                View, GroupLateralMenuMixin):
    """
    """
    template_name = 'modules/shop_module_category_create.html'
    form_class = None
    perm_codename = None
    lm_active = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.group = Group.objects.get(name=kwargs['group_name'])
            self.shop = shop_from_group(self.group)
            if kwargs['module_class'] == SelfSaleModule:
                self.module, created = SelfSaleModule.objects.get_or_create(
                    shop=self.shop)
            elif kwargs['module_class'] == OperatorSaleModule:
                self.module, created = OperatorSaleModule.objects.get_or_create(
                    shop=self.shop)
        except ObjectDoesNotExist:
            raise Http404
        except ValueError:
            raise Http404
        self.form_class = formset_factory(wraps(ModuleCategoryCreateForm)(partial(ModuleCategoryCreateForm, shop=self.shop)), extra=1)
        return super(ShopModuleCategoryCreate,
                     self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['cat_form'] = self.form_class()
        context['cat_name_form'] = ModuleCategoryCreateNameForm()
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        cat_name_form = ModuleCategoryCreateNameForm(request.POST)
        if cat_name_form.is_valid():
            category = Category.objects.create(
                name=cat_name_form.cleaned_data['name'],
                module=self.module
            )

        cat_form = self.form_class(request.POST)
        for product_form in cat_form.cleaned_data:
            try:
                product = Product.objects.get(pk=product_form['product'].split('/')[0])
                if product.unit:
                    quantity = int(product_form['quantity'])
                else:
                    quantity = 1
                CategoryProduct.objects.create(
                    category=category,
                    product=product,
                    quantity=quantity
                )
            except ObjectDoesNotExist:
                pass
            except KeyError:
                pass
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['module_class'] == SelfSaleModule:
            self.success_url = reverse(
                'url_module_selfsale_workboard', kwargs={
                'group_name': self.kwargs['group_name']})
        elif self.kwargs['module_class'] == OperatorSaleModule:
            self.success_url = reverse(
                'url_module_operatorsale_workboard', kwargs={
                'group_name': self.kwargs['group_name']})
        return self.success_url


class ShopModuleCategoryUpdate(GroupPermissionMixin, ShopFromGroupMixin,
                                ShopModuleMixin,
                                View, GroupLateralMenuMixin):
    """
    """
    template_name = 'modules/shop_module_category_update.html'
    form_class = None
    perm_codename = None
    lm_active = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.group = Group.objects.get(name=kwargs['group_name'])
            self.shop = shop_from_group(self.group)
            if kwargs['module_class'] == SelfSaleModule:
                self.module, created = SelfSaleModule.objects.get_or_create(
                    shop=self.shop)
            elif kwargs['module_class'] == OperatorSaleModule:
                self.module, created = OperatorSaleModule.objects.get_or_create(
                    shop=self.shop)
        except ObjectDoesNotExist:
            raise Http404
        except ValueError:
            raise Http404
        try:
            self.category = Category.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if self.category.module.pk != self.module.pk:
            raise Http404
        self.form_class = formset_factory(wraps(ModuleCategoryCreateForm)(partial(ModuleCategoryCreateForm, shop=self.shop)), extra=1)
        return super(ShopModuleCategoryUpdate,
                     self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        cat_form_data = [{'product': str(category_product.product.pk) + '/' + str(category_product.product.get_unit_display()), 'quantity': category_product.quantity}
                            for category_product in self.category.categoryproduct_set.all()]
        context['cat_form'] = self.form_class(initial=cat_form_data)
        context['cat_name_form'] = ModuleCategoryCreateNameForm(initial={'name': self.category.name})
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        cat_name_form = ModuleCategoryCreateNameForm(request.POST)
        if cat_name_form.is_valid():
            self.category.name = cat_name_form.cleaned_data['name']
            self.category.save()

        cat_form = self.form_class(request.POST)
        CategoryProduct.objects.filter(category=self.category).delete()
        for product_form in cat_form.cleaned_data:
            try:
                product = Product.objects.get(pk=product_form['product'].split('/')[0])
                if product.unit:
                    quantity = int(product_form['quantity'])
                else:
                    quantity = 1
                CategoryProduct.objects.create(
                    category=self.category,
                    product=product,
                    quantity=quantity
                )
            except ObjectDoesNotExist:
                pass
            except KeyError:
                pass
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['module_class'] == SelfSaleModule:
            self.success_url = reverse(
                'url_module_selfsale_workboard', kwargs={
                'group_name': self.kwargs['group_name']})
        elif self.kwargs['module_class'] == OperatorSaleModule:
            self.success_url = reverse(
                'url_module_operatorsale_workboard', kwargs={
                'group_name': self.kwargs['group_name']})
        return self.success_url


class ShopModuleCategoryDelete(GroupPermissionMixin, ShopFromGroupMixin,
                                ShopModuleMixin,
                                View, GroupLateralMenuMixin):
    """
    """
    template_name = 'modules/shop_module_category_delete.html'
    form_class = None
    perm_codename = None
    lm_active = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.group = Group.objects.get(name=kwargs['group_name'])
            self.shop = shop_from_group(self.group)
            if kwargs['module_class'] == SelfSaleModule:
                self.module, created = SelfSaleModule.objects.get_or_create(
                    shop=self.shop)
            elif kwargs['module_class'] == OperatorSaleModule:
                self.module, created = OperatorSaleModule.objects.get_or_create(
                    shop=self.shop)
        except ObjectDoesNotExist:
            raise Http404
        except ValueError:
            raise Http404
        try:
            self.category = Category.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404
        if self.category.module.pk != self.module.pk:
            raise Http404
        return super(ShopModuleCategoryDelete,
                     self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['object'] = self.category
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        CategoryProduct.objects.filter(category=self.category).delete()
        self.category.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['module_class'] == SelfSaleModule:
            self.success_url = reverse(
                'url_module_selfsale_workboard', kwargs={
                'group_name': self.kwargs['group_name']})
        elif self.kwargs['module_class'] == OperatorSaleModule:
            self.success_url = reverse(
                'url_module_operatorsale_workboard', kwargs={
                'group_name': self.kwargs['group_name']})
        return self.success_url


class ShopModuleConfig(GroupPermissionMixin, ShopFromGroupMixin,
                       ShopModuleMixin, FormView,
                       GroupLateralMenuFormMixin):
    """
    View to manage config of a self shop module.

    :param kwargs['group_name']: name of the group, mandatory
    :param kwargs['module_class']: class of the shop module, mandatory
    :type kwargs['group_name']: string
    :type kwargs['module_class']: class object
    """
    template_name = 'modules/shop_module_config.html'
    form_class = ShopModuleConfigForm
    perm_codename = None
    lm_active = None

    def get_initial(self):
        initial = super(ShopModuleConfig, self).get_initial()
        initial['state'] = self.module.state
        initial['logout_post_purchase'] = self.module.logout_post_purchase
        initial['limit_purchase'] = self.module.limit_purchase
        if self.module.delay_post_purchase:
            initial['infinite_delay_post_purchase'] = False
        else:
            initial['infinite_delay_post_purchase'] = True
        initial['delay_post_purchase'] = self.module.delay_post_purchase
        return initial

    def form_valid(self, form):
        self.module.state = form.cleaned_data['state']
        self.module.logout_post_purchase = form.cleaned_data['logout_post_purchase']
        self.module.limit_purchase = form.cleaned_data['limit_purchase']
        if form.cleaned_data['infinite_delay_post_purchase'] is True:
            self.module.delay_post_purchase = None
        else:
            self.module.delay_post_purchase = form.cleaned_data['delay_post_purchase']
        self.module.save()
        return super(ShopModuleConfig, self).form_valid(form)

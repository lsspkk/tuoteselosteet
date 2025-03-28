from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Company, Product, Amount, Allergen, Food


class CompanyForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {'user': forms.widgets.Select(attrs={'disabled': True})}


class SuperuserCompanyForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea, label=_('company|description'))

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {'user': forms.widgets.Select(attrs={'disabled': False})}


class AmountInline(admin.TabularInline):
    model = Amount
    list_display = ('food', 'weight')
    list_editable = ('food', 'weight')
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('change_link', 'name', 'nameSV', 'weight')
    list_editable = ('name', 'nameSV', 'weight')
    inlines = (AmountInline,)
    readonly_fields = ('change_link',)

    def change_link(self, obj):
        return mark_safe(
            '<a href="%s">Muokkaa</a>' %
            reverse('admin:selosteet_product_change', args=[obj.id])
        )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Product.objects.all()
        comps = Company.objects.filter(user=request.user)
        return Product.objects.filter(company__in=comps)


admin.site.register(Product, ProductAdmin)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    readonly_fields = ('change_link',)

    def change_link(self, obj):
        return mark_safe(
            '<a href="%s">Raaka-aineet</a>' %
            reverse('admin:selosteet_product_change', args=[obj.id])
        )


class CompanyAdmin(GuardedModelAdmin):
    inlines = (ProductInline,)
    show_change_link = True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.author = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = SuperuserCompanyForm
        else:
            kwargs['form'] = CompanyForm
        return super(CompanyAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(CompanyAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Company.objects.all()
        return Company.objects.filter(user=request.user)


admin.site.register(Company, CompanyAdmin)


class AllergenAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'nameSV'),
            'description': _("Raaka-aineet, jotka ovat allergian aiheuttajia, korostetaan tuoteselosteissa.")
        }),
    )
    list_display = ('id', 'name', 'nameSV')
    list_editable = ('name', 'nameSV')
    list_display_links = None


admin.site.register(Allergen, AllergenAdmin)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nameSV', 'description', 'descriptionSV')
    list_editable = ('name', 'nameSV', 'description', 'descriptionSV')
    list_display_links = ('id',)


admin.site.register(Food, FoodAdmin)

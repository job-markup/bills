from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from invoices_system.utils import unique_slug_generator


class Category(models.Model):
    name = models.CharField('اسم القسم', max_length=200, db_index=True)
    slug = models.SlugField(help_text='يتم انشائه تلقائيا', max_length=200,
                            db_index=True, blank=True, unique=True)
    created_at = models.DateTimeField('انشئ في', auto_now_add=True)
    updated_at = models.DateTimeField('حدث في', auto_now=True)

    class Meta:
        ordering = ('-updated_at',)
        index_together = (('id', 'slug'),)
        verbose_name = 'القسم'
        verbose_name_plural = 'الاقسام'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE, null=True)
    name = models.CharField('اسم المنتج', max_length=120)
    product_code = models.CharField('كود المنتج', max_length=50,
                                    blank=True, null=True)
    description = models.TextField('تفاصيل المنتج', blank=True)
    price = models.DecimalField('السعر', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('الكمية المتاحة')
    created_at = models.DateTimeField('انشئ في', auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'المنتج'
        verbose_name_plural = 'المنتجات'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list')


class ShopInfo(models.Model):
    name = models.CharField('اسم المتجر', max_length=200, db_index=True)
    image = models.ImageField('شعار المتجر', upload_to='logo/',
                              blank=True, null=True)
    phone = models.CharField('رقم الهاتف', max_length=120)
    tax_num = models.CharField('الرقم الضريبي', max_length=120)

    class Meta:
        verbose_name = 'اعدادات المتجر'
        verbose_name_plural = 'اعدادات المتجر'

    def __str__(self):
        return self.name


def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_pre_save_receiver, sender=Category)

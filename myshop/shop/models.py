from django.db import models
from django.urls import reverse
from slugify import slugify
 
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kargs): 
        self.slug = slugify(self.name) 
        super(Category, self).save(*args, **kargs)
#由于URL中有参数，就需要配置URL反向解析
#这样就为模型的对象配置好了用于反向解析URL的方法，我们已经知道，
#-->>get_absolute_url()是很好的获取具体对象规范化URL的方法
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)
        verbose_name = '商品'
        verbose_name_plural = verbose_name        

    def __str__(self):
        return self.name
    def save(self, *args, **kargs): 
        self.slug = slugify(self.name) 
        super(Product, self).save(*args, **kargs)
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
from django.contrib import admin
import pkr_user.models as models

admin.site.register(models.Product)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.Payment)
admin.site.register(models.OrderDetail)
admin.site.register(models.ProductLine)
admin.site.register(models.Stock)
admin.site.register(models.UserProfile)

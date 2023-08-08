from django.db import models
from django.contrib.auth.models import User
from django_tenants.models import DomainMixin, TenantMixin


class Tenant(TenantMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog_name = models.CharField(max_length=50)
    blog_image = models.ImageField(null=True, blank=True, upload_to="profile")
    is_featured = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True
    class Meta:
        ordering = ('-is_featured', '-updated_at')

    def __str__(self):
        return f"{self.blog_name}"


class Domain(DomainMixin):
    pass
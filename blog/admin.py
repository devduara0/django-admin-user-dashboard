from django.contrib import admin
from .models import Post,Category
from django.db.models import Count

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields":  ["author","title",   ]}),
    ]
    list_display = ("author", "title", "published_date")
    list_filter = ("author", "categories", "published_date")
    ordering = ("-published_date",)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count']

    ...

    def post_count(self, obj):
        return obj.post_count
     
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(post_count=Count("posts"))
        return queryset










#admin.site.register(Comment)
#admin.site.register(Post)
#admin.site.register(Category)
#admin.site.register(Subscriber)
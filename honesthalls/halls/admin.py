from django.contrib import admin

from .models import Hall, HallPhotos, RoomType


class RoomTypeInline(admin.TabularInline):
    """
    An Inline variant for the HallPhotos model.
    """
    model = RoomType


class HallPhotosInline(admin.TabularInline):
    """
    An Inline variant for the HallPhotos model.
    """
    model = HallPhotos


class HallAdmin(admin.ModelAdmin):
    """
    The Hall model spec for the Django admin app.
    Controls how the halls should be represented in the admin panel.
    """
    inlines = [
        RoomTypeInline,
        HallPhotosInline,
    ]

    # Show the following attributes in the corresponding table
    list_display = ('id', 'name', 'campus', 'date_modified')


admin.site.register(Hall, HallAdmin)

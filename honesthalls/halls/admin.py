from django.contrib import admin

from .models import Hall, HallPhotos, RoomType, Review, ReviewPhotos


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

    def get_form(self, request, obj=None, **kwargs):
        default_form = super().get_form(request, obj, **kwargs)
        return default_form


class ReviewPhotosInline(admin.TabularInline):
    """
    An Inline variant for the ReviewPhotos model.
    """
    model = ReviewPhotos


class ReviewAdmin(admin.ModelAdmin):
    """
    The Review model spec for the Django admin app.
    Controls how the reviews should be represented in the admin panel.
    """
    inlines = [
        ReviewPhotosInline,
    ]

    # Show the following attributes in the corresponding table
    list_display = ('id', 'text', 'date_modified')


admin.site.register(Hall, HallAdmin)
admin.site.register(Review, ReviewAdmin)

from django.contrib import admin

from .models import Review, ReviewPhotos, Report


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


# class ReviewInline(admin.TabularInline):
#     model = Review
#
#
# class ReportAdmin(admin.ModelAdmin):
#     inlines = [
#         ReviewInline,
#     ]

admin.site.register(Review, ReviewAdmin)
admin.site.register(Report)

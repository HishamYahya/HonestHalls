from django import forms
from django.forms import modelformset_factory

from reviews.models import Review, ReviewPhotos, Report


class ReviewEditForm(forms.ModelForm):
    text = forms.CharField(min_length=50, max_length=2500)
    anonymous = forms.BooleanField(required=False)
    cleanliness = forms.IntegerField(initial=5, min_value=1, max_value=5)
    social_life = forms.IntegerField(initial=5, min_value=1, max_value=5)
    noise = forms.IntegerField(initial=5, min_value=1, max_value=5)
    facilities = forms.IntegerField(initial=5, min_value=1, max_value=5)
    roomtype = forms.IntegerField(min_value=1)

    class Meta:
        model = Review
        fields = ['text', 'anonymous', 'cleanliness',
                  'social_life', 'noise', 'facilities']


class ReviewPhotosEditForm(forms.ModelForm):
    photo_path = forms.ImageField(required=False)
    photo_desc = forms.CharField(
        label='Description', min_length=10, max_length=100)

    class Meta:
        model = ReviewPhotos
        fields = ['photo_path', 'photo_desc']

    def clean(self):
        cleaned_data = super().clean()
        instance = cleaned_data.get('id', None)
        is_delete = cleaned_data.get('DELETE', False)
        photo_path = cleaned_data.get('photo_path', None)

        if instance and is_delete:
            # We need an id to delete a model
            raise forms.ValidationError("Cannot delete non-existent image.")

        if not instance and not photo_path:
            # Cannot add new instance without an image.
            raise forms.ValidationError("No image provided.")

    def save(self, commit=True, user=None, review=None):
        if not user:
            raise ValueError('user must be provided')
        if not review:
            raise ValueError('review must be provided')

        cleaned_data = self.cleaned_data
        # Django sets the 'id' key to the corresponding
        # model instance, but the id attribute is None
        # if there is no matching object in the database.
        instance = cleaned_data.get('id', None)
        photo_path = cleaned_data.get('photo_path', None)
        photo_desc = cleaned_data.get('photo_desc', None)
        is_delete = cleaned_data.get('DELETE', False)

        if instance and instance.id is not None:
            # Changing existing photo
            if is_delete:
                # Delete this photo and skip to the next one
                instance.delete()
                return None
            if photo_path:
                instance.photo_path = photo_path
            instance.photo_desc = photo_desc
        else:
            instance = ReviewPhotos(
                photo_path=photo_path,
                photo_desc=photo_desc,
                user=user,
                review=review,
            )

        # Honor the commit parameter
        if commit:
            instance.save()
        return instance

class ReportForm(forms.ModelForm):
    title = forms.CharField(min_length=5, max_length=75)
    explanation = forms.CharField(min_length=10, max_length=2500)

    class Meta:
        model = Report
        fields = ['title', 'explanation']


class ReviewPhotosEditFormSet(modelformset_factory(ReviewPhotos, form=ReviewPhotosEditForm, extra=3, can_delete=True)):
    pass

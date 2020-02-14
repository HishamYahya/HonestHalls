(function () {
  "use strict";

  /**
   * Initialize the image gallery feature.
   */
  function initImageGallery() {
    const $slider = $('#hh-hall-slider');
    $slider.lightSlider({
      gallery: true,
      item: 1,
      loop: true,
      slideMargin: 0,
      thumbItem: 6,
    });
  }

  /**
   * Initialize the image preview feature.
   */
  function initImagePreview() {
    const $imagePreviewBackdrop = $('.hh-image-preview-backdrop');
    const $imagePreviewElement = $('.hh-image-preview__image');
    const $imagePreviewClose = $('.hh-image-preview__close');

    $imagePreviewClose.on('click', function () {
      $imagePreviewBackdrop.removeClass('active');
    });

    function enableImagePreview($image) {
      $image.on('click', function () {
        $imagePreviewBackdrop.addClass('active');

        const imageUrl = $image.attr('src');
        $imagePreviewElement.css('background-image', 'url("' + imageUrl + '")');
      });
    }

    $('.hh-image-supports-preview').each(function (i, elem) {
      enableImagePreview($(elem));
    });
  }

  initImageGallery();
  initImagePreview();

})();
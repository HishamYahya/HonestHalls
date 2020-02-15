(function () {
  "use strict";

  function initRatingInputs() {
    /**
     * Transforms all <input class="hh-rating-input"> into
     * rating bars with stars that allow the user to select the rating visually.
     * To create a readonly rating input use:
     * <input class="hh-rating-input" value="3" readonly>
     */
    const $inputs = $('input.hh-rating-input');
    $inputs.each(function (i, input) {
      const $input = $(input);

      let starHtml = (
        '<span class="hh-rating__star">' +
        '<i class="material-icons">star</i>' +
        '</span>'
      );

      let $element = $(
        '<div class="hh-rating">' +
        starHtml.repeat(5) +
        '</div>'
      );

      // Get all the individual star elements.
      let $stars = $element.find('.hh-rating__star')

      // Updates the rating and value of <input>.
      function setRating(rating) {
        $stars.removeClass('unchecked');
        for (let i = rating; i < $stars.length; i++) {
          $($stars[i]).addClass('unchecked');
        }

        $input.val(rating);
        $input.trigger('change');
      }

      if (!$input.attr('readonly')) {
        // Clicking sets the rating.
        $stars.on('click', function (event) {
          const $star = $(this);
          const rating = $star.index() + 1;
          setRating(rating);
        });
      } else {
        $element.addClass('readonly');
      }

      // Initialize with the initial value of the <input>.
      if ($input.val()) {
        setRating($input.val() | 0);
      }

      $element.insertAfter($input);
      // Attach utility methods to the HTMLInputElement
      // instance under $rating.
      input.$rating = {
        setRating: setRating
      };
    });
  }

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

  initRatingInputs();
  initImageGallery();
  initImagePreview();

})();
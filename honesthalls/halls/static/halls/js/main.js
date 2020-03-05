(function () {
  "use strict";

  function initGlobalPlugins() {
    /**
     * Runs all the initializers for all the global plugins.
     */
    $('[data-toggle="tooltip"]').tooltip();
  }

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
        '<i class="material-icons hh-rating__star__bg">star</i>' +
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
        $stars.removeClass('unchecked semichecked-1-4 semichecked-2-4 semichecked-3-4');
        for (let i = Math.ceil(rating); i < $stars.length; i++) {
          $($stars[i]).addClass('unchecked');
        }

        if (Math.floor(rating) !== Math.ceil(rating)) {
          const level = Math.round((rating % 1) * 4);
          $($stars[Math.ceil(rating) - 1]).addClass('semichecked-' + level + '-4');
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
        setRating(parseFloat($input.val()));
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
    const $previewBackdrop = $('.hh-preview-dialog-backdrop');
    const $previewBackdropImage = $('.hh-preview-dialog__image');
    const $previewBackdropContent = $('.hh-preview-dialog__content');
    const $previewClose = $('.hh-preview-dialog-close');

    $previewClose.on('click', function () {
      $previewBackdrop.removeClass('active');
      $previewBackdrop.addClass('inactive');
    });

    $previewBackdrop.on('click', function (event) {
      if (event.target === $previewBackdrop[0]) {
        $previewBackdrop.removeClass('active');
        $previewBackdrop.addClass('inactive');
      }
    });

    function enableImagePreview($image) {
      $image.on('click', function () {
        $previewBackdrop.addClass('active');

        const contentId = $image.attr('data-hh-image-preview');
        if (contentId) {
          const $content = $(document.getElementById(contentId));
          $previewBackdropContent.html($content.html());
          // Init any JS plugins that were injected into the dialog.
          initGlobalPlugins();
        }

        const imageSrc = $image.attr('data-hh-image-src') || $image.attr('src');
        $previewBackdropImage.attr('src', imageSrc);
      });
    }

    $('[data-hh-image-preview]').each(function (i, elem) {
      enableImagePreview($(elem));
    });
  }

  initRatingInputs();
  initImageGallery();
  initImagePreview();

})();
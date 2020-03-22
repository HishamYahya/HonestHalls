$(function () {
  (function initializeCharCount() {
    /**
     * Updates the char count for the textarea whenever the text changes
     */
    const $reviewText = $('#reviewText');
    const $reviewCharCount = $("#reviewCharCount");

    function updateCharCount() {
      const length = $reviewText.val().length;
      $reviewCharCount.text(length);
    }

    $reviewText.on('keypress keyup', updateCharCount);
    updateCharCount();
  })(); // Self-invoked

  (function initializeRatings() {
    /**
     * Updates the overall rating whenever one of the other ratings change.
     */
    const $overallRating = $('#overallRating');
    const $overallRatingText = $('#overallRatingText');
    const $sourceRatings = $('#cleanlinessRating, #socialLifeRating, #facilitiesRating, #noiseRating');

    function updateOverallRating() {
      let total = 0;
      $sourceRatings.each(function () {
        total += $(this).val() | 0;
      });

      const newRating = total / $sourceRatings.length;
      // Set the rating using the attached $rating property.
      $overallRating[0].$rating.setRating(newRating);
      // Show value with two decimal digits.
      $overallRatingText.text(newRating.toFixed(2));
    }

    $sourceRatings.each(function () {
      $(this).on('change', updateOverallRating);
    });

    updateOverallRating();
  })(); // Self-invoked
});
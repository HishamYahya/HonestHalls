"use strict";
document.addEventListener("DOMContentLoaded", function() {
  // Obtain a reference to the marker <template>
  const $mapMarkerTemplate = $("#hh-map-marker-template");

  /**
   * Creates the markup for a map marker.
   */
  function createMapMarkerHtml(hall) {
    // Clone the template's content
    const clonedFragment = $mapMarkerTemplate[0].content.cloneNode(true);
    const $clone = $(clonedFragment.children[0]);
    $clone.attr("data-hall-id", hall.id);
    $clone.attr("href", "#hall-" + hall.id);
    $clone.find(".hh-map-marker__hall").text(hall.name);
    $clone.find(".hh-map-marker__campus").text(hall.campus);
    return $clone[0].outerHTML;
  }

  /**
   * Initializes the map.
   */
  function initializeMap(halls) {
    // Get the root element.
    const mapRoot = document.getElementById("map-root");
    // Initialize HERE maps.
    const platform = new H.service.Platform({
      apikey: "zMLjDHu9EnmCM9th-7gPJMY5NnCa6ZMxGaAGII2aXyc"
    });

    // Obtain the default map types from the platform object:
    const defaultLayers = platform.createDefaultLayers();

    // Instantiate (and display) a map object:
    const map = new H.Map(mapRoot, defaultLayers.vector.normal.map, {
      zoom: 14,
      center: { lat: 53.4518969, lng: -2.2349833 } // Focus right around Hulme hall
    });

    const ui = H.ui.UI.createDefault(map, defaultLayers);
    const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

    for (let hall of halls) {
      // Define a variable holding the markup for the marker.
      const markerHtml = createMapMarkerHtml(hall);
      // Create an icon, an object holding the latitude and longitude, and a marker:
      const icon = new H.map.DomIcon(markerHtml);
      // Specify the coordinates in the required form.
      const coords = { lat: hall.latitude, lng: hall.longitude };
      const marker = new H.map.DomMarker(coords, { icon: icon });
      // Add the marker to the map and center the map at the location of the marker:
      map.addObject(marker);
    }

    let focusedHall = null;
    function focusHall(id, center) {
      const hall = halls.find(x => x.id == id);
      if (!hall) {
        throw new Error("Cannot find hall with ID=" + id);
      }

      if (center) {
        map.setCenter({ lat: hall.latitude, lng: hall.longitude });
      }
      $('[data-hall-id]').removeClass('focused');
      $('[data-hall-id="' + id + '"]').addClass('focused');
      focusedHall = hall;
    }

    function tryFocusAnchorHall(id) {
      if (location.hash.indexOf('#hall-') === 0) {
        const id = location.hash.substr('#hall-'.length) | 0;
        focusHall(id, true);
      }
    }

    $('body').on('click', function(event) {
      const $target = $(event.target).parents('[data-hall-id]');
      if ($target.length) {
        const id = $target.attr('data-hall-id') | 0;
        focusHall(id, true);
      }
    });

    let areMarkersInit = false;
    function initializeMapMarkers() {
      if ($('.hh-map-marker').length) {
        // First load of the map. Focus the map in the hash.
        if (!areMarkersInit) {
          areMarkersInit = true;
          tryFocusAnchorHall();
        }
        // Need to re-add .focus to the marker if it
        // wasn't onscreen when the hall was focused.
        if (focusedHall != null) {
          focusHall(focusedHall.id, true);
        }
      }
    }

    // Call every 50 ms to run initialization logic once the map has loaded.
    const intervalID = setInterval(initializeMapMarkers, 50);
  }

  // Get the halls data from the injected script tag.
  const halls = JSON.parse(document.getElementById("hall-data-json").innerHTML);

  initializeMap(halls);
});

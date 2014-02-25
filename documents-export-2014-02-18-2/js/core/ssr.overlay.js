/**
 * Sub-namespace.
 * @type {Object}
 */
SSR.overlay = {};


/**
 * Overlay node.
 * @type {Object}
 */
SSR.overlay.overlay = null;


/**
 * Bookmark node.
 * @type {Object}
 */
SSR.overlay.bookmark = null;


/**
 * Print node.
 * @type {Object}
 */
SSR.overlay.print = null;


/**
 * Flags if any overlay is currently being shown.
 * @type {boolean}
 */
SSR.overlay.visible = false;


/**
 * Initialize overlay class.
 */
SSR.overlay.initialize = function() {
  SSR.overlay.overlay = $('#overlay');
  SSR.overlay.bookmark = $('#overlay div.bookmark');
  SSR.overlay.print = $('#overlay div.print');
};


/**
 * Shows the overlay with the bookmark that allows users to pick up where they
 * left off or start over.
 * @param {Object} continueCallback Callback for 'continue' response.
 * @param {Object} restartCallback Callback for 'restart' response.
 * @param {Object} cancelCallback Callback for 'cancel' response.
 */
SSR.overlay.showBookmark = function(continueCallback, restartCallback,
    cancelCallback) {
  SSR.overlay.overlay.stop().fadeIn(200);
  SSR.overlay.bookmark.siblings().hide();
  SSR.overlay.bookmark.stop().fadeIn(200);

  $('a.resume', SSR.overlay.bookmark).click(function() {
    SSR.overlay.hide();
    continueCallback();

    return false;
  });

  $('a.restart', SSR.overlay.bookmark).click(function() {
    SSR.overlay.hide();
    restartCallback();

    return false;
  });

  $('a.close', SSR.overlay.bookmark).click(function() {
    SSR.overlay.hide();
    cancelCallback();

    return false;
  });

  SSR.overlay.visible = true;
  SSR.overlay.hasShownBookmark = true;

  SSR.pageflip.unregisterEventListeners();

  $('body').addClass('overlay');
};


/**
 * Shows the print dialog.
 */
SSR.overlay.showPrint = function() {
  SSR.overlay.overlay.stop().fadeIn('fast');
  SSR.overlay.print.siblings().hide();
  SSR.overlay.print.stop().fadeIn('fast');

  $('a.close', SSR.overlay.print).click(function() {
    SSR.overlay.hide();

    return false;
  });

  $('a.downloadPdf.disabled', SSR.overlay.print).click(function() {
    return false;
  });

  SSR.overlay.visible = true;

  SSR.pageflip.unregisterEventListeners();

  $('body').addClass('overlay');
};


/**
 * Hides any currently open overlay window (print or bookmark).
 */
SSR.overlay.hide = function() {
  SSR.overlay.overlay.stop().fadeOut('fast');
  SSR.overlay.bookmark.stop().fadeOut('fast');
  SSR.overlay.print.stop().fadeOut('fast');

  SSR.overlay.visible = false;

  SSR.pageflip.registerEventListeners();

  $('body').removeClass('overlay');
};
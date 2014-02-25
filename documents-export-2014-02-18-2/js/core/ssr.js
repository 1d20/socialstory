/**
 * Global namespace.
 * @type {Object}
 */
var SSR = SSR || {};

/**
 * The width of one page (excluding jacket) in the book.
 * @type {number}
 */
SSR.PAGE_WIDTH = 800;


/**
 * The height of one page (excluding jacket) in the book.
 * @type {number}
 */
SSR.PAGE_HEIGHT = 500;


/**
 * Minimum width of the whole app (when scaled to be smaller than this,
 * scrollbars will appear).
 * @type {number}
 */
SSR.PAGE_MIN_WIDTH = 1000;


/**
 * Minimum width of the whole app (when scaled to be smaller than this,
 * scrollbars will appear).
 * @type {number}
 */
SSR.PAGE_MIN_HEIGHT = 680;


/**
 * Inner margin (x) of the book (space between where the book jacket and white
 * paper).
 * @type {number}
 */
SSR.PAGE_MARGIN_X = 32;


/**
 * Inner margin (y) of the book (space between where the book jacket and white
 * paper).
 * @type {number}
 */
SSR.PAGE_MARGIN_Y = 10;


/**
 * The total width of the book, including jacket.
 * @type {number}
 */
SSR.BOOK_WIDTH = 1660;


/**
 * The total width of the book, including jacket.
 * @type {number}
 */
SSR.BOOK_HEIGHT = 520;


/**
 * The width of the closed book, including jacket.
 * @type {number}
 */
SSR.BOOK_WIDTH_CLOSED = SSR.BOOK_WIDTH / 2;


/**
 * An offset applied to the horizontal positioning of the book (#book).
 * @type {number}
 */
SSR.BOOK_OFFSET_X = 5;


/**
 * User agent.
 * @type {string}
 */
SSR.UA = navigator.userAgent.toLowerCase();


/**
 * Whether UA is a touch device.
 * @type {boolean}
 */
SSR.IS_TOUCH_DEVICE = SSR.UA.match(/android/) || SSR.UA.match(/iphone/) ||
    SSR.UA.match(/ipad/) || SSR.UA.match(/ipod/);


/**
 * Initiates the main application logic. This is the first point at which any
 * scripting logic is applied.
 */
SSR.initialize = function() {

  // SSR.preloader.initialize();

  console.time('Loading contents');
  SSR.contents.initialize();
  console.timeEnd('Loading contents');

  // Initialize managers, do not alter the order in which these are called.
  // SSR.overlay.initialize();
  // SSR.storage.initialize();
  // SSR.cache.initialize();
  // SSR.search.initialize();
  // SSR.chapternav.initialize();
  // SSR.sharing.initialize();
  // SSR.paperstack.initialize();
  // SSR.tableofthings.initialize();
  // SSR.flipintro.initialize();

  // // Register event listeners.
  // $(window).resize(SSR.onWindowResize);
  // $(window).scroll(SSR.onWindowScroll);

  // // Trigger an initial update of the layout.
  // SSR.updateLayout();

  // Prevent native drag and drop behavior of all images. This is important
  // since it is very easy to start dragging assets by mistake while trying to
  // flip pages.
  // $('img').mousedown(function(event) { event.preventDefault() });
  // $("#container").turn({
  //     width: 1170,
  //     height: 720,
  //     // autoCenter: true
  //   });
};


/**
 * Outputs a log of the passed in object. This is centralized in one method so
 * that we can keep info logs around the site and easily disable/enable them
 * when jumping between live/dev.
 * @param {string} o Message to log to console.
 */
SSR.log = function(o) {
  if (window.console) {
    window.console.log(o);
  }
};


/**
 * A global shorthand for retrieving the current time.
 * @return {Object} Date object.
 */
SSR.time = function() {
  return new Date().getTime();
};


/**
 * Assign namespace to window object.
 */
window['SSR'] = SSR;
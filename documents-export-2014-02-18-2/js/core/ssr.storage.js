/**
 * Sub-namespace.
 * @type {Object}
 */
SSR.storage = {};


/**
 * First time visitor flag.
 */
SSR.storage.isFirstTimeVisitor = true;


/**
 * Storage contents.
 */
SSR.storage.contents = '';


/**
 * Article list.
 */
SSR.storage.data = {
  articles: {}, // Contains deeplink:html pairs
  progress: {}, // Contains deeplink:read_flag pairs
  bookmark: {
    articleId: '',
    pageNumber: ''
  }
};


/**
 * Initialize storage class.
 */
SSR.storage.initialize = function() {
  SSR.storage.routeDataRequest();
};


/**
 * Load local storage data.
 */
SSR.storage.load = function() {
  if (SSR.storage.supportsLocalStorage() && localStorage.data) {
    SSR.storage.data = $.parseJSON(localStorage.data);
  }
};


/**
 * Save local storage data.
 */
SSR.storage.save = function() {
  if (SSR.storage.supportsLocalStorage()) {
    localStorage.data = $.toJSON(SSR.storage.data);
  }
};


/**
 * Check for localStorage support.
 * @return {boolean} Whether UA supports local storage.
 */
SSR.storage.supportsLocalStorage = function() {
  return ('localStorage' in window) && window['localStorage'] !== null;
};


/**
 * Get articles from server, append to DOM and put in local storage.
 */
SSR.storage.getArticlesFromServer = function() {
  SSR.log('Getting articles from server');

  // Get a fresh listing of all disabled articles.
  var disabledArticles = SSR.chapternav.getDisabledArticles();

  $.ajax({
    url: '/' + SERVER_VARIABLES.LANG + '/all',
    contentType: 'text/html;charset=UTF-8',
    success: function(data) {

      var globalPageCounter = 0;

      SSR.storage.data.articles = {};

      $(data).each(function() {
        var articleId = $(this).attr('id');
        $(this).find('section').each(function(i) {
          globalPageCounter++;

          $(this).addClass('globalPage-' + globalPageCounter).css('zIndex',
              500 - globalPageCounter).hide();

          // If local storage is supported, save the content for this page.
          if (SSR.storage.supportsLocalStorage()) {
            SSR.storage.data.articles['/' + articleId + '/' + (i + 1)] =
                $('<div>').append($(this).clone()).remove().html();
          }

          var articleIsDisabled = false;

          // Check if this article is disabled.
          for (var i = 0; i < disabledArticles.length; i++) {
            if (disabledArticles[i] == articleId) {
              articleIsDisabled = true;
            }
          }

          // Only render the article if its not disabled.
          if (articleIsDisabled == false) {
            $('#pages').append($('<div>').append($(this).clone()).remove()
                .html());
          }
        });
      });

      SSR.storage.save();

      SSR.storage.onFindBookmark();
      SSR.storage.activateCurrentPageAndSetPageCount();
    }
  });
};


/**
 * Get articles from server translated.
 */
SSR.storage.getArticlesFromServerTranslated = function() {
  SSR.log('getting articles from server');

  // Get a fresh listing of all disabled articles.
  var disabledArticles = SSR.chapternav.getDisabledArticles();

  $.ajax({
    url: '/all',
    contentType: 'text/html;charset=UTF-8',
    success: function(data) {

      var globalPageCounter = 0;

      SSR.storage.data.articles = {};

      $(data).each(function() {
        var articleId = $(this).attr('id');
        $(this).find('section').each(function(i) {
          globalPageCounter++;

          $(this).addClass('globalPage-' +
              globalPageCounter).css('zIndex', 500 - globalPageCounter).hide();

          // If local storage is supported, save the content for this page.
          if (SSR.storage.supportsLocalStorage()) {
            SSR.storage.data.articles['/' + articleId + '/' + (i + 1)] =
                $('<div>').append($(this).clone()).remove().html();
          }

          var articleIsDisabled = false;

          // Check if this article is disabled.
          for (var i = 0; i < disabledArticles.length; i++) {
            if (disabledArticles[i] == articleId) {
              articleIsDisabled = true;
            }
          }

          // Only render the article if its not disabled.
          if (articleIsDisabled == false) {
            $('#pages').append($('<div>')
                .append($(this).clone()).remove().html());
          }
        });
      });

      SSR.storage.save();

      SSR.storage.onFindBookmark();
      SSR.storage.activateCurrentPageAndSetPageCount();

    }
  });
};


/**
 * Get articles from local storage and append to DOM.
 */
SSR.storage.getArticlesFromStorage = function() {
  SSR.log('Getting articles from storage');

  // Flag that this is not a first time visitor.
  SSR.storage.isFirstTimeVisitor = false;

  if (localStorage.data) {
    SSR.storage.data = $.parseJSON(localStorage.data);
  }
  else {

    // If there is no data in local storage we have to update.
    SSR.storage.getArticlesFromServer();
    return;
  }

  // Get a fresh listing of all disabled articles.
  var disabledArticles = SSR.chapternav.getDisabledArticles();

  for (var articlePath in SSR.storage.data.articles) {
    var articleIsDisabled = false;

    // Check if this article is disabled.
    for (var i = 0; i < disabledArticles.length; i++) {
      if (disabledArticles[i] == articlePath.split('/')[1]) {
        articleIsDisabled = true;
      }
    }

    // Only render the article if its not disabled.
    if (articleIsDisabled == false) {
      $('#pages').append(SSR.storage.data.articles[articlePath]);
    }

  }

  SSR.storage.onFindBookmark();
  SSR.storage.activateCurrentPageAndSetPageCount();

};


/**
 * Route data request to server or local storage.
 */
SSR.storage.routeDataRequest = function() {

  if (!SSR.storage.supportsLocalStorage()) {

    SSR.storage.getArticlesFromServer();

  } else {

    SSR.log('Version on server is: ' + SERVER_VARIABLES.SITE_VERSION);

    if (SERVER_VARIABLES.SITE_VERSION != localStorage.version ||
        SERVER_VARIABLES.LANG != localStorage.lang) {
      localStorage.version = SERVER_VARIABLES.SITE_VERSION;
      localStorage.lang = SERVER_VARIABLES.LANG;
      SSR.storage.getArticlesFromServer();
    } else {
      SSR.storage.getArticlesFromStorage();
    }

  }
};


/**
 * Take original article and insert into dynamically loaded list;
 * set current page number.
 */
SSR.storage.activateCurrentPageAndSetPageCount = function() {
  var $origArticle = $('#pages section').eq(0);
  $origArticle.attr('id', 'original');

  $('#pages section:not(#original)').each(function(i) {
    if ($(this).hasClass($origArticle.attr('class'))) {
      $origArticle.remove();
      $(this).addClass('current').show().next('section').show();
      $('<span id="currentPage">' + parseFloat(i + 1) + '</span>')
          .appendTo('body');
    }
  });

  if ($('#pages section.current').length === 0) {
    $('#pages section').first().addClass('current');
  }

  $('#pages section div.page').each(function(i) {
    $(this).append('<span class="pageNumber">' + (i + 1) + '</span>');
  });


  // If the app starts with a "view" class (home/credits) then we need to
  // manually select the current page.
  if ($('body').hasClass('home')) {
    $('#pages section').removeClass('current');
    $('#pages section').first().addClass('current');
  }
  else if ($('body').hasClass('credits')) {
    $('#pages section').removeClass('current');
    $('#pages section').last().addClass('current');
  }

  SSR.preloader.onContentsLoaded();
};


/**
 * Check for bookmark and prompt to resume.
 */
SSR.storage.onFindBookmark = function() {
  if (SSR.storage.supportsLocalStorage()) {
    if (SSR.storage.data.bookmark.articleId &&
        $('#pagination-prev').hasClass('inactive') &&
        !(SSR.storage.data.bookmark.articleId == $('#articleId').text() &&
        SSR.storage.data.bookmark.pageNumber == $('#pageNumber').text())) {

      SSR.log('Bookmark found: ' + SSR.storage.data.bookmark.articleId + '/' +
          SSR.storage.data.bookmark.pageNumber);

      // Show the bookmark and await callbacks.
      SSR.overlay.showBookmark(function() {

        // Continuie handler.
        SSR.navigation.goToPage(SSR.storage.data.bookmark.articleId,
            SSR.storage.data.bookmark.pageNumber);
      }, function() {

        // Restart handler.
        SSR.navigation.goToHome();
      }, function() {

        // Cancel handler
        SSR.storage.setBookmark($('#articleId').text(), $('#pageNumber').text());
      });

      SSR.log('Bookmark found: ' + SSR.storage.data.bookmark.articleId + '/' +
          SSR.storage.data.bookmark.pageNumber);
    }
    else {
      SSR.storage.setBookmark($('#articleId').text(), $('#pageNumber').text());
    }
  }
};


/**
 * Set bookmark and read/unread state.
 * @param {string} articleId Article ID.
 * @param {number} pageNumber Page number.
 */
SSR.storage.setBookmark = function(articleId, pageNumber) {
  if (SSR.storage.supportsLocalStorage() && articleId != SSR.history.THEEND) {

    // Set data.
    SSR.storage.data.bookmark.articleId = articleId;
    SSR.storage.data.bookmark.pageNumber = pageNumber;
    SSR.storage.data.progress['/' + articleId + '/' + pageNumber] = true;

    // Save data.
    SSR.storage.save();

    SSR.chapternav.updateReadMarkers();
    SSR.tableofthings.updateReadMarkers();
  }
};


/**
 * Check if article has been read.
 * @param {string} articleId Article ID.
 * @return {boolean} Whether article has been read.
 */
SSR.storage.hasArticleBeenRead = function(articleId) {
  return SSR.storage.data.progress['/' + articleId + '/1'] == true;
};
/**
 * Sub-namespace.
 * @type {Object}
 */
SSR.notes = {};


/**
 * Notes array.
 * @type {Object}
 */
SSR.notes.notes = null;


/**
 * Toolbar object.
 * @type {Object}
 */
SSR.notes.toolbar = null;


/**
 * Toolbar object.
 * @type {Object}
 */
SSR.notes.toolbar = null;


/**
 * Initialize notes class.
 */
SSR.notes.initialize = function() {
    SSR.notes.toolbar = SSR.notes.createToolbar();
    SSR.notes.form = SSR.notes.createNotesForm();
    SSR.notes.notes = SSR.notes.getElements();
    SSR.notes.createNotesPlaceholders();
    SSR.notes.bindElementsEvents();

    SSR.contents.getAllComments();
};

/**
 * Get all elements that have data-element-id attribute
 */
SSR.notes.getElements = function() {
    return document.querySelectorAll('[data-element-id]');
}


SSR.notes.checkSelection = function() {
    var i,
        newSelection,
        hasMultiParagraphs,
        selectionHtml,
        selectionElement;

    if (this.keepToolbarAlive !== true) {
        newSelection = window.getSelection();
        selectionHtml = SSR.contents.getSelectionHtml();
        selectionHtml = selectionHtml.replace(/<[\S]+><\/[\S]+>/gim, '');
        // Check if selection is between multi paragraph <p>.
        hasMultiParagraphs = selectionHtml.match(/<(p|h[0-6]|blockquote|pre|ul) data-element-id=\"(.+)\">([\s\S]*?)<\/(p|h[0-6]|blockquote|pre|ul)>/g);
        hasMultiParagraphs = hasMultiParagraphs ? hasMultiParagraphs.length : 0;
        if (newSelection.toString().trim() === '' || hasMultiParagraphs) {
            this.hideToolbarActions();
        } else {
            selectionElement = SSR.contents.getSelectionElement();
            if (!selectionElement || selectionElement.getAttribute('data-disable-toolbar')) {
                this.hideToolbarActions();
            } else {
                this.selection = newSelection;
                this.selectionRange = this.selection.getRangeAt(0);

                this.setToolbarPosition()
                    .showToolbarActions();
            }
        }
    }

};


SSR.notes.setToolbarPosition = function() {
    var self = this;
    var buttonHeight = 50,
        selection = window.getSelection(),
        range = selection.getRangeAt(0),
        boundary = range.getBoundingClientRect(),
        defaultLeft = 0 - (self.toolbar.offsetWidth / 2),
        middleBoundary = (boundary.left + boundary.right) / 2,
        halfOffsetWidth = self.toolbar.offsetWidth / 2;

    self.toolbar.style.top = boundary.top + (-10) + window.pageYOffset - self.toolbar.offsetHeight + 'px';
    if (middleBoundary < halfOffsetWidth) {
        self.toolbar.style.left = defaultLeft + halfOffsetWidth + 'px';
    } else if ((window.innerWidth - middleBoundary) < halfOffsetWidth) {
        self.toolbar.style.left = window.innerWidth + defaultLeft - halfOffsetWidth + 'px';
    } else {
        self.toolbar.style.left = defaultLeft + middleBoundary + 'px';
    }
    return this;
}

SSR.notes.createToolbar = function() {
    var toolbar = document.createElement('div');

    SSR.contents.reader.appendChild(toolbar);

    toolbar.classList.add('notes-toolbar');
    toolbar.classList.add('btn-group');

    toolbar.innerHTML =
        '<div class="notes-toolbar-button btn btn-default" data-action="add-comment" title="Написать комментарий"><i class="fa fa-comments"></i></div>' +
        '<div class="notes-toolbar-button btn btn-default" data-action="add-note" title="Добавить в заметки"><i class="fa fa-quote-left"></i></div>' +
        '<div class="notes-toolbar-button btn btn-default" data-action="add-bookmark" title="Добавить закладку"><i class="fa fa-bookmark"></i></div>';

    $(toolbar.querySelector('[data-action="add-comment"]')).on('click', function(e) {
        e.preventDefault();
        $('[data-note-comment-title]', $(SSR.notes.form)).text('Залишити коментар');
        SSR.notes.showNotesForm();
    });
    $(toolbar.querySelector('[data-action="add-note"]')).on('click', function(e) {
        e.preventDefault();
        SSR.notes.addNote();
    });
    $(toolbar.querySelector('[data-action="add-bookmark"]')).on('click', function(e) {
        e.preventDefault();
        SSR.notes.addBookmark();
    });

    return toolbar;
};

SSR.notes.hideToolbarActions = function() {
    this.keepToolbarAlive = false;
    this.toolbar.classList.remove('active');
    SSR.notes.clearSelection();
};

SSR.notes.showToolbarActions = function() {
    var self = this,
        timer;
    this.keepToolbarAlive = false;
    clearTimeout(timer);
    timer = setTimeout(function() {
        if (!self.toolbar.classList.contains('active')) {
            self.toolbar.classList.add('active');
        }
    }, 100);

    return this;
};


SSR.notes.createNotesPlaceholders = function() {
    for (var i = SSR.notes.notes.length - 1; i >= 0; i--) {
        var note = document.createElement('div');
        SSR.notes.notes[i].appendChild(note);

        note.style.top = parseInt(SSR.notes.notes[i].offsetTop) + 'px';

        if (SSR.notes.notes[i].parentElement.parentElement.classList.contains('ssr-page-left')) {
            note.style.left = parseInt(SSR.notes.notes[i].offsetLeft) +
                parseInt(SSR.notes.notes[i].offsetWidth) - 20 + 'px';
        } else {
            note.style.left = parseInt(SSR.notes.notes[i].offsetLeft) + 'px';
        }

        note.dataset.noteId = SSR.notes.notes[i].dataset.elementId;

        SSR.notes.bindNoteHandlers(note);
    };
}


SSR.contents.getAllComments = function() {
    $.ajax({
        url: '/writer/comments/count/' + SSR.contents.branchId + '/',
        data: {
            csrfmiddlewaretoken: SSR.contents.csrfmiddlewaretoken
        },
        type: 'POST',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            if (response.data) {
                for (var i = response.data.length - 1; i >= 0; i--) {
                    $('[data-note-id="' + response.data[i].paragraph_index + '"]').text(response.data[i].count).addClass('hovered');
                };
            }
        }
    });
};


SSR.notes.bindElementsEvents = function() {
    for (var i = SSR.notes.notes.length - 1; i >= 0; i--) {
        var note = SSR.notes.notes[i];

        $(note)
            .on('mouseover', SSR.notes.elementMouseOverHandler)
            .on('mouseleave', SSR.notes.elementMouseLeaveHandler);

    };
};


SSR.notes.elementMouseOverHandler = function() {
    var note = document.querySelector('[data-note-id="' + this.dataset.elementId + '"]');
    if (!note.classList.contains('hovered')) {
        note.classList.add('hovered');
    }
};


SSR.notes.elementMouseLeaveHandler = function() {
    var note = document.querySelector('[data-note-id="' + this.dataset.elementId + '"]');
    if (note.innerText == '') {
        note.classList.remove('hovered');
    }
};


SSR.notes.elementClickHandler = function(event, that) {
    console.log('click at ' + this.toString());
    event.preventDefault();

    SSR.notes.noteFormClickHandler(event, that);
};


SSR.notes.bindNoteHandlers = function(note) {

    $(note)
        .on('mouseover', SSR.notes.noteFormMouseOverHandler)
        .on('mouseleave', SSR.notes.noteFormMouseLeaveHandler)
        .on('click', function(event) {
            SSR.notes.elementClickHandler(event, this);
        });

};


SSR.notes.noteFormClickHandler = function(event, element) {
    event.preventDefault();

    this.showToolbarActions();

};


SSR.notes.noteFormMouseOverHandler = function(event) {
    if (!this.classList.contains('hovered')) {
        this.classList.add('hovered');
    }
}


SSR.notes.noteFormMouseLeaveHandler = function(event) {
    if (this.innerText == '') {
        this.classList.remove('hovered');
    }
};


SSR.notes.createNotesForm = function() {
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

    var form = document.createElement('div');

    SSR.contents.reader.appendChild(form);

    form.classList.add('modal');
    form.classList.add('fade');

    form.innerHTML = '<div class="modal-dialog">' +
        '<div class="modal-content">' +
        '<div class="modal-header">' +
        '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' +
        ' <h4 class="modal-title" data-note-comment-title></h4>' +
        '</div>' +
        ' <div class="modal-body">' +
        '  <form id="post-note"">' +
        '     <div class="form-group">' +
        '       <label>' +
        '         <input name="private" type="checkbox"> Виправлення' +
        '       </label>' +
        '    </div>' +
        '   <input type="hidden" name="csrfmiddlewaretoken">' +
        '   <input type="hidden" name="paragraph_index">' +
        '   <input type="hidden" name="first_char">' +
        '   <input type="hidden" name="last_char">' +
        '   <div class="well text-muted" data-note-comment-text></div>' +
        '   <input type="text" name="content" class="form-control">' +
        '    </form>' +
        '   <hr>' +
        '  <ul class="media-list"></ul>' +
        ' </div>' +
        ' <div class="modal-footer">' +
        '   <button type="button" class="btn btn-default" data-dismiss="modal">Вiдмiна</button>' +
        '   <button type="button" class="btn btn-primary" data-note-comment-confirm>Залишити коментар</button>' +
        ' </div>' +
        ' </div><!-- /.modal-content -->' +
        ' </div>';

    form.id = 'notes-form';

    $('[data-note-comment-confirm]', $(form)).on('click', function(e) {
        e.preventDefault();

        SSR.notes.postNote();
    });

    $('[name="csrfmiddlewaretoken"]', $(form)).val(csrfmiddlewaretoken);

    return form;
};

SSR.notes.showNotesForm = function() {
    var paragraph_index = SSR.notes.getElementWithIdOfSelection();
    var first_char = (window.getSelection().baseOffset < window.getSelection().extentOffset) ? window.getSelection().baseOffset : window.getSelection().extentOffset;
    var last_char = (window.getSelection().baseOffset > window.getSelection().extentOffset) ? window.getSelection().baseOffset : window.getSelection().extentOffset;

    $('[name="paragraph_index"]', $(SSR.notes.form)).val(paragraph_index);
    $('[name="first_char"]', $(SSR.notes.form)).val(first_char);
    $('[name="last_char"]', $(SSR.notes.form)).val(last_char);
    $('[data-note-comment-text]', $(SSR.notes.form)).text(this.selection);
    $('[name="content"]', $(SSR.notes.form)).val('');

    var branchId = SSR.contents.reader.dataset.branchId;

    $.ajax({
        url: '/writer/comments/get/' + branchId + '/' + paragraph_index + '/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]', $(SSR.notes.form)).val()
        },
        dataType: 'json',
        success: function(response) {

            var mediaList = $('.media-list', $(SSR.notes.form));
            var newHtml = '';

            for (var i = 0; i < response.data.length; i++) {
                var comment = response.data[i];

                newHtml += '<li class="media">' +
                    '                            <div class="pull-left">' +
                    '                             <img class="media-object media-object-min" src="' + comment.writer_avatar + '" alt="' + comment.writer_name + '">' +
                    '                          </div>' +
                    '                         <div class="media-body">' +
                    '                          <h4 class="media-heading">' + comment.writer_name + '<small class="text-muted">' + comment.date + '</small></h4>' +
                    '                         <p>' + comment.content + '</p>' +
                    '                      </div>' +
                    '                 </li>';

            };

            mediaList.html(newHtml);

            $(SSR.notes.form).modal();
        },
        error: function(response) {
            console.log(response);
        }
    });
};


SSR.notes.postNote = function() {
    var branchId = SSR.contents.reader.dataset.branchId;
    var paragraph = $('[name="paragraph_index"]', $(SSR.notes.form)).val();

    $.ajax({
        url: '/writer/comment/add/' + branchId + '/',
        data: $('#post-note').serialize(),
        type: 'POST',
        dataType: 'json',
        success: function(response) {
            $(SSR.notes.form).modal('hide');
        },
        error: function(response) {
            $(SSR.notes.form).modal('hide');
            console.log(response);
        },
        fail: function(response) {
            $(SSR.notes.form).modal('hide');
            console.log(response);
        }
    });

};


SSR.notes.getElementWithIdOfSelection = function() {
    var getParent = function(element) {
        if (element.dataset.elementId) {
            return element.dataset.elementId;
        } else {
            getParent(element.parentElement);
        }
    }

    return getParent(window.getSelection().baseNode.parentElement);
};

SSR.notes.addNote = function() {
    var data = {};
    data.csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]', $(SSR.notes.form)).val();
    data.paragraph_index = SSR.notes.getElementWithIdOfSelection();
    $('[data-note-comment-text]', $(SSR.notes.form)).text(this.selection);
    data.content = $('[data-note-comment-text]', $(SSR.notes.form)).text();

    $.ajax({
        url: '/writer/note/add/' + SSR.contents.reader.dataset.branchId + '/',
        data: data,
        type: 'POST',
        dataType: 'json',
        success: function(response) {
            if (response.result) {
                SSR.notes.hideToolbarActions();
            } else {
                alert('Error');
            }
        }
    });
    SSR.notes.hideToolbarActions();
};

SSR.notes.addBookmark = function() {
    var data = {};
    data.csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]', $(SSR.notes.form)).val();
    data.paragraph_index = SSR.notes.getElementWithIdOfSelection();

    $.ajax({
        url: '/writer/mark/add/' + SSR.contents.reader.dataset.branchId + '/',
        data: data,
        type: 'POST',
        dataType: 'json',
        success: function(response) {
            if (response.result) {
                SSR.notes.hideToolbarActions();
            } else {
                alert('Error');
            }
        }
    });

    SSR.notes.hideToolbarActions();
};


SSR.notes.clearSelection = function() {
    if (window.getSelection) window.getSelection().removeAllRanges();
    else if (document.selection) document.selection.empty();
}
/**
 * Sub-namespace.
 * @type {Object}
 */
SSR.contents = {};


/**
 * Content node.
 * @type {Object}
 */
SSR.contents.contents = null;


/**
 * Content node.
 * @type {Object}
 */
SSR.contents.container = null;


/**
 * Contents buffer.
 * @type {String}
 */
SSR.contents.contents_buffer = '';


/**
 * Reader node.
 * @type {Object}
 */
SSR.contents.reader = null;


/**
 * Pages nodes.
 * @type {Object}
 */
SSR.contents.pages = null;


/**
 * Page index.
 * @type {number}
 */
SSR.contents.page_index = 0;


/**
 * Current page index.
 * @type {number}
 */
SSR.contents.current_page_index = 0;


/**
 * Content children nodes.
 * @type {Object}
 */
SSR.contents.children = null;


/**
 * Flags if any content is currently being shown.
 * @type {boolean}
 */
SSR.contents.visible = false;


/**
 * Initialize contents class.
 */
SSR.contents.initialize = function() {
  SSR.contents.reader = document.getElementById('reader');
  SSR.contents.contents = document.getElementById('content');
  SSR.contents.container = document.getElementById('container');

  SSR.contents.getChildren();
  SSR.contents.setPageContents();
};


/**
 * Get all child nodes of contents
 */
SSR.contents.getChildren = function(){
	SSR.contents.children = SSR.contents.contents.children;
};


/**
 * Set all child nodes to pages
 */
SSR.contents.setPageContents = function(){
	if (SSR.contents.page_index === 0) {
		var firstPage = document.createElement('div');
		var innerPage = document.createElement('div');

		SSR.contents.container.appendChild(firstPage);
		
		firstPage.setAttribute('class', 'ssr-page ssr-page-left');
		firstPage.style.zIndex = 10000 - SSR.contents.current_page_index;
		firstPage.appendChild(innerPage);

		innerPage.setAttribute('class', 'ssr-page-inner');
		innerPage.setAttribute('id', 'ssr-page-' + SSR.contents.current_page_index);
		
		SSR.contents.page_index = 1;
	}

	var page = document.getElementById('ssr-page-'+SSR.contents.current_page_index);

	var node = SSR.contents.children[0];

	if (node) {
		page.appendChild(node);

		var lineHeight = parseInt(document.defaultView.getComputedStyle(node, null).getPropertyValue('line-height'));

		if (node.offsetTop + lineHeight > page.offsetTop + page.offsetHeight) {
			page.removeChild(page.childNodes[page.childNodes.length - 1]);
			page = SSR.contents.addNewPage();
			page.appendChild(node);
		} 

		if (! SSR.contents.nodeFitsThePage(page, node)) {
			SSR.contents.initNodeTransfer(page, node);
		}

		// Recursively fulfill
		SSR.contents.setPageContents();
	}
};


SSR.contents.addNewPage = function(){
	SSR.contents.page_index++;
	SSR.contents.current_page_index++;

	var page = document.createElement('div');
	var innerPage = document.createElement('div');
	var className = 'ssr-page' + (SSR.contents.current_page_index % 2 === 0 ? ' ssr-page-left' : '');

	SSR.contents.container.appendChild(page);

	page.setAttribute('class', className);
	page.style.zIndex = 10000 - SSR.contents.current_page_index;
	page.appendChild(innerPage);

	innerPage.setAttribute('class', 'ssr-page-inner');
	innerPage.setAttribute('id', 'ssr-page-' + SSR.contents.current_page_index);

	return innerPage;
}


/**
 * Check if node fits.
 * @param page {Node}
 * @param node {Node}
 */
SSR.contents.nodeFitsThePage = function(page, node){
	return (node.offsetTop + node.offsetHeight <
			page.offsetTop + page.offsetHeight );
};


/**
 * Populate contents buffer with overflowing words and
 * check in loop until node fits the page
 * @param page {Node}
 * @param node {Node}
 */
SSR.contents.initNodeTransfer = function(page, node){
	node.innerHTML = node.innerHTML.trim();
	var innerHTML = node.innerHTML;

	// console.time('Transfering');

	SSR.contents.cropNodeForOverflow(page,node);

	do {

		SSR.contents.contents_buffer = ' ' + node.innerHTML.split(' ').slice(-1) + SSR.contents.contents_buffer;
		node.innerHTML = node.innerHTML.split(' ').slice(0,-1).join(' ');
	} while (!SSR.contents.nodeFitsThePage(page, node));

	// console.timeEnd('Transfering');
	
	var closingTags = node.innerHTML.match(/<\/\S+>$/);

	if (closingTags) {
		var openingTags = closingTags[0].replace(/\//g,'');
		SSR.contents.contents_buffer = openingTags + innerHTML.slice(node.innerHTML.length - closingTags[0].length);
	} else {
		SSR.contents.contents_buffer = innerHTML.slice(node.innerHTML.length);
	}

	node.setAttribute('class', 'continuation');
	
	if (node.innerHTML.length === 0) {
		page.removeChild(page.childNodes[page.childNodes.length - 1]);
	}

	var newNode = SSR.contents.creaetNodeFromTransferedContent(node.nodeName);

	page = SSR.contents.addNewPage();
	page.appendChild(newNode);
	
	if (! SSR.contents.nodeFitsThePage(page, newNode)) {
		SSR.log(page);
		SSR.contents.initNodeTransfer(page, newNode);
	}
};


/**
 * Crop some lines from node
 * @param page {Node}
 * @param node {Node}
 */
SSR.contents.cropNodeForOverflow = function(page, node){
	var lineHeight = parseInt(document.defaultView.getComputedStyle(node, null).getPropertyValue('line-height'));
	var totalLines = Math.floor(node.offsetHeight / lineHeight);
	var overflow = Math.abs(node.offsetTop + node.offsetHeight - (page.offsetTop + page.offsetHeight));
	var overflowedLines = Math.floor(overflow / lineHeight);
	var overflowedChars = node.innerHTML.length * overflowedLines / totalLines;
	
	var lastIndexOfSpace = node.innerHTML.lastIndexOf(' ', node.innerHTML.length-overflowedChars);

	var crop = node.innerHTML.slice(lastIndexOfSpace);
	var rest = node.innerHTML.slice(0, lastIndexOfSpace);

	node.innerHTML = rest;
	SSR.contents.contents_buffer = crop;
}


/**
 * Add new page with buffered contents
 * @param nodeName {String}
 */
SSR.contents.creaetNodeFromTransferedContent = function(nodeName){
	var node = document.createElement(nodeName.toLowerCase());

	node.innerHTML = SSR.contents.contents_buffer;
	SSR.contents.contents_buffer = '';
	node.setAttribute('class', 'continuation');
	
	return node;
}

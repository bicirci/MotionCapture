jQuery(document).ready(function($){
	// adapt the header when scrolled
	$('.header-fragments .header-top-content').evolutionAdapativeHeader({
		fix: '.layout-region.header',
		activeClass: 'scrolled',
		minWidth: 768
	});

	// reflow content to single column when narrow
	$('.content-fragment-page').evolutionReflow({
		minWidth: 768
	});

	// dock the sidebar when possible
	//$('.content-fragment-page')
	//	.find('.layout-content.content-left-sidebar-right, .layout-content.sidebar-left-content-center-sidebar-right, .layout-content.sidebar-left-content-right, .layout-content.header-top-content-left-sidebar-right, .layout-content.header-top-sidebar-left-content-center-sidebar-right, .layout-content.header-top-sidebar-left-content-right, .layout-content.header-top-content-left-sidebar-right-footer, .layout-content.header-top-sidebar-left-content-center-sidebar-right-footer, .layout-content.header-top-sidebar-left-content-right-footer')
	//	.find('.layout-region-inner.right-sidebar, .layout-region-inner.left-sidebar')
	//	.evolutionDock({ });
	$(document).on('customizepage', function(){
		$('body').addClass('edit');
	});

	// override modals
	$.extend($.glowModal.defaults, {
		isDraggable: false,
		isResizable: false,
		loadingHtmlUrl: null,
		windowCssClasses: ['modal-wrapper','modal'],
		windowTitleCssClasses: ['modal-title'],
		windowCloseCssClasses: ['modal-close-wrapper', 'modal-close'],
		windowContentCssClasses: ['modal-content'],
		windowMaskCssClasses: ['modal-mask'],
		windowFooterCssClasses: ['modal-footer'],
		windowResizeCssClasses: [],
		windowWrapperCssClasses: ['modal-wrapper-wrapper'],
		height: 100
	});

	// raise available height messages
	var availableHeight = 0,
		win = $(window),
		headerElements = $('.header-fragments .layout-content.header-top-content, .header-fragments .layout-region.header');

	function throttle(fn, limit) {
		var lastRanAt, timeout;
		return function() {
			var scope = this
				attemptAt = (new Date().getTime()),
				args = arguments;
			if(lastRanAt && (lastRanAt + (limit || 50)) > attemptAt) {
				clearTimeout(timeout);
				timeout = setTimeout(function(){
					lastRanAt = attemptAt;
					fn.apply(scope, args);
				}, (limit || 50));
			} else {
				lastRanAt = attemptAt;
				fn.apply(scope, args);
			}
		};
	}

	function getHeaderOffset() {
		var headerOffset = 0;
		headerElements.each(function() {
			var header = $(this);
			if (header.is(':visible') && header.css('position') == 'fixed') {
				var offset = parseInt(header.css('top'), 10);
				if (isNaN(offset)) {
					offset = 0;
				}
				offset += header.outerHeight();
				if (offset > headerOffset) {
					headerOffset = offset;
				}
			}
		});
		return headerOffset;
	}

	win.on('scroll resize', throttle(function() {
		var scrollHeight = win.height();
		var headerOffsetTop = getHeaderOffset();
		var measuredHeight = scrollHeight - headerOffsetTop;

		if (availableHeight != measuredHeight) {
			$.telligent.evolution.messaging.publish('window.scrollableheight', { height: measuredHeight });
			availableHeight = measuredHeight;
		}
	}, 100));
});


(function($, global, undef) {

	var throttle = function(fn, limit) {
		var lastRanAt, timeout;
		return function() {
			var scope = this
				attemptAt = (new Date().getTime()),
				args = arguments;
			if(lastRanAt && (lastRanAt + (limit || 50)) > attemptAt) {
				global.clearTimeout(timeout);
				timeout = global.setTimeout(function(){
					lastRanAt = attemptAt;
					fn.apply(scope, args);
				}, (limit || 50));
			} else {
				lastRanAt = attemptAt;
				fn.apply(scope, args);
			}
		};
	};

	function process(context) {
		var width = context.selection.width(),
			scrollTop = $(global).scrollTop();

		// if too narrow, don't process, just possibly disable
		if(width < context.minWidth) {
			// disable if was enabled and screen now too narrow to support this behavior
			if(context.enabled) {
				context.enabled = false;
				unfix(context);

				if(context.adapted) {
					unadapt(context);
				}
			}
			// and do no more...
			return;
		}
		
		var difference = $(document).height() - context.staticHeight - $(window).height();
		var documentIsLongEnoughToAdapt = difference > (context.staticHeight - context.minimizedHeight);

		if(!context.adapted &&
			scrollTop > (context.staticHeight - context.minimizedHeight))
		{
			// apply scrolled adaptation
			adapt(context);
			if(!documentIsLongEnoughToAdapt) {
				window.scrollTo(0, (context.staticHeight - context.minimizedHeight));
			}
		} else if(context.adapted &&
			scrollTop <= (context.staticHeight - context.minimizedHeight))
		{
			unadapt(context);
		}

		// enable if not enabled at all
		if(!context.enabled) {
			context.enabled = true;
			if(scrollTop == 0)
				fix(context);
		}
	}

	function unfix(context) {
		context.body.css({
			paddingTop: '-=' + context.fixedElementsHeight
		});
		context.fixedElements.css({
			position: 'static'
		});
	}

	function fix(context) {
		context.body.css({
			paddingTop: ('+=' + context.fixedElementsHeight)
		});
		context.fixedElements.css({
			position: 'fixed',
			top: 0,
			'z-index': 10
		});
	}

	function adapt(context) {
		context.adapted = true;

		unfix(context);

		context.selection.css({
			position: 'fixed',
			top: 0,
			'z-index': 10
		}).addClass(context.activeClass);
		context.body.css({
			paddingTop: ('+=' + context.staticHeight)
		});
	}

	function unadapt(context){
		context.adapted = false;

		fix(context);

		context.selection.css({
			position: 'static'
		}).removeClass(context.activeClass);
		context.body.css({
			paddingTop: ('-=' + context.staticHeight)
		});
	}

	function handleEvents(context) {
		$(global).on('resize.adaptiveHeader scroll.adaptiveHeader', throttle(function(){
			process(context);
		}, context.resizeTimeout));
		// when entering page edit mode, turn everything back off
		$(document).on('customizepage', function(){
			unadapt(context);
			unfix(context);
			context.body.css({ 'padding-top': 0 });
			$(global).off('.adaptiveHeader');
		});
	}

	// determines minimized/scrolled height breakpoint by testing
	// the height when the scrolled class is applied
	function measureMinimizedHeight(context) {
		context.selection
			.css({ visibility: 'hidden' })
			.addClass(context.activeClass);

		var height = context.selection.height();

		context.selection
			.removeClass(context.activeClass)
			.css({ visibility: 'visible' });

		return height;
	}

	$.fn.evolutionAdapativeHeader = function(options) {
		var context = $.extend({}, $.fn.evolutionAdapativeHeader.defaults, options || {});
		context.selection = this;
		context.body = $('body');

		// capture elements
		context.fixedElements = $(context.fix, this);
		context.fixedElementsHeight = context.fixedElements.outerHeight();
		context.staticHeight = context.selection.height();

		if(!context.minimizedHeight) {
			context.minimizedHeight = measureMinimizedHeight(context);
		}
		if(context.staticHeight - context.fixedElementsHeight > 0) {
			context.selection.addClass('with-adaptable-elements');
		}

		handleEvents(context);
		process(context);

		return context.selection;
	}

	$.fn.evolutionAdapativeHeader.defaults = {
		fix: '.layout-region.header',
		// pre-defined breakpoint (when not provided, determines one by measuring height when activeClass is applied)
		minimizedHeight: null,
		//don't activate or remove behavior when screen less than
		minWidth: 768,
		activeClass: 'scrolled',
		resizeTimeout: 50
	};

})(jQuery, window);


(function($, global, undef) {

	$.fn.evolutionDock = function (options) {
		var settings = $.extend({}, $.fn.evolutionDock.defaults, options || {}),
			fixedSupported = true,
			availableHeight = $(window).height();

		(function() {
			var test = $('<div></div>').css({'position': 'fixed', 'top': '100px'});
			$('body').append(test);
			fixedSupported = test.offset().top == 100 + $(global).scrollTop();

			global.setTimeout(function() {
				fixedSupported = test.offset().top == 100 + $(global).scrollTop();
				test.remove();
			}, 199);
		})();

		return this.each(function () {
			var dockWrapper = $(this),
				jGlobal = $(global),
				top = dockWrapper.offset().top,
				defaults = {
					top: dockWrapper.css('top'),
					position: dockWrapper.css('position'),
					width: dockWrapper.css('width')
				},
				docked = false,
				placeholder = $('<div></div>').attr({'class': dockWrapper.attr('class'), 'visibility': 'hidden'}).hide(),
				footers = $(settings.footers);

			dockWrapper.parent().css('position', 'relative').append(placeholder);

			var reposition = function() {
				var parentOffset = dockWrapper.parent().offset();
				var scrollTop = jGlobal.scrollTop();
				var headerOffsetTop = $(window).height() - availableHeight;

				var shouldBeFixed = fixedSupported
					&& scrollTop > parentOffset.top - headerOffsetTop // we're scrolled
					&& dockWrapper.outerHeight() <= availableHeight // content is shorter than the viewport

				if (shouldBeFixed) {
					if (!docked) {
						placeholder.show().css('height', dockWrapper.innerHeight() + 'px');
					}

					var footerOffsetTop = getFooterTop();
					var top, position, dockOuterHeight = dockWrapper.outerHeight();
					if (footerOffsetTop == -1 || headerOffsetTop + dockOuterHeight + scrollTop < footerOffsetTop) {
						top = headerOffsetTop;
						position = 'fixed';
					} else {
						top = footerOffsetTop - parentOffset.top - dockOuterHeight;
						position = 'absolute';
					}
					docked = true;
					dockWrapper.css({ position: position, top: top + 'px', width: placeholder.width() + 'px' });
				} else if (!shouldBeFixed && docked) {
					placeholder.hide().css('height', '0px');
					docked = false;
					dockWrapper.css({ position: defaults.position, top: defaults.top, width: defaults.width });
				}
			},
			getFooterTop = function() {
				var footerTop = -1;
				footers.each(function() {
					var footer = $(this);
					if (footer.is(':visible')) {
						var offset = footer.offset();
						if (footerTop == -1 || offset.top < footerTop) {
							footerTop = offset.top;
						}
					}
				});
				return footerTop;
			}

			jGlobal
				.on('scroll resized', function () {
					reposition();
				});

			$.telligent.evolution.messaging.subscribe('window.scrollableheight', function(data) {
				availableHeight = data.height;
				reposition();
			});

			reposition();
		});
	};
	$.extend($.fn.evolutionDock, {
		defaults: {
			footers: ('.footer-fragments-header, ' +
				'.footer-fragments, ' +
				'.footer-fragments-footer, ' +
				'.content-fragment-page ' +
				'.layout-region.footer')
		}
	});

})(jQuery, window);


(function($, global, undef) {

	var _init = function (options) {
		return this.each(function () {
			var settings = $.extend({}, $.fn.evolutionReflow.defaults, options || {});
			var state = $(this);
			var checkReflowHandle = null;
			var isSingleColumn = false;
			var reflowContainer = $('<div></div>').addClass(settings.cssClass).css('display','none').insertBefore(state).end();
			var children = null;
			var isReflowing = false;

			var checkReflow = function() {
				if (isSingleColumn && reflowContainer.width() >= settings.minWidth) {
					restore();
				} else if (!isSingleColumn && state.width() < settings.minWidth) {
					reflow();
				}
			},
			reflow = function() {
				isReflowing = true;
				children = [];
				var originalOrder = 0;

				state.find(settings.children).each(function() {
						var c = $(this);
						children.push({
								element: c,
								parent: c.parent(),
								parentOrder: getParentOrder(c),
								responsiveOrder: getResponsiveOrder(c),
								originalOrder: originalOrder++
						});
				});

				children.sort(function(a, b) { return (a.responsiveOrder == b.responsiveOrder) ? a.parentOrder - b.parentOrder : a.responsiveOrder - b.responsiveOrder; });
				$.each(children, function() { reflowContainer.append(this.element); });

				reflowContainer.show();
				state.hide();

				isSingleColumn = true;
				isReflowing = false;
			},
			restore = function() {
				isReflowing = true;

				children.sort(function(a, b) { return a.originalOrder - b.originalOrder; });
				$.each(children, function() { this.parent.append(this.element); });

				state.show();
				reflowContainer.hide();

				isSingleColumn = false;
				isReflowing = false;
			},
			getResponsiveOrder = function(e) {
				var classes = e.attr('class').split(' ');
				for (var i = 0; i < classes.length; i++) {
					if (classes[i].indexOf('responsive-') == 0) {
						var o = parseInt(classes[i].substr(11), 10);
						if (!isNaN(o)) {
							return o;
						}
					}
				}
				return 10000;
			},
			getParentOrder = function(e) {
				if (settings.parents && settings.parents.length > 0) {
					var p = e.parent();
					for (var i = 0; i < settings.parents.length; i++) {
						if (p.hasClass(settings.parents[i])) {
							return i;
						}
					}
				}
				return 10000;
			}

			$(global).on('resized', checkReflow);

			checkReflow();
		});
	};

	$.fn.evolutionReflow = function (method) {
		if (typeof method === 'object' || !method)
			return _init.apply(this, arguments);
		else
			$.error('Method ' + method + ' does not exist on jQuery.fn.evolutionReflow');
	};

	$.extend($.fn.evolutionReflow, {
		defaults: {
			cssClass: 'single-column',
			minWidth: 600,
			children: '.content-fragment',
			parents: ['header', 'content', 'left-sidebar', 'split-sidebar-left', 'split-sidebar-right', 'right-sidebar', 'footer']
		}
	});

})(jQuery, window);



// override pager UI component
(function($, global, undef){

	function showLoadingIndicator(container, mask) {
		var containerOffset = container.offset();
		mask.hide().appendTo('body').css({
			width: container.width(),
			height: container.height(),
			top: containerOffset.top,
			left: containerOffset.left
		}).show();
	}

	function hideLoadingIndicator(container, mask) {
		mask.hide();
	}

	function buildMask() {
		return $('<div></div>').css({
			backgroundColor: '#fff',
			position: 'absolute',
			opacity: .75,
			zIndex: 1
		});
	}

	var ajaxPagerContexts = {};
	$.telligent.evolution.ui.components.page = {
		setup: function() {

		},
		add: function(elm, options) {
			// general settings
			var settings = {
				currentPage: parseInt(options.currentpage, 10),
				pageSize: parseInt(options.pagesize, 10),
				totalItems: parseInt(options.totalitems, 10),
				showPrevious: typeof options.configuration.ShowPrevious === 'undefined' ? true : options.configuration.ShowPrevious === 'true',
				showNext: typeof options.configuration.ShowNext === 'undefined' ? true : options.configuration.ShowNext === 'true',
				showFirst: true,
				showLast: true,
				showIndividualPages: typeof options.configuration.ShowIndividualPages === 'undefined' ? false : options.configuration.ShowIndividualPages === 'true',
				numberOfPagesToDisplay: 0,
				pageKey: options.pagekey,
				hash: options.configuration.Target,
				baseUrl: options.configuration.BaseUrl || window.location.href,
				template: typeof options.configuration.Template !== 'undefined' ? options.configuration.Template : '' +
					' <% if(links && links.length > 0) { %> ' +
					'   <% if($.grep(links, function(l){ return l.type === "previous"; }).length > 0) { %> ' +
					' 	  <a class="previous" data-type="previous" data-page="<%= $.grep(links, function(l){ return l.type === "previous"; })[0].page %>" href="<%: $.grep(links, function(l){ return l.type === "previous"; })[0].url %>">&lt;</a> ' +
					'   <% } else { %> ' +
					' 	  <a class="previous disabled" href="#">&lt;</a> ' +
					'   <% } %> ' +
					'   <div class="ends"> ' +
					' 	  <div> ' +
					'   	<% if($.grep(links, function(l){ return l.type === "first"; }).length > 0) { %> ' +
					'   	  	<a class="first" data-type="first" data-page="<%= $.grep(links, function(l){ return l.type === "first"; })[0].page %>" href="<%: $.grep(links, function(l){ return l.type === "first"; })[0].url %>">&lt;</a> ' +
					'   	<% } %> ' +
					'   	<% if($.grep(links, function(l){ return l.type === "last"; }).length > 0) { %> ' +
					'   		<a class="last" data-type="last" data-page="<%= $.grep(links, function(l){ return l.type === "last"; })[0].page %>" href="<%: $.grep(links, function(l){ return l.type === "last"; })[0].url %>">&gt;</a> ' +
					'   	<% } %> ' +
					'     </div> ' +
					'   </div> ' +
					'   <% if($.grep(links, function(l){ return l.type === "next"; }).length > 0) { %> ' +
					'   	<a class="next" data-type="next" data-page="<%= $.grep(links, function(l){ return l.type === "next"; })[0].page %>" href="<%: $.grep(links, function(l){ return l.type === "next"; })[0].url %>">&gt;</a> ' +
					'   <% } else { %> ' +
					'   	<a class="next disabled" href="#">&lt;</a> ' +
					'   <% } %> ' +
					' <% } %> '

			};
			// ajax-specific options
			if(options.pagedcontenturl) {
				ajaxPagerContexts[options.pagedcontentpagingevent] = {
					onPage: function(pageIndex, complete, hash) {
						var contentContainer = $('#' + options.pagedcontentwrapperid),
							body = $('html,body');

						var data = hash || {};
						data[options.pagekey] = pageIndex;
						// modify the url instead of passing as data, as the url might have this in the querystring already
						var url = $.telligent.evolution.url.modify({ url: options.pagedcontenturl, query: data });
						$.telligent.evolution.get({
							url: url,
							cache: false,
							success: function(response) {
								complete(response);
								// scroll to top of paging area after page if out of view
								var top = contentContainer.offset().top - 160;
								var scrollTop = 0;
								body.each(function(i, e) {
									if (e.scrollTop && e.scrollTop > scrollTop) {
										scrollTop = e.scrollTop;
									}
								});
								if(scrollTop > top) {
									body.animate({
										scrollTop: top
									}, 250);
								}
							}
						});
					}
				};
				$.extend(settings, {
					onPage: function(pageIndex, complete, hash) {
						ajaxPagerContexts[options.pagedcontentpagingevent].onPage(pageIndex, complete, hash);
					},
					refreshOnAnyHashChange: (options.loadonanyhashchange === 'true'),
					pagedContentContainer: '#' + options.pagedcontentwrapperid,
					pagedContentPagingEvent: options.pagedcontentpagingevent,
					pagedContentPagedEvent: options.pagedcontentpagedevent,
					transition: options.configuration.Transition,
					transitionDuration: typeof options.configuration.TransitionDuration === 'undefined' ? 200 : parseInt(options.configuration.TransitionDuration, 10)
				});
			}
			$(elm).evolutionPager(settings);

			if(options.loadingindicator === 'true') {
				var container = $('#' + options.pagedcontentwrapperid), mask = buildMask();
				$.telligent.evolution.messaging.subscribe(options.pagedcontentpagingevent, function(){
					showLoadingIndicator(container, mask);
				});
				$.telligent.evolution.messaging.subscribe(options.pagedcontentpagedevent, function(){
					hideLoadingIndicator(container, mask);
				});
			}
		}
	};

})(jQuery, window);


// moderation UI component override
(function($, global, undef){

	function addAbuseReport(contentId, contentTypeId) {
		return $.telligent.evolution.post({
			url: $.telligent.evolution.site.getBaseUrl() + 'api.ashx/v2/abusereports.json',
			data: {
				ContentId: contentId,
				ContentTypeId: contentTypeId
			},
			cache: false,
			dataType: 'json'
		});
	}

	function show(elm) {
		return elm.css({ display: 'block'});
	}

	function hide(elm) {
		return elm.css({ display: 'none'});
	}

	$.telligent.evolution.ui.components.moderate = {
		setup: function() { },
		add: function (elm, options) {
			if (options.supportsabuse === 'false') {
				elm.remove();
				return;
			}
			elm.empty();
			var flagLink = hide($('<a href="#">' + $.telligent.evolution.ui.components.moderate.defaults.flagText + '</a>').appendTo(elm));
			var	changing = hide($('<a href="#">…</a>').appendTo(elm));
			var	flaggedState = hide($('<a href="#">' + $.telligent.evolution.ui.components.moderate.defaults.flaggedText + '</a>').appendTo(elm));

			// if already flagged, show that instead of the link
			if(options.initialstate == 'true') {
				show(flaggedState).on('click', function(e){ return false; });
			} else {
				show(flagLink).on('click', function(e){
					e.preventDefault();
					e.stopPropagation();
					// when tapped, show the 'changing' state
					show(changing);
					hide(flagLink);
					// and submit the abuse report
					addAbuseReport(options.contentid, options.contenttypeid).then(function(){
						// switch to the 'flagged' link state
						show(flaggedState);
						hide(changing);
						// raise ui.reportabuse message
						$.telligent.evolution.messaging.publish('ui.reportabuse', {
							contentId: options.contentid,
							contentTypeId: options.contenttypeid
						});
						// show a message
						$.telligent.evolution.notifications.show($.telligent.evolution.ui.components.moderate.defaults.reportedText, {
							duration: $.telligent.evolution.ui.components.moderate.defaults.duration
						});
					});
				});
			}
		}
	};
	$.telligent.evolution.ui.components.moderate.defaults = {
		reportedText: 'Thank you for your report',
		flagText: 'Flag as spam/abuse',
		flaggedText: 'Flagged as spam/abuse',
		duration: 5 * 1000
	};

})(jQuery, window);


// resize overload
(function($, global, undef){

	var resize = function(context) {
			context.area.css({ height: 'auto' });

			var newHeight = context.area.prop('scrollHeight');
			if(newHeight < context.minHeight)
				newHeight = context.minHeight;

			context.area.css({ height: newHeight });

			newHeight = (context.area.outerHeight(true));

			if(newHeight !== context.oldHeight) {
				context.area.css({ overflow: 'hidden' });
				context.area.trigger('evolutionResize', { newHeight: newHeight, oldHeight: context.oldHeight });
				context.oldHeight = newHeight;
			}
		};

	$.fn.evolutionResize = function(options) {
		var settings = $.extend({}, $.fn.evolutionResize.defaults, options || {});
		return this.filter('textarea').each(function(){
			var area = $(this)
					.css({ width: '100%', resize: 'none', overflow: 'hidden' });
			var context = {
					area: area,
					oldHeight: area.height(),
					minHeight: area.outerHeight()
				};
			area.on('input', function(){ resize(context); });
			resize(context);
		});
	};
	$.fn.evolutionResize.defaults = {
		maxLength: 250
	};

})(jQuery, window);

// evolutionHighlight
(function($, global, undef){

	var highlighterKey = '_HIGHLIGHTER_CONTEXT',
		getContext = function(selection, options) {
			var context = selection.data(highlighterKey);
			if(typeof context === 'undefined' || context === null) {
				context = buildContext(selection, options);
				selection.data(highlighterKey, context);
			}
			return context;
		},
		buildContext = function(selection, options) {
			var area = selection.filter('textarea');
			var context = {
				selection: area,
				settings: $.extend({}, $.fn.evolutionHighlight.defaults, options || {}),
				verticalPadding: parseInt(area.css('padding-top') || '0', 10) + parseInt(area.css('padding-bottom') || '0', 10),
				horizontalPadding: parseInt(area.css('padding-left') || '0', 10) + parseInt(area.css('padding-right') || '0', 10) + parseInt(area.css('border-left') || '0', 10) + parseInt(area.css('border-right') || '0', 10)
			};
			buildHighlightingContainer(context);
			return context;
		},
		buildHighlightingContainer = function(context) {
			context.wrapper = $('<div></div>');
			context.mirror = $('<div></div>');

			// remove margins from textarea and apply to wrapper
			var wrapperStyle = {
				position: 'relative',
				width: context.selection.outerWidth(true),
				height: context.selection.outerHeight(true) + 2
			};
			$.each(['margin-left','margin-right','margin-top','margin-bottom'], function(i, styleName) {
				wrapperStyle[styleName] = context.selection.css(styleName);
				context.selection.css(styleName, 0);
			});

			// capture textarea styles to apply to mirror
			var mirrorStyle = {
				position: 'absolute',
				top: '0px',
				left: '0px',
				zIndex: '0',
				borderTopColor: 'transparent',
				borderBottomColor: 'transparent',
				borderLeftColor: 'transparent',
				borderRightColor: 'transparent',
				backgroundColor: context.selection.css('backgroundColor'),
				color: 'transparent',
				width: context.selection.outerWidth(),
				height: context.selection.outerHeight(),
				overflow: 'hidden',
				whiteSpace: 'normal'
			};
			$.each(context.settings.styles, function(i,styleName){
				mirrorStyle[styleName] = context.selection.css(styleName);
			});

			// new styles to apply to text area
			var textAreaStyle = {
				position: 'absolute',
				top: '0px',
				left: '0px',
				zIndex: '1',
				backgroundColor: 'transparent',
				width: context.selection.outerWidth(),
				height: context.selection.outerHeight()
			};

			// apply styles
			context.wrapper.css(wrapperStyle).addClass('highlighter');
			context.mirror.css(mirrorStyle);
			context.selection.css(textAreaStyle);

			// set background-color
			context.mirror.css('color', context.mirror.css('background-color'));

			// rearrange DOM
			context.selection.before(context.wrapper);
			context.wrapper.append(context.selection);
			context.wrapper.append(context.mirror);

			context.mirror.css({
				width: context.selection.outerWidth(true) + context.horizontalPadding,
				height: context.selection.outerHeight(true) + context.verticalPadding
			})
		},
		rDoubleSpace = /\s\s/gi,
		rBreak = /\n/gi,
		encodeSymbols = {
				'&' :'&amp;',
				'>': '&gt;',
				'<': '&lt;',
				'"': '&quot;',
				"'": '&#39;'
		},
		highlight = function(context) {
			// prepare highlights
			var ranges = {};
			$.each(context.settings.ranges, function(i, range) {
				ranges[range.start] = ranges[range.start] || [];
				ranges[range.start].push(range);
				ranges[range.stop] = ranges[range.stop] || [];
				ranges[range.stop].push(range);
			});

			var rawValue = $.telligent.evolution.html.encode(context.selection.val());
				newValue = [],
				spanDepth = 0;
			for(var i = 0; i < rawValue.length; i++) {
				if(typeof ranges[i] !== 'undefined') {
					$.each(ranges[i], function(h, range) {
						if(range.start === i) {
							newValue[newValue.length] = '<span class="'+range.className+'" style="white-space:normal;">';
							spanDepth++;
						} else {
							newValue[newValue.length] = '</span>';
							spanDepth--;
						}
					});
				}
				newValue[newValue.length] = encodeSymbols[rawValue.charAt(i)] ? encodeSymbols[rawValue.charAt(i)] : rawValue.charAt(i);
			}
			if(spanDepth > 0) {
				newValue[newValue.length] = '</span>';
			}
			var newRawValue = newValue.join('').replace(rBreak,'<br />').replace(rDoubleSpace,'&nbsp; ');
			// not using .html() as it executes js.  Not using .innerHTML directly on mirror as it errors in IE
			var mirroredValueWrapper = document.createElement('span');
			mirroredValueWrapper.innerHTML = newRawValue;
			context.mirror.empty().get(0).appendChild(mirroredValueWrapper);
		};
		var methods = {
			init: function(options) {
				var context = getContext(this, options);
				context.settings = $.extend({}, $.fn.evolutionHighlight.defaults, options || {});
				highlight(context);
				return this;
			},
			clear: function() {
				var context = getContext(this, null);
				if(context === null)
					return;
				context.mirror.html('');
				return this;
			},
			resize: function(width, height) {
				var context = getContext(this, null);
				if(context === null)
					return;
				var newStyle = {
					width: width + context.horizontalPadding,
					height: height + context.verticalPadding
				};
				context.mirror.css(newStyle);
				context.selection.css(newStyle);
				context.wrapper.css({
					width: context.selection.width() + context.horizontalPadding,
					height: context.selection.height() + context.verticalPadding + 4
				});
				return this;
			},
			css: function(css) {
				var context = getContext(this, null);
				if(context === null)
					return;
				context.wrapper.css(css);
				return this;
			}
		};
	$.fn.evolutionHighlight = function(method) {
		if (methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' +  method + ' does not exist on jQuery.evolutionHighlight');
		}
	};
	$.fn.evolutionHighlight.defaults = {
		ranges: [],
		styles: ['border-top-width','border-top-style','border-bottom-width',
			'border-bottom-style','border-right-width','border-right-width-value',
			'border-right-style','border-right-style-value','border-left-width',
			'border-left-width-value','border-left-style','border-left-style-value',
			'font-family','font-size','font-size-adjust','font-stretch',
			'font-style','font-variant','font-weight',
			'padding-bottom','padding-left','padding-right','padding-top',
			'letter-spacing','line-height','text-align','text-indent','word-spacing']
	};

})(jQuery, window);

// override search result UI component
(function($){
	$.telligent.evolution.ui.components.searchresult = {
		setup: function() { },
		add: function(elm) { }
	};
})(jQuery);


// override for liker template
(function($){

	$.fn.evolutionLike.defaults.likersTemplate = '' +
		' <% foreach(likers, function(liker) { %> ' +
		'     <li class="content-item"> ' +
		'         <div class="full-post-header"></div> ' +
		'         <div class="full-post"> ' +
		'             <span class="avatar"> ' +
		'                 <a href="<%: liker.profileUrl %>"  class="internal-link view-user-profile"> ' +
		'                     <% if(liker.avatarHtml) { %> ' +
		'                         <%= liker.avatarHtml %> ' +
		'                     <% } else { %> ' +
		'                         <img src="<%: liker.avatarUrl %>" alt="" border="0" width="32" height="32" style="width:32px;height:32px" /> ' +
		'                     <% } %> ' +
		'                 </a> ' +
		'             </span> ' +
		'             <span class="user-name"> ' +
		'                 <a href="<%: liker.profileUrl %>" class="internal-link view-user-profile"><%= liker.displayName %></a> ' +
		'             </span> ' +
		'         </div> ' +
		'         <div class="full-post-footer"></div> ' +
		'     </li> ' +
		' <% }); %> ';

})(jQuery);

// override defaults
(function($){
	$.fn.glowUpload.defaults.width = '80%';
	$.fn.evolutionStarRating.defaults.starElement = 'span'
})(jQuery);


// adjust tables to be scrollable if they are larger than the content width and available height
(function($) {
	var maxHeight = 400,
		checkResize = function() {
			$('.content-fragment-content .content .content .content-scrollable-wrapper').each(function() {
				var w = $(this);
				var sw = w.prop('scrollWidth') || w.width();
				if (sw > w.outerWidth()) {
					w.addClass('content-scrollable-wrapper-scrolled').css('max-height', (maxHeight * .8) + 'px');
				} else {
					w.removeClass('content-scrollable-wrapper-scrolled').css('max-height', 'none');
				}
			});
		}

	$.telligent.evolution.messaging.subscribe('window.scrollableheight', function(data) {
		maxHeight = data.height;
		checkResize();
	});

	$(window).on('resized', function() {
		checkResize();
	});

	$(document).ready(function() {
		$('.content-fragment-content .content .content table, .content-fragment-content .content .content pre').each(function() {
			var t = $(this);
			if (t.parents('.content-scrollable-wrapper').length == 0) {
				t.wrap('<div class="content-scrollable-wrapper" style="max-width: 100%; overflow: auto;"></div>');
			}
		});
		checkResize();
	});
})(jQuery);



if (typeof Object.create !== 'function') { Object.create = function (o) { function F() {}; F.prototype = o; return new F(); };}; // for older browsers
Function.prototype.inherits_from = function(super_constructor) { this.prototype = Object.create(super_constructor.prototype); this.prototype.constructor = super_constructor }; // inheritance

var epfl = new Object();


epfl_module = function() {

	epfl.queue = [];
	epfl.event_id = 0;
	epfl.components = {};
	epfl.show_please_wait_counter = 0;
	epfl.overlays = {};
	epfl.overlays_id = 0;

	epfl.init_page = function(opts) {
		$(".epfl_hover_image").bind_hover_border_events();
		$("body").append("<div id='epfl_please_wait'><img src='/epfl/static/img/ajax-loader-big.gif'></div>");
		$("#loader").remove(); // remove the std-mcp2 ajax-loader image

/*		var scroll_pos = $(".epfl_scroll_pos").val(); // Restoring Scroll-Pos
		if (scroll_pos) {
			var tmp = scroll_pos.split("x");
			$(document).scrollLeft(parseInt(tmp[0]));
			$(document).scrollTop(parseInt(tmp[1]));
		};


		$(window).scroll(function() { // Capturing Scroll-Pos
			var scroll_pos = $(document).scrollLeft() + "x" + $(document).scrollTop();
			$(".epfl_scroll_pos").val(scroll_pos)
		});
*/

		epfl.new_tid(opts["tid"], true);
		epfl.ptid = opts["ptid"];
		$(document).attr("data:tid", epfl.tid);

	};

	epfl.init_component = function(cid, class_name, params) {
		var constructor = epfl[class_name];
		if (!constructor) {
			alert("JS-ERROR: The component '" + class_name + "' does not exist!")
			return;
		}
		var compo_obj = new constructor(cid, params);
		epfl.components[cid] = compo_obj;
	};

	epfl.replace_component = function(cid, parts) {
		for (var part_name in parts) {
			if (part_name == "js") continue;
			var part_html = parts[part_name];
	  		if (part_name == "main") {
	  			var epflid = cid;
	  		} else {
	  			var epflid = cid + "$" + part_name;
	  		};
	  		var el = $("[epflid='" + epflid + "']");
	  		if (el.length == 0) {
	  			alert("Element with epflid='" + epflid + "' not found!");
	  			return;
	  		};
	  		el.replaceWith(part_html);
		};
		eval(parts["js"]);
	};

	epfl.hide_component = function(cid) {
	  	$("[epflid='" + cid + "']").replaceWith("<div epflid='" + cid + "'></div>");
	};

	epfl.destroy_component = function(cid) {
		if (epfl.components[cid]) {
			epfl.components[cid].destroy();
			delete epfl.components[cid];
		};
	};

	epfl.unload_page = function() {
		epfl.flush(null, true);
	};

	epfl.flush = function(callback_func, sync) {


		if (epfl.queue.length == 0) {
			// queue empty
			if (callback_func) {
				callback_func(null);
			};
		} else {
			// send and clear queue
			var ajax_target_url = location.href;

			if (epfl.show_please_wait_counter > 0) {
				sync = true;
			}

			epfl.show_please_wait(true);
			var queue = epfl.queue;
			epfl.queue = [];
			$.ajax({url: ajax_target_url,
					global: false,
					async: !sync,
				    type: "POST",
				    cache: false,
				    data: JSON.stringify({"tid": epfl.tid, "q": queue}),
				    contentType: "application/json",
				    dataType: "script",
	                success: function(data) {
	                    if (callback_func) {
                            try {
                                callback_func($.parseJSON(data))
                            } catch(e) {
                                console.log('Caught Exception when trying to parse data as JSON. Did you provide a ' +
                                    'callback for an event without a json response?');
                                console.log(e);
                            }
	                    };
	                    epfl.hide_please_wait(true);
	                },
	                error: function(httpRequest, message, errorThrown) {
	                    epfl.hide_please_wait(true);
	                    epfl.show_fading_message("txt_system_error: " + errorThrown, "error");
	                    console.log(httpRequest)
	                	//throw errorThrown;
	                }
			});
		};
	};

	epfl.send = function(epflevent, callback_func) {
		epfl.enqueue(epflevent);
		epfl.flush(callback_func);
	};

	epfl.enqueue = function(epflevent) {
		epfl.queue.push(epflevent);
	};

	epfl.repeat_enqueue = function(epflevent, equiv) {
		for (var i = 0; i < epfl.queue.length; i++) {
			if (epfl.queue[i]["eq"] == equiv) {
				epfl.queue.splice(i, 1);
				break;
			};
		};
		epflevent["eq"] = equiv;
		epfl.enqueue(epflevent);
	};

	epfl.dequeue = function(equiv) {
		var new_queue = [];
		for (var i = 0; i < epfl.queue.length; i++) {
			if (epfl.queue[i]["eq"] != equiv) {
				new_queue.push(epfl.queue[i]);
			};
		};
		epfl.queue = new_queue;
	};


	epfl.make_component_event = function(component_id, event_name, params) {

		if (!params) params = {};

		return {"id": epfl.make_event_id(),
		        "t": "ce",
		        "cid": component_id,
		        "e": event_name,
		        "p": params};
	};

	epfl.make_page_event = function(event_name, params) {

		if (!params) params = {};

		return {"id": epfl.make_event_id(),
		        "t": "pe",
		        "e": event_name,
		        "p": params};
	};

	epfl.make_event_id = function() {
		epfl.event_id += 1;
		return epfl.event_id;
	};

	epfl.json_request = function(event, callback_func) {
		epfl.flush(function() {
			var ajax_target_url = location.href;
			$.ajax({url: ajax_target_url,
					global: false,
				    type: "POST",
				    cache: false,
				    data: JSON.stringify({"tid": epfl.tid, "q": [event]}),
				    contentType: "application/json",
				    dataType: "json",
	                success: function(data) { callback_func(data) },
	                error: function(httpRequest, message, errorThrown) {
	                    epfl.show_fading_message("txt_system_error: " + errorThrown, "error");
	                }
				   });
		});
	};


	epfl.show_please_wait = function(is_ajax) { // Should be called as onsubmit
		if (is_ajax) {
			epfl.show_please_wait_counter += 1;
		} else {
			epfl.show_please_wait_counter = 1;
		}
		if (epfl.show_please_wait_counter == 1) {
			$('#epfl_please_wait').fadeIn();
		} else {
			$('#epfl_please_wait').stop(true);
			$('#epfl_please_wait').show();
		}
		$('#epfl_please_wait').center();
	};

	epfl.hide_please_wait = function(is_ajax) { // Should be called as onsubmit
		if (is_ajax) {
			epfl.show_please_wait_counter -= 1;
		} else {
			epfl.show_please_wait_counter = 0;
		}
		if (epfl.show_please_wait_counter == 0) {
			$('#epfl_please_wait').stop(true);
			$('#epfl_please_wait').fadeOut();
		};
	};

	epfl.show_fading_message = function(msg, typ) {
		$("body").append("<div id='epfl_message'></div>");
		if (typ == "info") {
			$("#epfl_message").css("background", "#ffff80");
		} else if (typ == "ok") {
			$("#epfl_message").css("background", "#80ff80");
		} else if (typ == "error") {
			$("#epfl_message").css("background", "#ff8080");
		};
		$("#epfl_message").html(msg);
		$("#epfl_message").center();
		setTimeout(function() {
			$("#epfl_message").fadeOut(500, function() {
					$(this).remove();
			});
		}, 2000);
	};

	epfl.reload_page = function() {
		var frm = $('<form id="__epfl_submit_form__" method="POST" action="#"></form>');
		frm.append('<input type="hidden" name="tid" value="' + epfl.tid + '">');
		$(document.body).append(frm);
		$("#__epfl_submit_form__").submit();
		$("#__epfl_submit_form__").remove();
	};

	epfl.go_next = function(target_url) {
		var frm = $('<form id="__epfl_submit_form__" method="POST" action="' + encodeURI(target_url) + '"></form>');
		frm.append('<input type="hidden" name="tid" value="' + epfl.tid + '"');
		$(document.body).append(frm);
		$("#__epfl_submit_form__").submit();
		$("#__epfl_submit_form__").remove();
	};

	epfl.jump = function(target_url) {
		var frm = $('<form id="__epfl_submit_form__" method="POST" action="' + encodeURI(target_url) + '"></form>');
		$(document.body).append(frm);
		$("#__epfl_submit_form__").submit();
		$("#__epfl_submit_form__").remove();
	};

	epfl.jump_extern = function(target_url, target) {
		var win = window.open(target_url, target);
		win.focus();
	};

	epfl.open_overlay = function(name, url, title, opts, show_please_wait) {
		if (!epfl.overlays[name]) {
			var overlay_id = "epfl_overlay_" + epfl.overlays_id;
			epfl.overlays_id += 1;
			epfl.overlays[name] = overlay_id;
			$(document.body).append("<div id='" + overlay_id + "'></div>");
			$("#" + overlay_id).append("<iframe id='" + overlay_id + "_iframe' src='about:blank' class='epfl-overlay-iframe'></iframe>")
			$("#" + overlay_id).dialog({

				"title": title || "Dialog",
                "resizable": opts["resizeable"],
                "modal": opts["modal"],
                "closeOnEscape": true,
                "draggable": opts["draggable"],
                "height": opts["height"] || "auto",
                "width": opts["width"] || "auto",
                "position": opts["position"] || "center",

                open: function() {
                	$('.ui-widget-overlay').css('position', 'fixed'); // fix a jquery-ui-bug
                },

				close:function (event, ui) {
					// getting the overlays tid
					var ifrm = document.getElementById(overlay_id + "_iframe");
					ifrm = (ifrm.contentWindow) ? ifrm.contentWindow : (ifrm.contentDocument.document) ? ifrm.contentDocument.document : ifrm.contentDocument;
					var overlay_tid = $(ifrm.document).attr("data:tid");

					// telling the server-state to clean up
					var ev = epfl.make_page_event("CloseOverlay", {"overlay_tid": overlay_tid});
					epfl.send(ev);

					// remove the overlay
					epfl.overlays[name] = null;
					$("#" + overlay_id).remove();
					$('.ui-widget-overlay').css('position', 'absolute'); // fix a jquery-ui-bug

				}
			});

			var ifrm = document.getElementById(overlay_id + "_iframe");
			ifrm = (ifrm.contentWindow) ? ifrm.contentWindow : (ifrm.contentDocument.document) ? ifrm.contentDocument.document : ifrm.contentDocument;
			ifrm.document.open();
			ifrm.document.close();
			if (show_please_wait) {
				$("body", ifrm.document).append("<div id='epfl_please_wait'><img src='/epfl/static/img/ajax-loader-big.gif'></div>");
			};
			$("#epfl_please_wait", ifrm.document).css({"position": "absolute",
				                                       "top": "50%",
				                                       "left": "50%",
				                                       "margin-left": "-30px",
		                                               "margin-top": "-30px"})

		} else {
			var overlay_id = epfl.overlays[name];
		}

		setTimeout(function() {
			$("#" + overlay_id + "_iframe").attr("src", url);
		}, 100);
	};

	epfl.close_overlay = function(overlay_name) {
		setTimeout(function() {
			// delayed to allow other events to execute first.
		    window.parent.epfl.__close_overlay_by_name(overlay_name); // go up one window
		}, 0);
	};

	epfl.__close_overlay_by_name = function(overlay_name) {
		var overlay_id = epfl.overlays[overlay_name];
		$("#" + overlay_id).dialog("close"); // close it by JS, let the "close" event do the server side stuff
	};

	epfl.exec_in_page = function(tid, js_src, search_downwards) {
		if (epfl.tid == tid) {
			eval(js_src);
		} else if (search_downwards) {
			for (var i = 0; i < epfl.overlays.length; i++) {
				var overlay_id = epfl.overlays[i];
				var overlay_ifrm = $(overlay_id + "_iframe");
				overlay_ifrm.get(0).epfl.exec_in_page(tid, js_src, true);
			}
		} else {
			window.top.epfl.exec_in_page(tid, js_src, true);
		}
	};

	epfl.handle_dynamic_extra_content= function(content) {
        content.forEach(function (data) {
            $(document.body).append(data)
        });
	};

    epfl.new_tid = function (tid, initial) {
        epfl.tid = tid;
        if (initial) {
            History.replaceState({tid: tid}, tid, window.location.pathname + "?tid=" + tid);
        } else {
            History.pushState({tid: tid}, tid, window.location.pathname + "?tid=" + tid);
        }
    };

    History.Adapter.bind(window,'statechange',function(){
        var state = History.getState();
        if (epfl.tid == state.data.tid) {
            return;
        }
        epfl.tid = state.data.tid;
        epfl.send(epfl.make_page_event('redraw_all'));
    });

};

epfl_module();

$(window).bind("beforeunload", epfl.unload_page);

(function($) {
	$.fn.highlight_hover_border = function() {
		this.removeClass("epfl_hover_image");
		this.addClass("epfl_hover_image_selected");
		this.unbind_hover_border_events();
		this.css("border-color", "blue");
	};
	$.fn.unhighlight_hover_border = function() {
		this.addClass("epfl_hover_image");
		this.removeClass("epfl_hover_image_selected");
		this.bind_hover_border_events();
		this.css("border-color", "transparent");
	};
	$.fn.unbind_hover_border_events = function() {
		this.unbind("mouseenter mouseleave")
	};
	$.fn.bind_hover_border_events = function() {
		this.hover(
				function() {
					$(this).css("border-color", "#8080ff");
				},
				function() {
					$(this).css("border-color", "transparent");
				});
	};
	$.fn.center = function(parent) {
	    if (parent) {
	        parent = this.parent();
	    } else {
	        parent = window;
	    }
	    this.css({
	        "position": "absolute",
	        "top": ((($(parent).height() - this.outerHeight()) / 2) + $(parent).scrollTop() + "px"),
	        "left": ((($(parent).width() - this.outerWidth()) / 2) + $(parent).scrollLeft() + "px")
	    });
	};
})(jQuery);


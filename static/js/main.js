 AOS.init({
 	duration: 800,
 	easing: 'slide',
 	once: false
 });

jQuery(document).ready(function($) {

	"use strict";

	

	var siteMenuClone = function() {

		$('.js-clone-nav').each(function() {
			var $this = $(this);
			$this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
		});


		setTimeout(function() {
			
			var counter = 0;
      $('.site-mobile-menu .has-children').each(function(){
        var $this = $(this);
        
        $this.prepend('<span class="arrow-collapse collapsed">');

        $this.find('.arrow-collapse').attr({
          'data-toggle' : 'collapse',
          'data-target' : '#collapseItem' + counter,
        });

        $this.find('> ul').attr({
          'class' : 'collapse',
          'id' : 'collapseItem' + counter,
        });

        counter++;

      });

    }, 1000);

		$('body').on('click', '.arrow-collapse', function(e) {
      var $this = $(this);
      if ( $this.closest('li').find('.collapse').hasClass('show') ) {
        $this.removeClass('active');
      } else {
        $this.addClass('active');
      }
      e.preventDefault();  
      
    });

		$(window).resize(function() {
			var $this = $(this),
				w = $this.width();

			if ( w > 768 ) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
			}
		})

		$('body').on('click', '.js-menu-toggle', function(e) {
			var $this = $(this);
			e.preventDefault();

			if ( $('body').hasClass('offcanvas-menu') ) {
				$('body').removeClass('offcanvas-menu');
				$this.removeClass('active');
			} else {
				$('body').addClass('offcanvas-menu');
				$this.addClass('active');
			}
		}) 

		// click outisde offcanvas
		$(document).mouseup(function(e) {
	    var container = $(".site-mobile-menu");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {
	      if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
	    }
		});
	}; 
	siteMenuClone();


	var sitePlusMinus = function() {
		$('.js-btn-minus').on('click', function(e){
			e.preventDefault();
			if ( $(this).closest('.input-group').find('.form-control').val() != 0  ) {
				$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) - 1);
			} else {
				$(this).closest('.input-group').find('.form-control').val(parseInt(0));
			}
		});
		$('.js-btn-plus').on('click', function(e){
			e.preventDefault();
			$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) + 1);
		});
	};
	// sitePlusMinus();


	var siteSliderRange = function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 500,
      values: [ 75, 300 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
      " - $" + $( "#slider-range" ).slider( "values", 1 ) );
	};
	// siteSliderRange();


	var siteMagnificPopup = function() {
		$('.image-popup').magnificPopup({
	    type: 'image',
	    closeOnContentClick: true,
	    closeBtnInside: false,
	    fixedContentPos: true,
	    mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
	     gallery: {
	      enabled: true,
	      navigateByImgClick: true,
	      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
	    },
	    image: {
	      verticalFit: true
	    },
	    zoom: {
	      enabled: true,
	      duration: 300 // don't foget to change the duration also in CSS
	    }
	  });

	  $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
	    disableOn: 700,
	    type: 'iframe',
	    mainClass: 'mfp-fade',
	    removalDelay: 160,
	    preloader: false,

	    fixedContentPos: false
	  });
	};
	siteMagnificPopup();


	var siteCarousel = function () {
		if ( $('.nonloop-block-13').length > 0 ) {
			$('.nonloop-block-13').owlCarousel({
		    center: false,
		    items: 1,
		    loop: true,
				stagePadding: 0,
		    margin: 20,
		    nav: false,
		    dots: true,
				navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
		    responsive:{
	        600:{
	        	margin: 20,
	        	stagePadding: 0,
	          items: 1
	        },
	        1000:{
	        	margin: 20,
	        	stagePadding: 0,
	          items: 2
	        },
	        1200:{
	        	margin: 20,
	        	stagePadding: 0,
	          items: 2
	        }
		    }
			});
		}

		if ( $('.slide-one-item').length > 0 ) {
			$('.slide-one-item').owlCarousel({
		    center: false,
		    items: 1,
		    loop: true,
				stagePadding: 0,
		    margin: 0,
		    autoplay: true,
		    pauseOnHover: false,
		    nav: true,
		    animateOut: 'fadeOut',
		    animateIn: 'fadeIn',
		    navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">']
		  });
	  }


	  if ( $('.nonloop-block-4').length > 0 ) {
		  $('.nonloop-block-4').owlCarousel({
		    center: true,
		    items:1,
		    loop:false,
		    margin:10,
		    nav: true,
				navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
		    responsive:{
	        600:{
	          items:1
	        }
		    }
			});
		}

	};
	siteCarousel();

	var siteStellar = function() {
		$(window).stellar({
	    responsive: false,
	    parallaxBackgrounds: true,
	    parallaxElements: true,
	    horizontalScrolling: false,
	    hideDistantElements: false,
	    scrollProperty: 'scroll'
	  });
	};
	siteStellar();

	var siteCountDown = function() {

		if ( $('#date-countdown').length > 0 ) {
			$('#date-countdown').countdown('2020/10/10', function(event) {
			  var $this = $(this).html(event.strftime(''
			    + '<span class="countdown-block"><span class="label">%w</span> weeks </span>'
			    + '<span class="countdown-block"><span class="label">%d</span> days </span>'
			    + '<span class="countdown-block"><span class="label">%H</span> hr </span>'
			    + '<span class="countdown-block"><span class="label">%M</span> min </span>'
			    + '<span class="countdown-block"><span class="label">%S</span> sec</span>'));
			});
		}
				
	};
	siteCountDown();

	var siteDatePicker = function() {

		if ( $('.datepicker').length > 0 ) {
			$('.datepicker').datepicker();
		}

	};
	siteDatePicker();

});

$(function(){
function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }

    $( "#birds" )
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( "search_artist", {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 1 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );

          ids.push(ui.item.id);

          this.value = terms.join( ", " );

          //get_desc(ui.item.value);

          return false;
        }
      });
});

$( function() {
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }

    $(".readonly").on('keydown paste', function(e){
        e.preventDefault();
    });
    $('.login').click(login);
    $('.register').click(register);
    $('.prev').click(prev);
    $('.next').click(next);
    isLoggedIn();
    hot();
    buy();

    $('.free_search').click(function(){
        location.href = '/find?free_id=' + free_id;
    });

    if ($('.concert_manip').length > 0 & getUrlParameter('id') > 0){
        concert_manip();
    }

    $.widget("custom.catcomplete", $.ui.autocomplete, {
         _renderMenu: function (ul, items) {
             var self = this,
    currentCategory = "";
             $.each(items, function (index, item) {
                 if (item.category != currentCategory) {
                     ul.append("<li aria-label=\"" + item.category + "\">" + item.category + "</li>");
                     currentCategory = item.category;
                 }

                 li = self._renderItemData( ul, item );
                  if ( item.category ) {
                    li.attr( "aria-label", item.category + " : " + item.label );
                  }
             });
         }
     });

    $( "#city" )
      // don't navigate away from the field on tab when selecting an item
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .catcomplete({
        source: function( request, response ) {
            var artist = '';
           if ($('#cbx').is(':checked')){
                artist = $('#artist').val();
           }
          $.getJSON( "search", {
            term: extractLast( request.term ),
            artist: artist
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 1 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          this.value = terms;
          return false;
        }
      });

$(".form_datetime").datetimepicker({
        format: "dd MM yyyy - hh:ii"
    });

$( "#free" )
        .val(getUrlParameter('artist'))
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( "free_search", {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 1 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          this.value = terms;

            free_id = ui.item.id;

          return false;
        }
      });

      $( "#location" )
        .val(getUrlParameter('artist'))
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( "search_location", {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 1 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          this.value = terms;

            loc_id = ui.item.id;

          return false;
        }
      });

$('.search').click( search);

  $( "#artist" )
        .val(getUrlParameter('artist'))
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( "search_artist", {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 1 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );



          this.value = terms;





          return false;
        }
      });

    $.views.settings.delimiters("<%", "%>");

     page = parseInt(getUrlParameter('page'));
      if (!Number.isInteger(page)){
        page = -1;

      }

      if ($('.results').length > 0){
        search();
      }
  } );

var page, free_id,loc_id;
var isAdmin = false;
var ids = [];

  function add_concert(){
    $('form').toggleClass('loading').find('fieldset').attr('disabled','');
    name = $('#name').val();
    capacity = $('#capacity').val();
    from = $('#from').val();
    to = $('#to').val();
    $.ajax({
        method: "POST",
        dataType: "json",
        url: "/add_concert",
        data: { name: name,
                capacity: capacity,
                start: from,
                end: to,
                location_id: loc_id,
                artists : ids.join(',')}
    }).done(function( msg ) {
        if (msg == ''){
            $('.alert').removeClass('d-none');
        }
        else{
            $('#exampleModalCenter a').attr('href','/find?concert_id=' + msg.id)
            $('#exampleModalCenter').modal();
            $('fieldset input').val('');
            ids = [];
            loc_id = '';
        }
        $('form').toggleClass('loading').find('fieldset').removeAttr('disabled');
    });

    return false;
  }

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]).replace(/\+/g, ' ');
        }
    }
};

  function prev(e){
    $('form').toggleClass('loading').find('fieldset').attr('disabled','');
    page -= 1;
    $.ajax({
        method: "POST",
        url: "/find2",
        dataType: "json",
        data: { artist: $('#artist').val(),
                page: page}
    }).done(function( msg ) {
        if (msg.length > 10){
            msg.pop();
        }

        var template = $.templates("#theTmpl");
        var htmlOutput = template.render(msg);
        $(".results .result").remove();
        $(".results").append(htmlOutput);
        $('.next').removeClass('d-none');

        if (page == 0){
            $('.prev').addClass('d-none');
        }

        if (isAdmin){
            $('.admin').show().css('visibility', 'visible');
            $('.icon-delete').click(del_concert);
            $('.icon-edit').click(edit_concert);
        }

        $('form').toggleClass('loading').find('fieldset').removeAttr('disabled');
    });

    e.preventDefault();
  }
   function next(e){
    $('form').toggleClass('loading').find('fieldset').attr('disabled','');
    page += 1;
    $.ajax({
        method: "POST",
        url: "/find2",
        dataType: "json",
        data: { artist: $('#artist').val(),
                page: page}
    }).done(function( msg ) {
        if (msg.length > 10){
            msg.pop();
        }
        else {
            $('.next').addClass('d-none');
        }

        var template = $.templates("#theTmpl");
        var htmlOutput = template.render(msg);
        $(".results .result").remove();
        $(".results").append(htmlOutput);
        $('.prev').removeClass('d-none');

        if (isAdmin){
            $('.admin').show().css('visibility', 'visible');
            $('.icon-delete').click(del_concert);
            $('.icon-edit').click(edit_concert);
        }

        $('form').toggleClass('loading').find('fieldset').removeAttr('disabled');
    });



    e.preventDefault();
  }

  function login(){
    $('.alert').addClass('d-none');
    $('form').toggleClass('loading').find('fieldset').attr('disabled','');
    user = $('#username').val()
    password = $('#password').val()
    $.ajax({
        method: "POST",
        url: "/login",
        data: { username: user,
                password: password }
    }).done(function( msg ) {
        if (msg > 0){
            $('.alert').removeClass('d-none');
        }
        else{
            location.href = '/';
        }
        $('form').toggleClass('loading').find('fieldset').removeAttr('disabled');
    });

    return false;
  }

  function register(){
    $('.alert').addClass('d-none');
    $('form').toggleClass('loading').find('fieldset').attr('disabled','');
    user = $('#username').val()
    password = $('#password').val()
    $.ajax({
        method: "POST",
        url: "/register",
        data: { username: user,
                password: password }
    }).done(function( msg ) {
        if (msg > 1){
            $('.alert').html('<b>An error occurred.</b> Please try again.').removeClass('d-none');
        }
        else if (msg > 0){
            $('.alert').html('<b>This username is taken.</b> Please try another.').removeClass('d-none');
        }
        else{
            location.href = '/';
        }
        $('form').toggleClass('loading').find('fieldset').removeAttr('disabled');
    });

    return false;
  }



  function isLoggedIn(){
    $.ajax({
        method: "GET",
        url: "/isloggedin"
    }).done(function( msg ) {
        $('.admin').hide();
        if (msg > 0){

            if (msg > 1){
                $('.admin').show().css('visibility', 'visible');
                isAdmin = true;
            }

            $('.menu_login a>span').html('<span class="h5 mr-2"><i class="fas fa-user"></i></span> Logout');
            $('.menu_login a').attr('href', '/logout');
            $('.loggedIn').removeClass('d-none');
        }
        $('.menu_login').removeClass('invisible');
    });
  }


  function del_concert(){
    p = $(this);
    $.ajax({
        method: "GET",
        url: "/del_concert",
        data : {id : $(this).parents('.ml-auto').find('input:hidden').val()}
    }).done(function( msg ) {
        if (msg == 0){
            p.parents('.result').remove();
        }
    });
  }

    function edit_concert(){
    location.href = 'add_concert?id=' + $(this).parents('.ml-auto').find('input:hidden').val();
  }

  // Image Picker
// by Rodrigo Vera
//
// Version 0.3.1
// Full source at https://github.com/rvera/image-picker
// MIT License, https://github.com/rvera/image-picker/blob/master/LICENSE
// Image Picker
// by Rodrigo Vera
//
// Version 0.3.0
// Full source at https://github.com/rvera/image-picker
// MIT License, https://github.com/rvera/image-picker/blob/master/LICENSE
(function(){var ImagePicker,ImagePickerOption,both_array_are_equal,sanitized_options,bind=function(fn,me){return function(){return fn.apply(me,arguments)}},indexOf=[].indexOf||function(item){for(var i=0,l=this.length;i<l;i++){if(i in this&&this[i]===item)return i}return-1};jQuery.fn.extend({imagepicker:function(opts){if(opts==null){opts={}}return this.each(function(){var select;select=jQuery(this);if(select.data("picker")){select.data("picker").destroy()}select.data("picker",new ImagePicker(this,sanitized_options(opts)));if(opts.initialized!=null){return opts.initialized.call(select.data("picker"))}})}});sanitized_options=function(opts){var default_options;default_options={hide_select:true,show_label:false,initialized:void 0,changed:void 0,clicked:void 0,selected:void 0,limit:void 0,limit_reached:void 0,font_awesome:false};return jQuery.extend(default_options,opts)};both_array_are_equal=function(a,b){var i,j,len,x;if(!a||!b||a.length!==b.length){return false}a=a.slice(0);b=b.slice(0);a.sort();b.sort();for(i=j=0,len=a.length;j<len;i=++j){x=a[i];if(b[i]!==x){return false}}return true};ImagePicker=function(){function ImagePicker(select_element,opts1){this.opts=opts1!=null?opts1:{};this.sync_picker_with_select=bind(this.sync_picker_with_select,this);this.select=jQuery(select_element);this.multiple=this.select.attr("multiple")==="multiple";if(this.select.data("limit")!=null){this.opts.limit=parseInt(this.select.data("limit"))}this.build_and_append_picker()}ImagePicker.prototype.destroy=function(){var j,len,option,ref;ref=this.picker_options;for(j=0,len=ref.length;j<len;j++){option=ref[j];option.destroy()}this.picker.remove();this.select.off("change",this.sync_picker_with_select);this.select.removeData("picker");return this.select.show()};ImagePicker.prototype.build_and_append_picker=function(){if(this.opts.hide_select){this.select.hide()}this.select.on("change",this.sync_picker_with_select);if(this.picker!=null){this.picker.remove()}this.create_picker();this.select.after(this.picker);return this.sync_picker_with_select()};ImagePicker.prototype.sync_picker_with_select=function(){var j,len,option,ref,results;ref=this.picker_options;results=[];for(j=0,len=ref.length;j<len;j++){option=ref[j];if(option.is_selected()){results.push(option.mark_as_selected())}else{results.push(option.unmark_as_selected())}}return results};ImagePicker.prototype.create_picker=function(){this.picker=jQuery("<ul class='thumbnails image_picker_selector'></ul>");this.picker_options=[];this.recursively_parse_option_groups(this.select,this.picker);return this.picker};ImagePicker.prototype.recursively_parse_option_groups=function(scoped_dom,target_container){var container,j,k,len,len1,option,option_group,ref,ref1,results;ref=scoped_dom.children("optgroup");for(j=0,len=ref.length;j<len;j++){option_group=ref[j];option_group=jQuery(option_group);container=jQuery("<ul></ul>");container.append(jQuery("<li class='group_title'>"+option_group.attr("label")+"</li>"));target_container.append(jQuery("<li class='group'>").append(container));this.recursively_parse_option_groups(option_group,container)}ref1=function(){var l,len1,ref1,results1;ref1=scoped_dom.children("option");results1=[];for(l=0,len1=ref1.length;l<len1;l++){option=ref1[l];results1.push(new ImagePickerOption(option,this,this.opts))}return results1}.call(this);results=[];for(k=0,len1=ref1.length;k<len1;k++){option=ref1[k];this.picker_options.push(option);if(!option.has_image()){continue}results.push(target_container.append(option.node))}return results};ImagePicker.prototype.has_implicit_blanks=function(){var option;return function(){var j,len,ref,results;ref=this.picker_options;results=[];for(j=0,len=ref.length;j<len;j++){option=ref[j];if(option.is_blank()&&!option.has_image()){results.push(option)}}return results}.call(this).length>0};ImagePicker.prototype.selected_values=function(){if(this.multiple){return this.select.val()||[]}else{return[this.select.val()]}};ImagePicker.prototype.toggle=function(imagepicker_option,original_event){var new_values,old_values,selected_value;old_values=this.selected_values();selected_value=imagepicker_option.value().toString();if(this.multiple){if(indexOf.call(this.selected_values(),selected_value)>=0){new_values=this.selected_values();new_values.splice(jQuery.inArray(selected_value,old_values),1);this.select.val([]);this.select.val(new_values)}else{if(this.opts.limit!=null&&this.selected_values().length>=this.opts.limit){if(this.opts.limit_reached!=null){this.opts.limit_reached.call(this.select)}}else{this.select.val(this.selected_values().concat(selected_value))}}}else{if(this.has_implicit_blanks()&&imagepicker_option.is_selected()){this.select.val("")}else{this.select.val(selected_value)}}if(!both_array_are_equal(old_values,this.selected_values())){this.select.change();if(this.opts.changed!=null){return this.opts.changed.call(this.select,old_values,this.selected_values(),original_event)}}};return ImagePicker}();ImagePickerOption=function(){function ImagePickerOption(option_element,picker,opts1){this.picker=picker;this.opts=opts1!=null?opts1:{};this.clicked=bind(this.clicked,this);this.option=jQuery(option_element);this.create_node()}ImagePickerOption.prototype.destroy=function(){return this.node.find(".thumbnail").off("click",this.clicked)};ImagePickerOption.prototype.has_image=function(){return this.option.data("img-src")!=null};ImagePickerOption.prototype.is_blank=function(){return!(this.value()!=null&&this.value()!=="")};ImagePickerOption.prototype.is_selected=function(){var select_value;select_value=this.picker.select.val();if(this.picker.multiple){return jQuery.inArray(this.value(),select_value)>=0}else{return this.value()===select_value}};ImagePickerOption.prototype.mark_as_selected=function(){return this.node.find(".thumbnail").addClass("selected")};ImagePickerOption.prototype.unmark_as_selected=function(){return this.node.find(".thumbnail").removeClass("selected")};ImagePickerOption.prototype.value=function(){return this.option.val()};ImagePickerOption.prototype.label=function(){if(this.option.data("img-label")){return this.option.data("img-label")}else{return this.option.text()}};ImagePickerOption.prototype.clicked=function(event){this.picker.toggle(this,event);if(this.opts.clicked!=null){this.opts.clicked.call(this.picker.select,this,event)}if(this.opts.selected!=null&&this.is_selected()){return this.opts.selected.call(this.picker.select,this,event)}};ImagePickerOption.prototype.create_node=function(){var image,imgAlt,imgClass,thumbnail;this.node=jQuery("<li/>");if(this.option.data("font_awesome")){image=jQuery("<i>");image.attr("class","fa-fw "+this.option.data("img-src"))}else{image=jQuery("<img class='image_picker_image'/>");image.attr("src",this.option.data("img-src"))}thumbnail=jQuery("<div class='thumbnail'>");imgClass=this.option.data("img-class");if(imgClass){this.node.addClass(imgClass);image.addClass(imgClass);thumbnail.addClass(imgClass)}imgAlt=this.option.data("img-alt");if(imgAlt){image.attr("alt",imgAlt)}thumbnail.on("click",this.clicked);thumbnail.append(image);if(this.opts.show_label){thumbnail.append(jQuery("<p/>").html(this.label()))}this.node.append(thumbnail);return this.node};return ImagePickerOption}()}).call(this);

  function get_desc(artist){

  $('#concertDetails .modal-body').addClass('spinner');
  $('#concertDetails .modal-body .pre-scrollable').html('');
    $.ajax({
        method: "GET",
        url: "/wiki_summary",
        dataType: "json",
        data: { artist: artist }
    }).done(function( msg ) {
        if (msg){

            $('#concertDetails .spinner').removeClass('spinner');
            $('#concertDetails .modal-body .pre-scrollable').text(msg.desc);
            $('#concertDetails .modal-body .pre-scrollable').prepend('<img src="' + msg.images[0] + '" class="artist_profile">');
            /*
            $('.desc textarea').val(msg.desc).parents('.desc').show();
            $('.desc-img .images option').remove();
            $.each(msg.images, function (key, val) {
                html = '<option data-img-src="' + val + '" data-img-alt="Page ' + key + '" value="' + key + '">  Page ' + key + '  </option>';
                $('.desc-img .images').append(html);
            });
            $(".images").imagepicker({
                  hide_select : true,
                  show_label  : false
                });
                $(".image_picker_image").on( "click", function(){
                    $(".clicked").html('<img src="' + $(this).attr('src') + '" />');
                });
                $('.image_picker_image').first().trigger('click');*/
        }
    });
  }


  function hot(){
    $.ajax({
        method: "GET",
        dataType: "json",
        url: "/hot_concerts"
    }).done(function( msg ) {
        var template = $.templates("#theTmpl");
        var htmlOutput = template.render(msg);
        $(".hot .result").remove();
        $(".hot .container").append(htmlOutput);
        if (isAdmin){
            $('.admin').show().css('visibility', 'visible');
        }
    });
  }

function update_price(){
    var cat = $('.tickets_cat').val().split(" ");
    cat = cat[cat.length-1].replace('$');
    var price = parseInt($('.tickets_num').val()) * parseInt(cat);
    $('.price').text(price + '$');
}

function buy(){
try{
update_price();
 $('.modal.modal-buy *').change(function(){
    update_price();
 });
 }
 catch(e){}
}

var results;
function search(){
    $('form').toggleClass('loading').find('fieldset').attr('disabled','');
    $(".results .result").remove().addClass('spinner');
    page = 0;

    data = {};
    if (typeof getUrlParameter('concert_id') !== "undefined"){
        data = {concert_id : getUrlParameter('concert_id')};
    }
    else if (typeof getUrlParameter('artist_id') !== "undefined"){
        data = {artist_id : getUrlParameter('artist_id')};
    }

    $.ajax({
        method: "GET",
        url: "/find2",
        dataType: "json",
        data: data
    }).done(function( msg ) {
        if (!Array.isArray(msg.concerts)){

            msg.artists = JSON.parse(msg.artists);

            h = '';
            for (i=0; i < msg.artists.length;i++){
                h += '<button type="button" class="btn btn-outline-warning ml-2" artistid="' + msg.artists[i].id + '">' + msg.artists[i].name + '</button>';
            }
            msg.artists_links = h;
        }
        else
        {
            arts = JSON.parse(msg.artists);

            j = 0;
            curc = msg.concerts[j];
            curcid = msg.concerts[j].id;
            for (i=0; i < arts.length;i++){
                cid = arts[i].concert_id;
                while (cid > curcid){
                    curc = msg.concerts[++j];
                    curcid = msg.concerts[j].id;
                }
                curc.artists_links += '<button type="button" class="btn btn-outline-warning ml-2" artistid="' + arts[i].id + '">' + arts[i].name + '</button>'
            }

        }

        results = msg;

        var template = $.templates("#theTmpl");
        var htmlOutput = template.render(msg.concerts);

        $(".results").append(htmlOutput).removeClass('spinner');
        $('.prev').removeClass('d-none');

        $('.result #concert_artists button').click(function(){
        artist_id = $(this).attr('artistid');

        get_desc($(this).text());

        $('#concertDetails #concertTitle').text($(this).text());
        $('#concertDetails #btnAll span').text($(this).text()).parent().attr('href','find?artist_id=' + artist_id);
        $('#concertDetails').modal();
/*
        $.ajax({
        method: "GET",
        dataType: "json",
        data: {id : artist_id},
        url: "/artist"
    }).done(function( msg ) {
            msg = JSON.parse(msg);

    });
*/
        });

        if (isAdmin){
            $('.admin').show().css('visibility', 'visible');
            $('.icon-delete').click(del_concert);
            $('.icon-edit').click(edit_concert);
        }
        $('form').toggleClass('loading').find('fieldset').removeAttr('disabled');
    });
}

function concert_manip(){
    $.ajax({
        method: "GET",
        dataType: "json",
        data: {id : getUrlParameter('id')},
        url: "/edit_concert"
    }).done(function( msg ) {
        if (msg != ''){
            $('#name').val(msg.name);
            $('#capacity').val(msg.capacity);
            $('#from').val(msg.start);
            $('#to').val(msg.end);
            $('.add_concert').text('Update');
        }
    });
}
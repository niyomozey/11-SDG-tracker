( function( $ ) {
		jQuery(document).ready(function(){
			
            jQuery('.m-menu').click(function(){
            	jQuery(this).toggleClass('open');
				jQuery('.navbar').slideToggle();

			});
		jQuery('.img_bg').children('img').each(function(n, img) {
				img = jQuery(img);
				var imgUrl = jQuery(this).attr('src');
				img.parents('.img_bg').css({
					'background': '#fff url(' + imgUrl + ') right center  no-repeat'
				});
				img.hide();
			});	
            subMenu();
		});
		jQuery(window).scroll(function() {
			var headerheight = jQuery(".header").height();
			if(jQuery(window).scrollTop() > headerheight){			
				jQuery('.header').addClass("sticky"); 
			}else{
				jQuery('.header').removeClass("sticky"); 
			}
		});  
		function subMenu(){
			jQuery(".nav > li .submenu").before('<span class="mobile-arrow">+</span>');
			jQuery(".nav > li > .mobile-arrow").click(function() {
				if(jQuery(this).next("ul.submenu").is(":visible")){
					jQuery(this).next("ul.submenu").slideUp();
					jQuery(this).text("+");
				}
				else
				{
					jQuery(".nav > li .submenu").slideUp();
					jQuery(".nav > li .mobile-arrow").text("+");
					jQuery(this).next("ul.submenu").slideDown();
					jQuery(this).text("-");
				}		
			});
			jQuery(".submenu > li .mobile-arrow").click(function() {
				if(jQuery(this).next("ul.submenu").is(":visible")){
					jQuery(this).next("ul.submenu").slideUp();
					jQuery(this).text("+");
				}
				else
				{
					jQuery(".submenu > li .submenu").slideUp();
					jQuery(".submenu > li .mobile-arrow").text("+");
					jQuery(this).next("ul.submenu").slideDown();
					jQuery(this).text("-");
				}		
			});
		}
		$('.main_news .bbs_list').matchHeight({
			property: 'min-height'
		});
		$('.main_news .bbs_list p').matchHeight({
			property: 'min-height'
		});
		$('.matchHeight').matchHeight({
			property: 'height'
		});
		$('.main_news .col-sm-4').matchHeight({
			property: 'height'
		});
} )( jQuery );
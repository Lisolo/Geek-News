$(document).ready(function() {
	$('#likes-tag').click(function() {
		var tagid;
		tagid = $(this).attr("data-tagid");
		$('#likes-tag').prop("disabled", true);
		$('#likes-tag').removeClass();
		$('#likes-tag').addClass("btn btn-danger btn-sm");
		var data = parseInt($('#like-tag-count').html()) + 1;
		$('#like-tag-count').html(data);
		$.get('/share/like_tag/', {tag_id: tagid});
	});

	$('.news-like').click(function() {
		var newsid;
		newsid = $(this).attr("data-newsid");
		$(this).prop("disabled", true);
		$(this).removeClass();
		$(this).addClass("btn btn-primary btn-sm");
		var data = parseInt($('#likes-' + newsid).html()) + 1;
		$('#likes-' + newsid).html(data);
		$.get('/share/likes_news/', {news_id: newsid});
	});

	$('.news-dislike').click(function() {
		var newsid;
		newsid = $(this).attr("data-newsid");
		$(this).prop("disabled", true);
		$(this).removeClass();
		$(this).addClass("btn btn-primary btn-sm");
		var data = parseInt($('#dislikes-' + newsid).html()) + 1;
		$('#dislikes-' + newsid).html(data);
		$.get('/share/dislikes_news/', {news_id: newsid});
	});
    
	$('.vote-up').click(function() {
		var commentd;
		commentid = $(this).attr("data-commid");
		var data = parseInt($('#vote-' + commentid).html()) + 1;
		$('#vote-' + commentid).html(data);
		$(this).prop("disabled", true);
		$(this).removeClass();
		$(this).addClass("btn btn-primary btn-sm");
		$.get('/share/vote_comment/', {comment_id: commentid});
	});
	
    $('.book-like').click(function() {
		var bookid;
		bookid = $(this).attr("data-tagid");
		var data = parseInt($('#likes-' + bookid).html()) + 1;
		$('#likes-' + bookid).html(data);
		$(this).prop("disabled", true);
		$(this).removeClass();
		$(this).addClass("btn btn-danger btn-sm");
		$.get('/share/likes_book/', {book_id: bookid});
	});

	$('#suggestion1').keyup(function() {
		var query;
		query = $(this).val();
		$.get('/share/suggest_news/', {suggestion: query}, function(data) {
			$('#news').html(data);
		});
	});
	
	$('.share-add').click(function() {
		var tagid = $(this).attr("data-tagid");
		var url = $(this).attr("data-url");
		var title = $(this).attr("data-title");
		var me = $(this);
		$.get('/share/auto_add_news/', {tag_id : tagid, url: url, title: title}, function(data) {
			$('#news').html(data);
			me.hide();
		});
	});

    // Add refresh button after field (this can be done in the template as well)
    $('img.captcha').after(
            $('<button class="captcha-refresh btn btn-sm"><span class="glyphicon glyphicon-refresh"></span></button>')
            );

    // Click-handler for the refresh-link
    $('.captcha-refresh').click(function(){
        var $form = $(this).parents('form');
        var url = location.protocol + "//" + window.location.hostname + ":"
                  + location.port + "/captcha/refresh/";

        // Make the AJAX-call
        $.getJSON(url, {}, function(json) {
            $form.find('input[name="captcha_0"]').val(json.key);
            $form.find('img.captcha').attr('src', json.image_url);
        });
        return false;
    });
});
$(document).ready(function() {
	$('#likes-category').click(function() {
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/share/like_category/', {category_id: catid}, function(data) {
			$('#like-category-count').html(data);
			$('#likes-category').hide();
		});
	});

	$('.news-like').click(function() {
		var newsid;
		newsid = $(this).attr("data-catid");
		var me = $(this);
		$.get('/share/likes_news/', {news_id: newsid}, function(data) {
			$('#likes-' + newsid).html(data);
			me.hide();
		});
	});

	$('.news-dislike').click(function() {
		var cnews;
		newsid = $(this).attr("data-catid");
		var me = $(this);
		$.get('/share/dislikes_news/', {news_id: newsid}, function(data) {
			$('#dislikes-' + newsid).html(data);
			me.hide();
		});
	});
    
	$('.vote-up').click(function() {
		var commentd;
		commentid = $(this).attr("data-catid");
		var me = $(this);
		$.get('/share/vote_comment/', {comment_id: commentid}, function(data) {
			$('#vote-' + commentid).html(data);
			me.hide();
		});
	});
	
    $('.book-like').click(function() {
		var bookid;
		bookid = $(this).attr("data-catid");
		var me = $(this);
		$.get('/share/likes_book/', {book_id: bookid}, function(data) {
			$('#likes-' + bookid).html(data);
			me.hide();
		});
	});

	$('#suggestion1').keyup(function() {
		var query;
		query = $(this).val();
		$.get('/share/suggest_news/', {suggestion: query}, function(data) {
			$('#news').html(data);
		});
	});
	
	$('.share-add').click(function() {
		var catid = $(this).attr("data-catid");
		var url = $(this).attr("data-url");
		var title = $(this).attr("data-title");
		var me = $(this);
		$.get('/share/auto_add_news/', {category_id : catid, url: url, title: title}, function(data) {
			$('#news').html(data);
			me.hide();
		});
	});
});
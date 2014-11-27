$(document).ready(function() {
	$('#likes-category').click(function() {
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/share/like_category/', {category_id: catid}, function(data) {
			$('#like-category-count').html(data);
			$('#likes-category').hide()
		});
	});

	$('#likes-news').click(function() {
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/share/likes_news/', {new_id: catid}, function(data) {
			$('#likes-news-count').html(data);
			$('#likes-news').hide()
		});
	});

	$('#dislikes-news').click(function() {
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/share/dislikes_news/', {new_id: catid}, function(data) {
			$('#dislikes-news-count').html(data);
			$('#dislikes-news').hide()
		});
	});
	
	$('#suggestion1').keyup(function() {
		var query;
		query = $(this).val();
		$.get('/share/suggest_news/', {suggestion: query}, function(data) {
			$('#news').html(data);
		});
	});
	
	$('#share-add').click(function() {
		var catid = $(this).attr("data-catid");
		var url = $(this).atrr("data-url");
		var title = $(this).attr("data-title");
		var me = $(this);
		$get('/share/auto_add_new/', {category_id : catid, url: url, title: title}, function(data) {
			$('#news').html(data);
			me.hide();
		});
	});
});
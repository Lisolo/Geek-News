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
		var catid;
		catid = $(this).attr("data-catid");
		var me = $(this);
		$.get('/share/likes_news/', {new_id: catid}, function(data) {
			$('#likes-' + catid).html(data);
			me.hide();
		});
	});

	$('.news-dislike').click(function() {
		var catid;
		catid = $(this).attr("data-catid");
		var me = $(this);
		$.get('/share/dislikes_news/', {new_id: catid}, function(data) {
			$('#dislikes-' + catid).html(data);
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
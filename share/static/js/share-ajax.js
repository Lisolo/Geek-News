$(document).ready(function() {
	$('#likes-category').click(function() {
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/share/like_category/', {category_id: catid}, function(data) {
			$('#like-category-count').html(data);
			$('#likes-category').hide()
		});
	});

	$('#likes-new').click(function() {
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/share/like_new/', {new_id: catid}, function(data) {
			$('#like-new-count').html(data);
			$('#likes-new').hide()
		});
	});

	$('#dislikes-new').click(function() {
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/share/dislike_new/', {new_id: catid}, function(data) {
			$('#dislike-new-count').html(data);
			$('#dislikes-new').hide()
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

$(function() {

	function addDateFormat(date, format) {
	    date = new Date(date);
	    var map = {
	        "M": date.getMonth() + 1, //月份
	        "d": date.getDate(), //日
	        "h": date.getHours(), //小时
	        "m": date.getMinutes(), //分
	        "s": date.getSeconds(), //秒
	        "q": Math.floor((date.getMonth() + 3) / 3), //季度
	        "S": date.getMilliseconds() //毫秒
	    };
	    format = format.replace(/([yMdhmsqS])+/g, function(all, t){
	        var v = map[t];
	        if(v !== undefined){
	            if(all.length > 1){
	                v = '0' + v;
	                v = v.substr(v.length-2);
	            }
	            return v;
	        }
	        else if(t === 'y'){
	            return (date.getFullYear() + '').substr(4 - all.length);
	        }
	        return all;
	    });
	};


	$('.load-article-btn').click(function() {
		var self = $(this);
		self.button('loading');
		var cPage = parseInt($(this).attr('data-current-page'));
		var page = cPage + 1;
		var categoryId = $(this).attr('data-category-id');
		if(!categoryId){
			categoryId = 0;
		}
		var url = '/article_list/' + categoryId + '/' + page + '/';
		phajax.get({
			'url': url,
			'success':function(data) {
				if(data['code'] == 200){
					// 将文章列表追加到之前的ul后面
					var articles = data['data']['articles'];
					if(articles.length > 0){
						for (var i = 0; i < articles.length; i++) {
							console.log(articles[i]['desc']);
							if(!articles[i]['desc']){
								var text = $(articles[i]['content']).text();
								articles[i]['desc'] = text.substring(0,100);
								if(text.length > 100){
									articles[i]['desc'] += '...';
								}

							}
							var html = xttemplate.template('article-list-tpl',{'article':articles[i]});
							$('#article-list-box').append(html);
						}
						self.attr('data-current-page',page);
						self.button('reset');
					}else{
						self.html('没有更多文章');
						self.attr('disabled','disabled');
					}
				}else{
					xtalert.alertErrorToast(data['message']);
				}
			}
		});
	});
});
/**
 * Created by yuan on 2017/5/29.
 */

$(function () {
    function article_deal(btn,url,text) {
        var tdParent = btn.parent().parent();
        var uid = tdParent.attr('data-article-uid');
        if(text == '文章删除成功'){
            xtalert.alertConfirm({
                'title':'你确定要删除这篇文章吗？',
                'confirmCallback':function () {
                    setTimeout(function () {
                        post_submit();
                    },500);
                }
            });
        }else{
            post_submit();
        }
        function post_submit() {
            phajax.post({
           'url':url,
            'data':{'uid':uid},
            'success':function (data) {
                if(data['code'] == 200){
                    setTimeout(function () {
                        window.location = '/cms/';
                    },1000);
                    xtalert.alertSuccessToast(text)
                }else{
                    xtalert.alertErrorToast(data['message']);
                }
            }
        });
        }
}
    window.article_deal = article_deal;
});

$(function () {
    $('.delete-article').click(function (event) {
        event.preventDefault();
        window.article_deal($(this),'/cms/delete_article/','文章删除成功');
    });
});

$(function () {
    $('.top-article').click(function (event) {
        event.preventDefault();
        var url = '/cms/top_article/';
        var text = '文章置顶成功';
        if($(this).text().indexOf('取消置顶')>0){
            url =  '/cms/untop_article/';
            text = '文章取消置顶成功';
        }
        window.article_deal($(this),url,text);
    });
});

$(function () {
   $('#category-select').change(function (event) {
       event.preventDefault();
       category_id = $(this).val();
       window.location = '/cms/article_manage/1/'+category_id + '/';
   }); 
});

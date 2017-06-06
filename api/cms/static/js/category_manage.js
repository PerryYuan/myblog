/**
 * Created by yuan on 2017/5/29.
 */

$(function () {
    $('.category-editer').click(function (event) {
        event.preventDefault();
        var tr = $(this).parent().parent();
        var id = tr.attr('data-category-id');
        xtalert.alertOneInput({
            'placeholder':'请输入新的分类名称',
            'confirmText':'确定修改',
            'confirmCallback':function (inputValue) {
                phajax.post({
                    'url':'/cms/category_editer/',
                    'data':{
                        'id':id,
                        'name':inputValue
                    },
                    'success':function (data) {

                        if(data['code'] == 200){
                            tr.children().eq(0).html(inputValue);
                            setTimeout(function () {
                                xtalert.alertSuccessToast('修改成功');
                            },500);
                        }else{
                            xtalert.alertErrorToast(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $('.category-delete').click(function (event) {
        event.preventDefault();
        var tr = $(this).parent().parent();
        var id = tr.attr('data-category-id');
        xtalert.alertConfirm({
            'title':'你确定删除该分类吗？',
            'confirmCallback':function () {
                phajax.post({
                    'url':'/cms/category_delete/',
                    'data':{'id':id},
                    'success':function (data) {
                        if(data['code'] == 200){
                            tr.remove();
                            setTimeout(function () {
                                xtalert.alertSuccessToast('删除成功');
                            },500);
                        }else{
                            setTimeout(function () {
                                xtalert.alertErrorToast(data['message']);
                            },500);

                        }
                    }
                });
            }
        })
    });
});

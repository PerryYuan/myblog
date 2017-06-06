/**
 * Created by yuan on 2017/5/12.
 */


$(function () {
    var flag = false;
    xtqiniu.setUp({
        'browse_btn':'avatar',
        'success': function (up,file,info) {
            var avatar = file.name;
            $('#avatar').attr('src',avatar);
            flag = true;
            $("#btn-save").removeAttr("disabled");
        },
        'fileadded':function (up,files) {
            $('#btn-save').attr({"disabled":"disabled"});
        }
    });

    $('#btn-save').click(function (event) {
        event.preventDefault();
        var username = $('#username').val();
        var data = {'username':username};
        if(flag){
            data['avatar'] = $('#avatar').attr('src');
            flag = false;
        }
        phajax.post({
            'url':'/cms/update_profile/',
            'data':data,
            'success':function (data) {
                if(data['code']==200){
                    xtalert.alertSuccessToast('修改成功');
                }else{
                    xtalert.alertErrorToast(data['error']);
                }
            }
        })
    });
});

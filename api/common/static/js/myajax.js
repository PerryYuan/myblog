/**
 * Created by yuan on 2017/3/5.
 */

//获取cookie的方法
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function () {
    phajax = {
         'ajax':function (args) {
             if(!args['error']){
                 args['error'] = function (error) {
                    xtalert.alertNetworkError(error);
                 }
             }
            this.ajaxSetup();
            $.ajax(args);
        },
        'get':function (args) {
            args['type'] = 'get';
            this.ajax(args);
        },
        'post':function (args) {
            args['type'] = 'post';
            this.ajax(args);
        },
        'ajaxSetup':function () {
            $.ajaxSetup({
                'beforeSend':function(xhr,settings) {
                    var csrftoken = getCookie('csrftoken');
                    //2.在header当中设置csrf_token的值
                    xhr.setRequestHeader('X-CSRFToken',csrftoken);
                }
            });
        }
    }
});

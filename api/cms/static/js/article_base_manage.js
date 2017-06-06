/**
 * Created by yuan on 2017/5/29.
 */

$(function () {
    var url = window.location.href;
    var nav_box = $('.nav-box-2');
    var index = 0;
    if(url.indexOf('category_manage') >= 0){
        index = 1;
    }else if(url.indexOf('common') >= 0){
        index = 2;
    }
    console.log(nav_box.children().eq(index));
    nav_box.children().eq(index).addClass('active').siblings().removeClass('active');
});

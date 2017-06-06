/**
 * Created by yuan on 2017/5/10.
 */

$(document).ready(function () {
    var ul_meau = $('.ul-meau');
    var lacationUrl = window.location.href;
    var index = 0;
    if(lacationUrl.indexOf('add_article') > 0){
        index = 1;
    }else if(lacationUrl.indexOf('setting') > 0){
        index = -1;
    }else{
        index = 0;
    }
    if(index >= 0){
        ul_meau.children().eq(index).addClass('active').siblings().removeClass('active')
    }else{
        ul_meau.children().removeClass('active');
    }
});
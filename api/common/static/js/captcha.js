/**
 * Created by yuan on 2017/5/11.
 */

$(function () {
    $('#flush-captcha').click(function (event) {
        event.preventDefault();
        var image = $('.captcha-img');
        var imgSrc = xtparam.setParam(image.attr('src'),'xx',Math.random());
        image.attr('src',imgSrc);
    });
});

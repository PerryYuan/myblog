/**
 * Created by yuan on 2017/5/25.
 */

$(function () {
    var toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough', 'fontScale', 'color', 'ol', 'ul', 'blockquote', 'code', 'table', 'link', 'image', 'hr', 'indent', 'outdent', 'alignment',];
    var editor = new Simditor({
        textarea: $('#editor'),
        toorbar:toolbar,
        pasteImage: true
    });
    window.editor = editor;
});

$(function () {
    $('#add-category').click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'title':'添加分类',
            'text':'分类名',
            'confirmCallback':function (inputValue) {
                phajax.post({
                    'url':'/cms/add_category/',
                    'data':{'name':inputValue},
                    'success':function (data) {
                        if(data['code'] == 200){
                            var select_category = $('#select-category');
                            var option = $('<option></option>');
                            option.attr('value',data['data']['id']);
                            option.html(data['data']['name']);
                            select_category.append(option);
                            select_category.children().last().attr('selected','selected').siblings().removeAttr('selected');
                            setTimeout(function(){
                                xtalert.alertSuccessToast('添加成功');
                            },500);
                        }else{
                           setTimeout(function(){
                                xtalert.alertErrorToast(data['message']);
                            },500);
                        }
                    },
                    'error':function (error) {
                        xtalert.alertErrorToast('网路错误');
                    }
                });
            }
        });
    });
});

$(function () {
    $('#add-tag').click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'title':'添加标签',
            'text':'标签名',
            'confirmCallback':function (inputValue) {
                phajax.post({
                    'url':'/cms/add_tag/',
                    'data':{'name':inputValue},
                    'success':function (data) {
                        if(data['code'] == 200){
                            var data = data['data'];
                            console.log('1--------------------');
                            console.log(data['id']+data['name']);
                            console.log('1--------------------');
                            var add_tag_html = template('add-tag-html',data);
                            //var label = $("<label class='checkbox-inline'></label>");
                            //创建一个input
                            // var input = $("<input type='checkbox'/>");
                            // input.val(data['id']);
                            // input.attr('checked','checked');
                            // label.append(input);
                            // label.append(data['name']);
                            var add_tab_box = $('#add-tag-box');
                            if(add_tab_box.find("span").length>0){
                                add_tab_box.html('');
                            }
                            add_tab_box.append(add_tag_html);
                            setTimeout(function(){
                                xtalert.alertSuccessToast('添加成功');
                            },500);
                        }else{
                           setTimeout(function(){
                                xtalert.alertErrorToast(data['message']);
                            },500);
                        }
                    },
                    'error':function (error) {
                        xtalert.alertErrorToast('网路错误');
                    }
                });
            }
        });
    });
});

$(function () {
    xtqiniu.setUp({
        'browse_btn':'thumbnail',
        'success':function (up,file,info) {
            $('#thumbnail-input').val(file.name);
        }
    });
});

$(function () {
   $('#add-article').click(function (event) {
       event.preventDefault();
       var titleInput = $('input[name=title-input]');
       var descInput = $('input[name=desc-input]');
       var thumbnailInput = $('#thumbnail-input');
       var tagsInput = $('input[name=tags-input]');
       
       var category = $('#select-category').val();
       var title = titleInput.val();
       var desc = descInput.val();
       var thumbnail = thumbnailInput.val();
       var content = window.editor.getValue();
       var tags = [];
       var uid = $(this).attr('article-uid-data');
       tagsInput.each(function () {
           if($(this).is(':checked')){
               tags.push($(this).val());
           }
       });
       phajax.post({
           'url':window.location.href,
           'data':{
               'category':category,
               'title':title,
               'desc':desc,
               'thumbnail':thumbnail,
               'content':content,
               'tags[]':tags,
               'uid':uid
           },
           'success':function (data) {
               if(data['code'] == 200){
                   var title = '博客修改成功';
                   var cancelText = '继续修改';
                   if(window.location.href.indexOf('add_article')>0){
                       title = '博客发表成功';
                       cancelText = '再发一篇';
                   }
                   xtalert.alertConfirm({
                       'title':title,
                       'confirmText':'返回首页',
                       'cancelText':cancelText,
                       'confirmCallback':function () {
                           window.location = '/cms';
                       },
                       'cancelCallback':function () {
                           window.location.reload();
                       }
                   });

               }else{
                   xtalert.alertErrorToast(data['message']);
               }
           },
       });
   });
});

/**
 * Created by Administrator on 14-9-15.
 */

//打标签按钮
function validate() {
    if (window.confirm('确认全部打标签？')) {
        //alert("确定");

        $('.format_prod').each(function (i) {
            var fp = $(this).attr('data-fp');
            if ($(this).prop('checked') == true) {
                $('#sel' + fp).attr('value', 1);
            }
            else {
                $('#sel' + fp).attr('value', 0);
            }
        });
        document.getElementById('form_post').submit();
    } else {
        //alert("取消");
    }
}

//打标签，根据打标签按钮更新对应单品的checkbox
function add_checkbox(fp) {
//    alert(fp);
    $button = $('#buttons' + fp + ' button');
    $input = $('#edit' + fp + ' input');
    $addButton = $('#add' + fp);

    $button.each(function (i) {
        if ($(this).attr('class').indexOf('active') >= 0) {
            var tag = $(this).attr('value');
//            var input_id = $(this).attr('data-ref');
            if ($input.eq(i).prop('checked') == false) {
                $input.eq(i).prop('checked', true);
                $('<button type="button"' + ' value=' + tag + ' data-fp="' + fp + '" class="btn btn-success btn-xs" onclick="del_checkbox(this);">'
                    + tag + '<i class="glyphicon glyphicon-remove"></i></button><span> </span>').insertBefore($addButton);
            }

//        只增加，不减少
//        else {
//            $input.eq(i).prop('checked', false);
//        }
            $(this).removeClass('active');
        }
    });
}

//标签按钮单击删除
function del_checkbox(self) {

    var fp = $(self).attr('data-fp');
    var val = $(self).attr('value');
//    alert(fp);
    $input = $('#edit' + fp + ' input');

    $input.each(function (i) {
        if ($(this).attr('value') == val) {
            $(this).prop('checked', false);
        }
    });
    $(self).remove();
}

//刷标签
function format_tags() {
    $('.format_prod').each(function (i) {
        if ($(this).prop('checked') == true) {
            var fp = $(this).attr('data-fp');
            format_checkbox(fp);
        }
    });
    $button = $('#format_button button');
    $button.each(function (i) {
        $(this).removeClass('active');
    });
}

//根据刷标签按钮更新checkbox
function format_checkbox(fp) {
//    alert(fp);
    $button = $('#format_button button');
    $input = $('#edit' + fp + ' input');
    $addButton = $('#add' + fp);

    $button.each(function (i) {
        if ($(this).attr('class').indexOf('active') >= 0) {
            var tag = $(this).attr('value');
            if ($input.eq(i).prop('checked') == false) {
                $input.eq(i).prop('checked', true);
                $('<button type="button"' + ' value=' + tag + ' data-fp="' + fp + '" class="btn btn-success btn-xs" onclick="del_checkbox(this);">'
                    + tag + '<i class="glyphicon glyphicon-remove"></i></button><span> </span>').insertBefore($addButton);
            }
        }
    });
//    $button.each(function (i) {
//        $(this).removeClass('active');
//    });
}
//全选
function select_all() {
    $('.format_prod').each(function (i) {
        $(this).prop('checked', true);
    });
    $('#sel_all').hide();
    $('#unsel_all').show();
    display_sel_num();
}

//反选
function unselect_all() {
    $('.format_prod').each(function (i) {
        $(this).prop('checked', false);
    });
    $('#sel_all').show();
    $('#unsel_all').hide();
    display_sel_num();
}

//双击打开新增面板
function open_modal(fp) {

    $('#edit' + fp).modal('show');
}

//删除类目
function del_sort() {
    var sort = $('#sort :selected').val();
    var chose_product = false;
    //根据format_prod选择，勾选对应单品sel+fp的select，用于post时更新该单品。同时将当前'#edit' + fp + ' input中对应选项checked
    $('.format_prod').each(function (i) {
        var fp = $(this).attr('data-fp');
        $input = $('#edit' + fp + ' input');
        if ($(this).prop('checked') == true) {
            chose_product = true;

            //所选单品提交保存，未选不保存修改
            $('#sel' + fp).attr('value', 1);
            $input.each(function (i) {

                if ($(this).val() == sort) {
                    $(this).prop('checked', false);
                }
            });

        }
        else {
            $('#sel' + fp).attr('value', 0);
        }
    });

    if (sort != '' && sort != '0') {
        if (chose_product) {
            if (window.confirm('确认删除所选类目？\n类目：' + sort)) {
                //alert("确定");
                document.getElementById('form_post').submit();
            } else {
                //alert("取消");
            }
        }
        else {
            alert("请选择至少一个单品！");
        }
    }
    else {
        alert("请选择类目分类!");
    }
}

//增加类目
function add_sort() {
    $button = $('#addsort_button button');
    var add_tags = new Array();
    var chose_product = false;
    $('.format_prod').each(function (i) {
        if ($(this).prop('checked') == true) {
            chose_product = true;

            var fp = $(this).attr('data-fp');
            $input = $('#edit' + fp + ' input');

            //所选单品提交保存，未选不保存修改
            $('#sel' + fp).attr('value', 1);
            $button.each(function (i) {
                if ($(this).attr('class').indexOf('active') >= 0) {
                    var tag = $(this).attr('value');

                    if ($input.eq(i).prop('checked') == false) {
                        $input.eq(i).prop('checked', true);
                    }
                }
            });
        }
    });

    //取消类目选择，生成类目列表
    $button.each(function (i) {
        if ($(this).attr('class').indexOf('active') >= 0) {
            add_tags.push($(this).attr('value'));
            $(this).removeClass('active');
        }
    });

    //确定更新
    if (add_tags.length > 0 && chose_product) {
        if (window.confirm('确认增加所选类目？\n类目:' + add_tags)) {
            //alert("确定");
            document.getElementById('form_post').submit();
        } else {
            //alert("取消");
        }
    }
    else {
        alert("请选择至少一个单品、一个类目！");
    }

}

//删除标签
function del_tags() {
    var sort = $('#sort :selected').val();
    var chose_product = false;
    //根据format_prod选择，勾选对应单品sel+fp的select，用于post时更新该单品。同时将当前'#edit' + fp + ' input中对应选项checked
    $('.format_prod').each(function (i) {
        var fp = $(this).attr('data-fp');
        $input = $('#edit' + fp + ' input');
        if ($(this).prop('checked') == true) {
            chose_product = true;

            //所选单品提交保存，未选不保存修改
            $('#sel' + fp).attr('value', 1);
            $input.each(function (i) {

                if ($(this).val() == sort) {
                    $(this).prop('checked', false);
                }
            });

        }
        else {
            $('#sel' + fp).attr('value', 0);
        }
    });

    if (sort != '' && sort != '0') {
        if (chose_product) {
            if (window.confirm('确认删除所选标签？\n标签：' + sort)) {
                //alert("确定");
                document.getElementById('form_post').submit();
            } else {
                //alert("取消");
            }
        }
        else {
            alert("请选择至少一个单品！");
        }
    }
    else {
        alert("请选择标签分类!");
    }

}

//增加标签
function add_tags() {
    $button = $('#addsort_button button');
    var add_tags = new Array();
    var chose_product = false;
    $('.format_prod').each(function (i) {
        if ($(this).prop('checked') == true) {
            chose_product = true;

            var fp = $(this).attr('data-fp');
            $input = $('#edit' + fp + ' input');

            //所选单品提交保存，未选不保存修改
            $('#sel' + fp).attr('value', 1);
            $button.each(function (i) {
                if ($(this).attr('class').indexOf('active') >= 0) {
                    var tag = $(this).attr('value');

                    if ($input.eq(i).prop('checked') == false) {
                        $input.eq(i).prop('checked', true);
                    }
                }
            });
        }
    });

    //取消类目选择，生成类目列表
    $button.each(function (i) {
        if ($(this).attr('class').indexOf('active') >= 0) {
            add_tags.push($(this).attr('value'));
            $(this).removeClass('active');
        }
    });

    //确定更新
    if (add_tags.length > 0 && chose_product) {
        if (window.confirm('确认增加所选标签？\n标签:' + add_tags)) {
            //alert("确定");
            document.getElementById('form_post').submit();
        } else {
            //alert("取消");
        }
    }
    else {
        alert("请选择至少一个单品、一个标签！");
    }

}



//增加款式
function add_genders() {
    $button = $('#addsort_button button');
    var add_genders = new Array();
    var chose_product = false;
    $('.format_prod').each(function (i) {
        if ($(this).prop('checked') == true) {
            chose_product = true;

            var fp = $(this).attr('data-fp');
            $input = $('#edit' + fp + ' input');

            //所选单品提交保存，未选不保存修改
            $('#sel' + fp).attr('value', 1);
            $button.each(function (i) {
                if ($(this).attr('class').indexOf('active') >= 0) {
                    var gender = $(this).attr('value');

                    if ($input.eq(i).prop('checked') == false) {
                        $input.eq(i).prop('checked', true);
                    }
                }
            });
        }
    });

    //取消类目选择，生成类目列表
    $button.each(function (i) {
        if ($(this).attr('class').indexOf('active') >= 0) {
            add_genders.push($(this).attr('value'));
            $(this).removeClass('active');
        }
    });

    //确定更新

    if (add_genders.length > 0 && chose_product) {
        var num = add_genders.length
        var show = add_genders
        if (num > 1){
                alert("只能选择一个款式！");
        }
        else {
                if (show == 'male'){
                if (window.confirm('确认增加所选款式？\n款式:' + '男款')) {
                    //alert("确定");
                    document.getElementById('form_post').submit();}
                else {
            //alert("取消");
            // }
        }
        }
            if (show == 'female'){
                if (window.confirm('确认增加所选款式？\n款式:' + '女款')) {
                    //alert("确定");
                    document.getElementById('form_post').submit();}
                else {
            //alert("取消");
            // }
        }
        }
            if (show == 'None'){
                if (window.confirm('确认增加所选款式？\n款式:' + '其他')) {
                    //alert("确定");
                    document.getElementById('form_post').submit();}
                else {
            //alert("取消");
            // }
        }
        }
        }
    }
    else {
        alert("请选择至少一个单品、一个款式！");
    }

}

//删除款式
function del_genders() {
    var sort = $('#sort :selected').val();
    var chose_product = false;
    var show = sort;
    //根据format_prod选择，勾选对应单品sel+fp的select，用于post时更新该单品。同时将当前'#edit' + fp + ' input中对应选项checked
    $('.format_prod').each(function (i) {
        var fp = $(this).attr('data-fp');
        $input = $('#edit' + fp + ' input');
        if ($(this).prop('checked') == true) {
            chose_product = true;

            //所选单品提交保存，未选不保存修改
            $('#sel' + fp).attr('value', 1);
            $input.each(function (i) {

                if ($(this).val() == sort) {
                    $(this).prop('checked', false);
                }
            });

        }
        else {
            $('#sel' + fp).attr('value', 0);
        }
    });

    if (sort != '' && sort != '0') {
        if (chose_product) {
            if (show == 'male'){
                if (window.confirm('确认删除所选款式？\n款式：' + '男款')) {
                //alert("确定");
                document.getElementById('form_post').submit();
                } else {
                //alert("取消");
                }
            }

            if (show == 'female'){
                if (window.confirm('确认删除所选款式？\n款式：' + '女款')) {
                //alert("确定");
                document.getElementById('form_post').submit();
                } else {
                //alert("取消");
                }
            }

            if (show == 'None'){
                if (window.confirm('确认删除所选款式？\n款式：' + '其他')) {
                //alert("确定");
                document.getElementById('form_post').submit();
                } else {
                //alert("取消");
            }
        }
        }


        else {
            alert("请选择至少一个单品！");
        }
    }
    else {
        alert("请选择款式!");
    }

}


//添加款式，根据添加款式按钮更新对应单品的checkbox
function add_checkbox2(fp) {
//    alert(fp);
    $button = $('#buttons' + fp + ' button');
    $input = $('#edit' + fp + ' input');
    $addButton = $('#add' + fp);

    $button.each(function (i) {
        if ($(this).attr('class').indexOf('active') >= 0) {
            var gender = $(this).attr('value');
//            var input_id = $(this).attr('data-ref');
            if ($input.eq(i).prop('checked') == false) {
                $input.eq(i).prop('checked', true);
                $('<button type="button"' + ' value=' + gender + ' data-fp="' + fp + '" class="btn btn-success btn-xs" onclick="del_checkbox(this);">'
                    + tag + '<i class="glyphicon glyphicon-remove"></i></button><span> </span>').insertBefore($addButton);
            }

//        只增加，不减少
//        else {
//            $input.eq(i).prop('checked', false);
//        }
            $(this).removeClass('active');
        }
    });
}

function display_sel_num() {
    var count = 0;
    $('.format_prod').each(function (i) {
        if ($(this).prop('checked') == true) {
            count += 1;
            $(this).parent().parent().parent().css('background-color', '#ccc');
        }
        else {
            $(this).parent().parent().parent().css('background-color', '#f5f5f5');
        }
    });
    $('#sel_num').text(count);
}





//<! DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
//"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
//<html xmlns="http://www.w3.org/1999/xhtml">
//<head>
//<title>拼音排序列表框</title>
//<script type="text/javascript">
//function s(n){
//  var o=document.getElementById(n);
//  if (!o) return ;
//  var t=[],tt=o.options;
//  while(tt.length>0){
//  t[t.length]=tt[0].text;
//  tt.remove(0);
// }
// t.sort();
//  for(var i=0,c;c=t[i];i++){
//  tt.add(new Option(c));
// }
//}
//</script>
//</head>
//<body onload="s('abc')">
//<select id="abc">
//<option>Firewall</option>
//<option>Alcohol 120%</option>
//<option>AMD</option>
//<option>baidu.com</option>
//<option>BlackIce</option>
//<option>BlueTooth</option>
//<option>Cisco </option>
//<option>千千静听</option>
//<option>DAEMON Tools</option>
//<option>瑞星(Rising)</option>
//<option>Editplus</option>
//<option>EmEditor</option>
//<option>eMule</option>
//<option>Google</option>
//<option>ICQ</option>
//<option>北京欢迎您</option>
//<option>微软</option>
//<option>木马克星(iparmor)</option>
//<option>天网防火墙</option>
//<option>网页制作</option>
//<option>Microsoft AntiSpyware</option>
//<option>UltraISO</option>
//<option>Winamp</option>
//<option>Zonealarm</option>
//</select>
//</body>
//</html>
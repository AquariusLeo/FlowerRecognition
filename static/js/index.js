var tmpcas=document.getElementById('tempCanvas');
var tmpctx=tmpcas.getContext('2d');

//画板尺寸自适应
getViewPort();

//弹出框水平垂直居中  
(window.onresize = function() {  
    var win_height = $(window).height();  
    var win_width = $(window).width();  
    if (win_width <= 768) {  
        $(".tailoring-content").css(  
                {  
                    "top" : (win_height - $(".tailoring-content")  
                            .outerHeight()) / 2,  
                    "left" : 0  
                });  
    } else {  
        $(".tailoring-content").css(  
                {  
                    "top" : (win_height - $(".tailoring-content")  
                            .outerHeight()) / 2,  
                    "left" : (win_width - $(".tailoring-content")  
                            .outerWidth()) / 2  
                });  
    }  
})();  

// 选择文件触发事件  
function selectImg(file) {  
    //文件为空，返回  
    if (!file.files || !file.files[0]) {  
        return;  
    }  
    $(".tailoring-container").toggle();  //将之前隐藏的裁剪框显示出来
    var reader = new FileReader();  
    reader.onload = function(evt) {  
        var replaceSrc = evt.target.result;  
        // 更换cropper的图片  
        $('#tailoringImg').cropper('replace', replaceSrc, false);// 默认false，适应高度，不失真  
    }  
    reader.readAsDataURL(file.files[0]);  
}  
// cropper图片裁剪  
$('#tailoringImg').cropper({  
    aspectRatio : 1 / 1,// 默认比例  
    preview : '.previewImg',// 预览视图  
    guides : false, // 裁剪框的虚线(九宫格)  
    autoCropArea : 0.5, // 0-1之间的数值，定义自动剪裁区域的大小，默认0.8  
    movable : false, // 是否允许移动图片  
    dragCrop : true, // 是否允许移除当前的剪裁框，并通过拖动来新建一个剪裁框区域  
    movable : true, // 是否允许移动剪裁框  
    resizable : true, // 是否允许改变裁剪框的大小  
    zoomable : false, // 是否允许缩放图片大小  
    mouseWheelZoom : false, // 是否允许通过鼠标滚轮来缩放图片  
    touchDragZoom : true, // 是否允许通过触摸移动来缩放图片  
    rotatable : true, // 是否允许旋转图片  
    crop : function(e) {  
        // 输出结果数据裁剪图像。  
    }  
});  
// 旋转  
$(".cropper-rotate-btn").on("click", function() {  
    $('#tailoringImg').cropper("rotate", 45);  
});  
// 复位  
$(".cropper-reset-btn").on("click", function() {  
    $('#tailoringImg').cropper("reset");  
});  
// 换向  
var flagX = true;  
$(".cropper-scaleX-btn").on("click", function() {  
    if (flagX) {  
        $('#tailoringImg').cropper("scaleX", -1);  
        flagX = false;  
    } else {  
        $('#tailoringImg').cropper("scaleX", 1);  
        flagX = true;  
    }  
    flagX != flagX;  
});  

// 确定按钮点击事件  
$("#sureCut").on("click", function() {  
    if ($("#tailoringImg").attr("src") == null) {  
        return false;  
    } else {  
        $('#result').html("识别中，请稍后...");
        var cas = $('#tailoringImg').cropper('getCroppedCanvas');// 获取被裁剪后的canvas  
        //放入299*299的临时canvas中
        var ctx=cas.getContext('2d');
        tmpcas.width=299;
        tmpcas.height=299;
        var imgdata=ctx.getImageData(0, 0, cas.width, cas.height);
        imgdata=scaleImageData(imgdata, 299/cas.width);
        tmpctx.putImageData(imgdata, 0, 0);

        var base64 = tmpcas.toDataURL('image/jpeg'); // 转换为base64  

        $("#finalImg").prop("src", base64);// 显示图片  
        uploadFile(base64);//编码后上传服务器  
        closeTailor();// 关闭裁剪框  
    }  
});  

//=======================内部函数========================
// 关闭裁剪框  
function closeTailor() {  
    $(".tailoring-container").toggle();  
}  

//ajax请求上传  
function uploadFile(file) {  
    $.ajax({  
        url : '/ajax',  
        type : 'POST',  
        data : {myphoto:file},  
        async : true,  
        success:function(data){     //请求成功后的回调函数，data为服务器返回的数据
            var obj=jQuery.parseJSON(data);
            alert("识别成功！\n结果： "+obj.result);
            $('#result').html(obj.result);  //显示结果
        },
        error:function(){
            console.log("上传失败");
        }  
    });  
}  

//画板尺寸自适应
function getViewPort(){
    if (isMobile()){
        $(".showImg").css({width:"90%", height:"400px"})
    }
    else{
        $(".showImg").css({width:"300px", height:"300px"})
    }
}

//ImageData对象缩放
function scaleImageData(imageData, scale) {
    var scaled = tmpctx.createImageData(imageData.width * scale, imageData.height * scale);
    for (var row = 0; row < imageData.height; row++) {
        for (var col = 0; col < imageData.width; col++) {
            var sourcePixel = [
                imageData.data[(row * imageData.width + col) * 4 + 0],
                imageData.data[(row * imageData.width + col) * 4 + 1],
                imageData.data[(row * imageData.width + col) * 4 + 2],
                imageData.data[(row * imageData.width + col) * 4 + 3]
            ];
            for (var y = 0; y < scale; y++) {
                var destRow = Math.floor(row * scale) + y;
                for (var x = 0; x < scale; x++) {
                    var destCol = Math.floor(col * scale) + x;
                    for (var i = 0; i < 4; i++) {
                        scaled.data[(destRow * scaled.width + destCol) * 4 + i] = sourcePixel[i];
                    }
                }
            }
        }
    }
    return scaled;
}

//判断PC端还是移动端
function isMobile() {
    var userAgentInfo = navigator.userAgent;
    var Agents = ["Android", "iPhone","SymbianOS", "Windows Phone","iPad", "iPod"];
    var flag = false;
    for (var v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
            flag = true;
            break;
        }
    }
    return flag;
}
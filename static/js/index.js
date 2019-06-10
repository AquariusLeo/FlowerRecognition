var takePhoto=document.getElementById('takePhoto');

//上传函数
function uploadPhoto(base64){
    $.ajax({
        url:"/ajax",
        type:"post",
        data:{myphoto:base64},
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

//读取拍摄的图片在canvas上显示并上传
function drawOnCanvas(file){
    var reader=new FileReader();
    reader.onload=function(e){  //reader加载成功的回调函数
        var dataURL=e.target.result,
            canvas=document.getElementById('myCanvas'),
            ctx=canvas.getContext('2d'),
            img=new Image();
        img.onload=function(){  //img加载成功的回调函数
            var length=299;
            canvas.width=length;
            canvas.height=length;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, canvas.width, canvas.height); //缩放至299*299的画板
            var base64=canvas.toDataURL('image/jpeg', 1);   //获取base64编码

            uploadPhoto(base64);    //上传base64编码
        }
        img.src=dataURL;
    }
    reader.readAsDataURL(file);
}

//takePhoto输入文件变化时的调用函数
takePhoto.onchange=function(){
    $('#result').html("识别中，请稍后...");
    var file=takePhoto.files[0];
    drawOnCanvas(file);
}
var dicImg = new Array();	//图片字典
$(function(){
	// 鼠标经过显示删除按钮
	$('.content-img-list').on('mouseover','.content-img-list-item',function(){
		$(this).children('a').removeClass('hide');
	});
	// 鼠标离开隐藏删除按钮
	$('.content-img-list').on('mouseleave','.content-img-list-item',function(){
		$(this).children('a').addClass('hide');
	});
	// 单个图片删除
	$(".content-img-list").on("click", '.content-img-list-item a', function () {
		var parentID = $(this).parent().parent().attr("id");
		var indImg = $(this).attr("index");

		checkImgDict(parentID);
		dicImg[parentID].splice(indImg, 1);

		// 图片展示更新
		addNewContent(parentID);
	  });
	// 提交请求
	$('#btn-submit-upload').on('click', function() {
		// FormData上传图片
		var formFile = new FormData();
		// formFile.append("type", type); 
		// formFile.append("content", content); 
		// formFile.append("mobile", mobile); 
		// 遍历图片imgFile添加到formFile里面
		$.each(imgFile, function (i, file) {
			formFile.append('myFile', file);
		});

		//图片上传
		//urlImg = uploadImg('myFile', imgFile[0]);
		//alert(urlImg);
    })
});

// 图片上传-事件实现
function event_uploadImg(objFile) {
	//图片上传，及信息记录
	var obj = "#" + objFile.id;
	var numImg = $(obj).parent().parent().attr("maxImg");
	var parentID = $(obj).attr("img-list-id");

	checkImgDict(parentID);
	imgSrc = dicImg[parentID];
	if (imgSrc.length >= numImg) {
		return alert("最多只能上传4张图片");
	}

	var fileList = objFile.files;
	var imgSize = fileList[0].size;
	var fileSize = $(obj).parent().parent().attr("fileSize");
	var fileSize_Max = 1024 * 1024 * fileSize;
	if (fileSize_Max < imgSize) {				//content-img下fileSize设置
		return alert("上传图片不能超过1M");
	}
	console.log(fileList[0].type)
	if (fileList[0].type != 'image/png' && fileList[0].type != 'image/jpeg' && fileList[0].type != 'image/gif') {
		return alert("图片上传格式不正确");
	}

	//图片上传，及信息记录
	for (var i = 0; i < fileList.length; i++) {
		var imgSrcI = getObjectURL(fileList[i]);
		dicImg[parentID].push(imgSrcI);
	}

	// 图片展示更新
	addNewContent(parentID);
	$(obj).value = null;			//解决无法上传相同图片的问题
}
//图片上传
function uploadImg(fileTag, file) {
	var data = new FormData();
	data.append(fileTag, file);

	urlImg = '';
	$.ajax({
		url: '/img_upload/' + fileTag,
		type: 'POST',
		data: data,
		async: false,
		cache: false,
		contentType: false,
		processData: false,
		// traditional:true,
		dataType: 'json',
		success: function (res) {
			console.log(res);
			if (res.status) {
				urlImg = res.filePath + "/" + res.fileName
				console.log('upload success');
			} else {
				console.log(res.msg);
			}
		},
		error: function (res) {
			console.log(res.status);
		}
	});
	return urlImg;
}
//图片展示
function addNewContent(tagID) {
	var obj = "#" + tagID;
	imgSrc = dicImg[tagID];

	$(obj).html("");
	for (var a = 0; a < imgSrc.length; a++) {
		var oldBox = $(obj).html();
		$(obj).html(oldBox + '<li class="content-img-list-item"><img src="' + imgSrc[a] + '" alt=""><a index="' + a + '" class="hide delete-btn"><i class="ico-delete"></i></a></li>');
	}

	//显隐上传按钮
	var numImg = $(obj).parent().attr("maxImg");
	if (imgSrc.length < numImg) {
		$(obj).parent().children('.file').show();
	}
	else {
		$(obj).parent().children('.file').hide();
	}
}

// 检查初始img字典
function checkImgDict(imgTag) {
	if (dicImg.hasOwnProperty(imgTag)) {
		//alert("dicImg exist");
	}
	else {
		dicImg[imgTag] = [];
	}
}
//建立一個可存取到該file的url
function getObjectURL(file) {
	var url = null;

	//图片上传-提取URL时
	url = uploadImg('fileImg', file);
	if (url.length <= 1) {
		alert("图片上传失败");
	}

	if (window.createObjectURL!=undefined) { // basic
		//url = window.createObjectURL(file) ;
	} else if (window.URL!=undefined) { // mozilla(firefox)
		//url = window.URL.createObjectURL(file) ;
	} else if (window.webkitURL!=undefined) { // webkit or chrome
		//url = window.webkitURL.createObjectURL(file) ;
	}
	return url;
}

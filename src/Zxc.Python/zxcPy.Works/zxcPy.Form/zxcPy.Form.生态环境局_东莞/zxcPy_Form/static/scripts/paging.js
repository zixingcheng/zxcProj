var tableStyle =
    ".page {font-size: 14px;background-color: transparent;width: 100%;height: 50px;line-height: 50px;display: none;}" +
    ".page .page-l select {width: 60px;height: 30px;}" +
    ".page .page-l .page-size-box {display: inline-block;margin-left: 20px;}" +
    ".page .page-r {float: right;padding-top: 10px;}" +
    ".page .page-r ul {float: left;list-style: none;margin: 0;height: 30px;box-sizing: border-box;padding: 0;}" +
    ".page .page-r ul li {float: left;list-style: none;height: 100%;line-height: 30px;border: 1px solid #ccc;border-right: 0 none;box-sizing: border-box;}" +
    ".page .page-r ul li a:hover {background-color: #f5f2f2;}" +
    ".page .page-r ul li:last-child {border-right: 1px solid #ccc;}" +
    ".page .page-r ul li a {text-decoration: none;display: block;height: 100%;padding:0 10px; color: #777;}" +
    ".page .page-r ul li a.active {background-color: #09aeb0;color: #fff;}" +
    ".page .page-r ul li span {display: block;height: 100%;padding:0 10px;color: #ccc;cursor: not-allowed;}" +
    ".page .page-r ul li span.ellipsis {cursor: default;}";

var styleNode = document.createElement('style');
styleNode.innerHTML = tableStyle;
var headNode = document.getElementsByTagName('head')[0];
headNode.appendChild(styleNode);

function Paging(paramsObj, callback) {
    this.pageSize = paramsObj.pageSize || 10;       //每页条数（不设置时，默认为10
    this.pageIndex = paramsObj.pageIndex || 1;      //当前页码
    this.totalCount = paramsObj.totalCount || 0;    //总记录数
    this.totalPage = Math.ceil(paramsObj.totalCount / paramsObj.pageSize) || 0;     //总页数
    this.prevPage = paramsObj.prevPage || '<';      //上一页（不设置时，默认为：<）
    this.nextPage = paramsObj.nextPage || '>';      //下一页（不设置时，默认为：>）
    this.firstPage = paramsObj.firstPage || '<<';   //首页（不设置时，默认为：<<）
    this.lastPage = paramsObj.lastPage || '>>';     //末页（不设置时，默认为：>>）
    this.degeCount = paramsObj.degeCount || 3;      //当前页前后两边可显示的页码个数（不设置时，默认为3）
    this.ellipsis = paramsObj.ellipsis;             //是否显示省略号不可点击按钮（true：显示，false：不显示）
    this.ellipsisBtn = (paramsObj.ellipsis == true || paramsObj.ellipsis == null) ? '<li><span class="ellipsis">…</span></li>' : '';
    var that = this;

    $('#page_size').val(this.pageSize);
    callback && callback(this.pageIndex, this.pageSize);    //立即执行回调函数

    // 生成分页DOM结构
    this.initPage = function (totalCount, totalPage, pageIndex) {
        this.totalCount = totalCount;
        this.totalPage = totalPage;
        this.pageIndex = pageIndex;
        var degeCount = this.degeCount;
        var pageHtml = '';          //总的DOM结构
        var tmpHtmlPrev = '';       //省略号按钮前面的DOM
        var tmpHtmlNext = '';       //省略号按钮后面的DOM
        var headHtml = '';          //首页和上一页按钮的DOM
        var endHtml = '';           //末页和下一页按钮的DOM
        if (pageIndex - degeCount >= degeCount - 1 && totalPage - pageIndex >= degeCount + 1) {         //前后都需要省略号按钮
            headHtml = '<li><a id="first_page" href="javascript:;">' + this.firstPage + '</a></li>' +
                '<li><a id="prev_page" href="javascript:;">' + this.prevPage + '</a></li>';

            endHtml = '<li><a id="next_page" href="javascript:;">' + this.nextPage + '</a></li>' +
                '<li><a id="last_page" href="javascript:;">' + this.lastPage + '</a></li>';

            var count = degeCount;  //前后各自需要显示的页码个数
            for (var i = 0; i < count; i++) {
                if (pageIndex != 1) {
                    tmpHtmlPrev += '<li><a href="javascript:;" class="page-number">' + (pageIndex - (count - i)) + '</a></li>';
                }
                tmpHtmlNext += '<li><a href="javascript:;" class="page-number">' + ((pageIndex - 0) + i + 1) + '</a></li>';
            }
            pageHtml = headHtml +
                this.ellipsisBtn +
                tmpHtmlPrev +
                '<li><a href="javascript:;" class="active">' + pageIndex + '</a></li>' +
                tmpHtmlNext +
                this.ellipsisBtn +
                endHtml;
        } else if (pageIndex - degeCount >= degeCount - 1 && totalPage - pageIndex < degeCount + 1) { //前面需要省略号按钮，后面不需要
            headHtml = '<li><a id="first_page" href="javascript:;">' + this.firstPage + '</a></li>' +
                '<li><a id="prev_page" href="javascript:;">' + this.prevPage + '</a></li>';

            if (pageIndex == totalPage) {   //如果当前页就是最后一页
                endHtml = '<li><span id="next_page" href="javascript:;">' + this.nextPage + '</span></li>' +
                    '<li><span id="last_page" href="javascript:;">' + this.lastPage + '</span></li>';
            } else {                        //当前页不是最后一页
                endHtml = '<li><a id="next_page" href="javascript:;">' + this.nextPage + '</a></li>' +
                    '<li><a id="last_page" href="javascript:;">' + this.lastPage + '</a></li>';
            }

            var count = degeCount;                  //前需要显示的页码个数
            var countNext = totalPage - pageIndex;  //后需要显示的页码个数
            if (pageIndex != 1) {
                for (var i = 0; i < count; i++) {
                    tmpHtmlPrev += '<li><a href="javascript:;" class="page-number">' + (pageIndex - (count - i)) + '</a></li>';
                }
            }
            for (var i = 0; i < countNext; i++) {
                tmpHtmlNext += '<li><a href="javascript:;" class="page-number">' + ((pageIndex - 0) + i + 1) + '</a></li>';
            }
            pageHtml = headHtml +
                this.ellipsisBtn +
                tmpHtmlPrev +
                '<li><a href="javascript:;" class="active">' + pageIndex + '</a></li>' +
                tmpHtmlNext +
                endHtml;
        } else if (pageIndex - degeCount < degeCount - 1 && totalPage - pageIndex >= degeCount + 1) { //前面不需要，后面需要省略号按钮
            if (pageIndex == 1) {           //如果当前页就是第一页
                headHtml = '<li><span id="first_page" href="javascript:;">' + this.firstPage + '</span></li>' +
                    '<li><span id="prev_page" href="javascript:;">' + this.prevPage + '</span></li>';
            } else {                        //当前页不是第一页
                headHtml = '<li><a id="first_page" href="javascript:;">' + this.firstPage + '</a></li>' +
                    '<li><a id="prev_page" href="javascript:;">' + this.prevPage + '</a></li>';
            }

            endHtml = '<li><a id="next_page" href="javascript:;">' + this.nextPage + '</a></li>' +
                '<li><a id="last_page" href="javascript:;">' + this.lastPage + '</a></li>';

            var countPrev = pageIndex - 1;  //前需要显示的页码个数
            var count = degeCount;          //后需要显示的页码个数
            if (pageIndex != 1) {
                for (var i = 0; i < countPrev; i++) {
                    tmpHtmlPrev += '<li><a href="javascript:;" class="page-number">' + (pageIndex - (countPrev - i)) + '</a></li>';
                }
            }
            for (var i = 0; i < count; i++) {
                tmpHtmlNext += '<li><a href="javascript:;" class="page-number">' + ((pageIndex - 0) + i + 1) + '</a></li>';
            }
            pageHtml = headHtml +
                tmpHtmlPrev +
                '<li><a href="javascript:;" class="active">' + pageIndex + '</a></li>' +
                tmpHtmlNext +
                this.ellipsisBtn +
                endHtml;
        } else if (pageIndex - degeCount < degeCount - 1 && totalPage - pageIndex < degeCount + 1) {   //前后都不需要省略号按钮
            headHtml = '<li><a id="first_page" href="javascript:;">' + this.firstPage + '</a></li>' +
                '<li><a id="prev_page" href="javascript:;">' + this.prevPage + '</a></li>';
            endHtml = '<li><a id="next_page" href="javascript:;">' + this.nextPage + '</a></li>' +
                '<li><a id="last_page" href="javascript:;">' + this.lastPage + '</a></li>';

            if (totalPage == 1) {           //如果总页数就为1
                headHtml = '<li><span id="first_page" href="javascript:;">' + this.firstPage + '</span></li>' +
                    '<li><span id="prev_page" href="javascript:;">' + this.prevPage + '</span></li>';
                endHtml = '<li><span id="next_page" href="javascript:;">' + this.nextPage + '</span></li>' +
                    '<li><span id="last_page" href="javascript:;">' + this.lastPage + '</span></li>';
            } else {
                if (pageIndex == 1) {       //如果当前页就是第一页
                    headHtml = '<li><span id="first_page" href="javascript:;">' + this.firstPage + '</span></li>' +
                        '<li><span id="prev_page" href="javascript:;">' + this.prevPage + '</span></li>';
                    endHtml = '<li><a id="next_page" href="javascript:;">' + this.nextPage + '</a></li>' +
                        '<li><a id="last_page" href="javascript:;">' + this.lastPage + '</a></li>';
                } else if (pageIndex == totalPage) {    //如果当前页是最后一页
                    headHtml = '<li><a id="first_page" href="javascript:;">' + this.firstPage + '</a></li>' +
                        '<li><a id="prev_page" href="javascript:;">' + this.prevPage + '</a></li>';
                    endHtml = '<li><span id="next_page" href="javascript:;">' + this.nextPage + '</span></li>' +
                        '<li><span id="last_page" href="javascript:;">' + this.lastPage + '</span></li>';
                }
            }

            var countPrev = pageIndex - 1;              //前需要显示的页码个数
            var countNext = totalPage - pageIndex;      //后需要显示的页码个数
            if (pageIndex != 1) {
                for (var i = 0; i < countPrev; i++) {
                    tmpHtmlPrev += '<li><a href="javascript:;" class="page-number">' + (pageIndex - (countPrev - i)) + '</a></li>';
                }
            }
            for (var i = 0; i < countNext; i++) {
                tmpHtmlNext += '<li><a href="javascript:;" class="page-number">' + ((pageIndex - 0) + i + 1) + '</a></li>';
            }
            pageHtml = headHtml +
                tmpHtmlPrev +
                '<li><a href="javascript:;" class="active">' + pageIndex + '</a></li>' +
                tmpHtmlNext +
                endHtml;
        }
        $('#page_ul').html(pageHtml);
        $('#total_count').html(totalCount);
    };

    // 点击页码（首页、上一页、下一页、末页、数字页）
    $('#page_ul').on('click', 'a', function (e) {
        var _this = $(this);
        var idAttr = _this.attr('id');
        var className = _this.attr('class');
        if (idAttr == 'first_page') {           //如果是点击的首页
            that.pageIndex = 1;
        } else if (idAttr == 'prev_page') {     //如果点击的是上一页
            that.pageIndex = that.pageIndex == 1 ? that.pageIndex : that.pageIndex - 1;
        } else if (idAttr == 'next_page') {     //如果点击的是下一页
            that.pageIndex = that.pageIndex == that.totalPage ? that.pageIndex : parseInt(that.pageIndex) + 1;
        } else if (idAttr == 'last_page') {     //如果点击的是末页
            that.pageIndex = that.totalPage;
        } else if (className == 'page-number') {//如果点击的是数字页码
            that.pageIndex = _this.html();
        }
        callback && callback(that.pageIndex, that.pageSize);
    });

    // 改变每页条数
    $('#page_size').change(function () {
        var _this = $(this);
        that.pageIndex = paramsObj.pageIndex = 1;
        that.pageSize = paramsObj.pageSize = _this.val() - 0;
        callback && callback(that.pageIndex, that.pageSize);
    })
}
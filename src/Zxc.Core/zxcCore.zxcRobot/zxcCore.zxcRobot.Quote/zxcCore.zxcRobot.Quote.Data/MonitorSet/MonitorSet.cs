//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：MonitorSet_Spider --监测设置类--蜘蛛爬虫
// 创建标识：zxc   2021-06-20
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{

    /// <summary>监测设置类--蜘蛛爬虫
    /// </summary>
    public class MonitorSet : Data_Models
    {
        #region 属性及构造 

        /// <summary>爬虫设置名称
        /// </summary>
        public string SpiderName
        {
            get; set;
        }
        /// <summary>爬虫设置规则
        /// </summary>
        public string SpiderRule
        {
            get; set;
        }
        /// <summary>爬虫设置分类
        /// </summary>
        public string SpiderTag
        {
            get; set;
        }
        /// <summary>爬虫设置Url
        /// </summary>
        public string SpiderUrl
        {
            get; set;
        }

        /// <summary>爬虫设置Url
        /// </summary>
        public string TimeSet
        {
            get; set;
        }
        public string Mark
        {
            get; set;
        }

        /// <summary>是否有效
        /// </summary>
        public bool IsValid
        {
            get; set;
        }

        public MonitorSet()
        {

        }
        ~MonitorSet()
        {
            // 缓存数据？
        }

        #endregion


        //对象转换-由json对象
        public new bool FromJson(dynamic jsonData)
        {
            this.SpiderName = jsonData["spiderName"] + "";
            this.SpiderRule = jsonData["spiderRule"] + "";
            this.SpiderTag = jsonData["spiderTag"] + "";
            this.SpiderUrl = jsonData["spiderUrl"] + "";

            this.TimeSet = jsonData["timeSet"] + "";
            this.Mark = jsonData["mark"] + "";

            this.IsValid = zxcTransHelper.ToBoolean(jsonData["isValid"]);
            return true;
        }

        //转换为Json字符串
        public virtual string ToJson_Str()
        {
            var msgWx = new
            {
                spiderName = this.SpiderName,
                spiderRule = this.SpiderRule,
                spiderTag = this.SpiderTag,
                spiderUrl = this.SpiderUrl,
                timeSet = this.TimeSet,
                mark = this.Mark,
                isValid = this.IsValid.ToString(),
                isDel = (!this.IsValid).ToString()
            };
            string jsonStr = JsonConvert.SerializeObject(msgWx);
            return jsonStr;
        }

    }

}

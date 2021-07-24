//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Word_Initial --汉字信息查询及初始类(百度)
// 创建标识：zxc   2021-07-24
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using HtmlAgilityPack;
using Newtonsoft.Json;
using zxcCore.Common;
using zxcCore.Extensions;

namespace zxcCore.zxcStudy.Word
{
    //汉字信息查询及初始类(百度)
    public class Word_Initial
    {
        /// <summary>全局行情查询对象
        /// </summary>
        public static readonly Word_Initial _APIs = new Word_Initial();

        #region 属性及构造

        protected internal string _apiToken = "";           //API接口-Tocken
        protected internal DateTime _apiToken_Time;         //API接口-Tocken时间

        protected internal string _urlAPI_Base = "";        //API接口-根
        protected internal string _urlAPI_Mob = "";         //API接口-用户名
        protected internal string _urlAPI_Pwd = "";         //API接口-密码
        protected internal int _urlAPI_QueryCount = 0;      //API接口-剩余查询条数
        protected internal string _verWord = "";            //API接口-Word版本号


        protected internal Dictionary<string, string> _mapFields = null;        //映射行情对象属性名字典
        protected internal Dictionary<string, string> _mapTypeTimes = null;     //映射行数数据时间类型字典
        public Word_Initial()
        {
            //提取行情API配置
            _urlAPI_Base = zxcConfigHelper.ConfigurationHelper.config["ZxcStudy:Word:WordQueryAPI_Url"] + "";
            _verWord = zxcConfigHelper.ConfigurationHelper.config["ZxcStudy:Word:Word_Version"] + "";

            this.Check_Token();     //初始平台Token
        }
        ~Word_Initial()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>校检平台Token(失效重新获取)
        /// </summary>
        /// <returns></returns>
        protected internal bool Check_Token()
        {
            //当天有效
            //if (string.IsNullOrEmpty(_apiToken) || (_apiToken_Time.Day - DateTime.Now.Day) > 0)
            //{
            //    //重新获取token
            //    _apiToken = this.Get_Token();
            //    if (string.IsNullOrEmpty(_apiToken))
            //        return false;
            //    _apiToken_Time = DateTime.Now;
            //    //_urlAPI_QueryCount = this.Get_QueryCount();
            //}
            return true;
        }
        /// <summary>获取平台Token
        /// </summary>
        /// <returns></returns>
        protected internal string Get_Token()
        {
            //生成JSON请求信息
            string jsonParam = JsonConvert.SerializeObject(new
            {
                method = "get_token",
                mob = _urlAPI_Mob,     //mob是申请JQData时所填写的手机号
                pwd = _urlAPI_Pwd      //Password为聚宽官网登录密码，新申请用户默认为手机号后6位
            });

            //POST请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Post_ByHttpClient(_urlAPI_Base, jsonParam, out statusCode);

            return result;
        }
        /// <summary>获取平台当前Token
        /// </summary>
        /// <returns></returns>
        protected internal string Get_Token_Current()
        {
            //生成JSON请求信息
            string jsonParam = JsonConvert.SerializeObject(new
            {
                method = "get_current_token",
                mob = _urlAPI_Mob,     //mob是申请JQData时所填写的手机号
                pwd = _urlAPI_Pwd      //Password为聚宽官网登录密码，新申请用户默认为手机号后6位
            });

            //POST请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Post_ByHttpClient(_urlAPI_Base, jsonParam, out statusCode);

            return result;
        }
        /// <summary>获取查询剩余条数
        /// </summary>
        /// <returns></returns>
        protected internal int Get_QueryCount()
        {
            //生成JSON请求信息
            if (!this.Check_Token()) return -1;
            string jsonParam = JsonConvert.SerializeObject(new
            {
                method = "get_query_count",
                token = _apiToken
            });

            //POST请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Post_ByHttpClient(_urlAPI_Base, jsonParam, out statusCode);

            return Convert.ToInt32(result);
        }


        /// <summary>提取指定汉字信息
        /// </summary>
        /// <param name="strWord">指定的汉字</param>
        /// <returns></returns>
        public bool Init_WordInfo(Word pWord)
        {
            //生成JSON请求信息
            if (!this.Check_Token()) return false;

            //POST请求并等待结果
            string strWord = pWord.WordStr;
            string statusCode = "";
            _urlAPI_Base = "https://hanyu.baidu.com/zici/s?wd=";
            var result = zxcNetHelper.Post_ByHttpClient(_urlAPI_Base, strWord, out statusCode, "text/html");
            if (statusCode.ToLower() != "ok") return false;

            //直接通过url加载
            var htmlDoc = new HtmlDocument();
            htmlDoc.LoadHtml(result);
            var nodeRoot = htmlDoc.DocumentNode;


            //解析百度汉字标识
            var nodeWordImg = nodeRoot.SelectNodes(".//div[@class='alter-text']");
            var strTag = nodeWordImg[0].Attributes["style"].Value;
            var ind0 = strTag.IndexOf("/u=") + 3;
            var ind2 = strTag.IndexOf("&fm");
            var wordTag = strTag.Substring(ind0, ind2 - ind0);
            var wordImg = string.Format("https://dss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u={0}&fm=58", wordTag);

            //解析笔画顺序
            var nodeWordImg_Stocks = nodeRoot.SelectNodes(".//img[@id='word_bishun']");
            var wordImgStocks = nodeWordImg_Stocks[0].Attributes["data-gif"].Value;


            //解析拼音及读音
            var nodeWordPinyin = nodeRoot.SelectNodes(".//div[@id='pinyin']");
            var nodePinyins = nodeWordPinyin.Descendants("span");
            Dictionary<string, string> dictPinyin = new Dictionary<string, string>();
            foreach (var item in nodePinyins)
            {
                string namePinyin = item.ChildNodes["b"].InnerText;
                string mp3Pinyin = item.ChildNodes["a"].Attributes["url"].Value;
                if (!string.IsNullOrEmpty(namePinyin + mp3Pinyin))
                    dictPinyin[namePinyin] = mp3Pinyin;
            }

            //解析部首及其他信息
            var wordRadical = nodeRoot.SelectNodes(".//li[@id='radical']/span")[0].InnerText;
            var wordStrokeNum = Convert.ToInt32(nodeRoot.SelectNodes(".//li[@id='stroke_count']/span")[0].InnerText);
            var wordWuXing = nodeRoot.SelectNodes(".//li[@id='wuxing']/span")[0].InnerText;


            //初始汉字信息 
            bool bResult = true;
            pWord.WordStr = strWord;
            pWord.WordRadical = wordRadical;
            pWord.WordStrokeNum = wordStrokeNum;
            pWord.WordWuXing = (typeWuXing)Enum.Parse(typeof(typeWuXing), wordWuXing);
            pWord.WordTag_bd = wordTag;
            pWord.VerTag = _verWord;
            bResult = bResult && pWord.Set_Font(typeFace.中宋体, wordImg, wordImgStocks);
            foreach (var item in dictPinyin)
            {
                bResult = bResult && pWord.Set_Pinyin(item.Key, item.Value);
            }
            bResult = bResult && pWord.Init_JsonFile();
            return bResult;
        }

    }
}

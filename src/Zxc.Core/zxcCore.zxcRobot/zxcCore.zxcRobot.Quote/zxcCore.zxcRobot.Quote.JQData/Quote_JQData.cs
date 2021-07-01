//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Quote_JQData --行情查询(聚宽)
// 创建标识：zxc   2021-06-26
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Text;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote.JQData
{
    public class Quote_JQData
    {
        /// <summary>全局行情查询对象
        /// </summary>
        public static readonly Quote_JQData _APIs = new Quote_JQData();

        #region 属性及构造

        protected internal string _jqQPI_Token = "";          //行情API接口-Tocken
        protected internal DateTime _jqQPI_Token_Time;        //行情API接口-Tocken时间

        protected internal string _urlAPI_Base = "";          //行情API接口-根
        protected internal string _urlAPI_Mob = "";           //行情API接口-用户名
        protected internal string _urlAPI_Pwd = "";           //行情API接口-密码
        protected internal int _urlAPI_QueryCount = 0;        //行情API接口-剩余查询条数


        protected internal Dictionary<string, string> _mapFields = null;        //映射行情对象属性名字典
        protected internal Dictionary<string, string> _mapTypeTimes = null;     //映射行数数据时间类型字典
        public Quote_JQData()
        {
            //提取行情API配置
            _urlAPI_Base = zxcConfigHelper.ConfigurationHelper.config["ZxcRobot.Quote:QuoteAPI_JQData:BaseAPI_Url"] + "";
            _urlAPI_Mob = "18002273029";
            _urlAPI_Pwd = "zxcvbnm.123";

            this.Check_Token();     //初始平台Token

            //初始行情对象属性名映射字典
            _mapFields = new Dictionary<string, string>()
            {
                {"date", "datetime" },
                {"open", "openPrice" },
                {"close", "lastPrice" },
                {"high", "highPrice" },
                {"low", "lowPrice" },
                {"volume", "tradeValume" },
                {"money", "tradeTurnover" },
                {"paused", "paused" },
                {"high_limit", "high_limit" },
                {"low_limit", "low_limit" },
                {"open_interest", "open_interest" },
                {"avg", "avg" },
                {"pre_close", "preClose" }
            };
            _mapTypeTimes = new Dictionary<string, string>()
            {
                {"1m", "m1" },
                {"5m", "m5" },
                {"15m", "m15" },
                {"30m", "m30" },
                {"60m", "m60" },
                {"120m", "m120" },
                {"1d", "day" },
                {"1w", "week" },
                {"1M", "month" }
            };
        }
        ~Quote_JQData()
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
            if (string.IsNullOrEmpty(_jqQPI_Token) || (_jqQPI_Token_Time.Day - DateTime.Now.Day) > 0)
            {
                //重新获取token
                _jqQPI_Token = this.Get_Token();
                if (string.IsNullOrEmpty(_jqQPI_Token))
                    return false;
                _jqQPI_Token_Time = DateTime.Now;
                _urlAPI_QueryCount = this.Get_QueryCount();
            }
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
                token = _jqQPI_Token
            });

            //POST请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Post_ByHttpClient(_urlAPI_Base, jsonParam, out statusCode);

            return Convert.ToInt32(result);
        }



        /// <summary>获取指定时间周期的行情数据
        /// </summary>
        /// <param name="codeTag">证券代码</param>
        /// <param name="endTime">查询的截止时间，默认是今天</param>
        /// <param name="bars">大于0的整数，表示获取bar的条数，不能超过5000</param>
        /// <param name="barUnit">bar的时间单位, 支持如下周期：1m, 5m, 15m, 30m, 60m, 120m, 1d, 1w, 1M。其中m表示分钟，d表示天，w表示周，M表示月</param>
        /// <returns></returns>
        public JObject Get_Price(string codeTag, string endTime = "", int bars = 1, string barUnit = "1d", string fqrefTime = "")
        {
            //生成JSON请求信息
            if (!this.Check_Token()) return null;
            string jsonParam = JsonConvert.SerializeObject(new
            {
                method = "get_price",
                token = _jqQPI_Token,
                code = codeTag,
                count = bars,
                unit = barUnit,
                end_date = endTime.Length > 10 ? endTime.Substring(0, 10) : endTime,
                fq_ref_date = fqrefTime.Length > 10 ? fqrefTime.Substring(0, 10) : fqrefTime
            });

            //POST请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Post_ByHttpClient(_urlAPI_Base, jsonParam, out statusCode);

            if (statusCode.ToLower() != "ok") return null;
            return this.TransTo_JsonData(codeTag, result, barUnit);
        }
        /// <summary>获取指定时间周期的行情数据
        /// </summary>
        /// <param name="codeTag">证券代码</param>
        /// <param name="startTime">查询的截止时间，默认是今天</param>
        /// <param name="endTime">查询的截止时间，默认是今天</param>
        /// <param name="barUnit">bar的时间单位, 支持如下周期：1m, 5m, 15m, 30m, 60m, 120m, 1d, 1w, 1M。其中m表示分钟，d表示天，w表示周，M表示月</param>
        /// <returns></returns>
        public JObject Get_Price(string codeTag, DateTime startTime, DateTime endTime, string barUnit = "1d", string fqrefTime = "")
        {
            //生成JSON请求信息
            if (!this.Check_Token()) return null;
            string jsonParam = JsonConvert.SerializeObject(new
            {
                method = "get_price_period",
                token = _jqQPI_Token,
                code = codeTag,
                unit = barUnit,
                date = startTime.ToString("yyyy-MM-dd HH:mm:ss"),
                end_date = endTime.ToString("yyyy-MM-dd HH:mm:ss"),
                fq_ref_date = fqrefTime.Length > 10 ? fqrefTime.Substring(0, 10) : fqrefTime
            });

            //POST请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Post_ByHttpClient(_urlAPI_Base, jsonParam, out statusCode);

            if (statusCode.ToLower() != "ok") return null;
            return this.TransTo_JsonData(codeTag, result, barUnit);
        }

        /// <summary>获取指定范围交易日
        /// </summary>
        /// <param name="startTime"></param>
        /// <param name="endTime"></param>
        /// <returns></returns>
        public string[] Get_TradeDays(DateTime startTime, DateTime endTime)
        {
            //生成JSON请求信息
            if (!this.Check_Token()) return null;
            string jsonParam = JsonConvert.SerializeObject(new
            {
                method = "get_trade_days",
                token = _jqQPI_Token,
                date = startTime.ToString("yyyy-MM-dd"),
                end_date = endTime.ToString("yyyy-MM-dd")
            });

            //POST请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Post_ByHttpClient(_urlAPI_Base, jsonParam, out statusCode);

            return result.Split("\n");
        }


        /// <summary>将行情数据转换为Json
        /// </summary>
        /// <param name="strData"></param>
        /// <param name="barUnit">bar的时间单位</param>
        /// <returns></returns>
        public JObject TransTo_JsonData(string codeTag, string strData, string barUnit = "1d")
        {
            JObject pRes = new JObject();
            JArray jsonDatas = new JArray();
            pRes.Add("result", true);
            pRes.Add("datasPlat", typeQuotePlat.JQDataAPI_zxc.ToString());
            pRes.Add("datas", jsonDatas);


            //映射接口字段到行情属性
            string[] strLines = strData.Split("\n");
            string[] strHeads = strLines[0].Split(",");
            for (int j = 0; j < strHeads.Length; j++)
            {
                strHeads[j] = _mapFields[strHeads[j]];
            }

            //修正行情时间，转换所有
            string strID = codeTag.Split(".")[0];
            string strTime_suffix = barUnit.Contains("m") ? ":00" : " 00:00:00";
            for (int i = 1; i < strLines.Length; i++)
            {
                string[] strTemps = strLines[i].Split(",");

                //生成数据对象
                JObject pObj = new JObject
                {
                    { "id", strID },
                    { strHeads[0], strTemps[0] + strTime_suffix },   //时间字符串格式修正
                    { "quoteTimeType", _mapTypeTimes[barUnit] },
                    { "quotePlat", typeQuotePlat.JQDataAPI_zxc.ToString()}
                };
                for (int j = 1; j < strHeads.Length; j++)
                {
                    pObj.Add(strHeads[j], strTemps[j]);
                }
                jsonDatas.Add(pObj);
            }
            return pRes;
        }

    }
}

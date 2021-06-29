using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据检查-行情基类
    /// </summary>
    public class DataCheck_Quote<T> : DataCheck<T>
    {
        #region 属性及构造

        protected internal bool _isValid = true;
        public bool IsValid
        {
            get { return _isValid; }
            set { _isValid = value; }
        }

        protected internal JObject _setObj = null;
        protected internal Data_Quote_Swap _data = null;
        public DataCheck_Quote(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache)
        {
            this.InitSetting(setting);
        }
        ~DataCheck_Quote()
        {
            // 缓存数据？
            _data = null;
        }

        #endregion


        //初始配置参数
        public override bool InitSetting(dynamic setting)
        {
            if (setting.GetType() == typeof(string))
            {
                if (setting + "" == "") return false;
                this._setObj = JObject.Parse(setting);
            }
            return true;
        }

        //数据检查处理-使用基类
        public override bool CheckData()
        {
            return true;
        }
        //数据检查实现（具化数据对象及缓存）-使用基类
        public override bool CheckData(DateTime dtTime, T data, IDataCache<T> dataCache = null)
        {
            if (dataCache != null) this._DataCache = dataCache;
            _data = (Data_Quote_Swap)Convert.ChangeType(data, typeof(Data_Quote_Swap));
            return true;
        }


        //消息通知
        public override bool NotifyMsg(dynamic msg, string userID_To)
        {
            if (this.Msger != null)
            {
                var pMsg = this.getMsg(msg, userID_To);
                if (pMsg != null)
                    this.Msger.NotifyMsg(pMsg);
            }
            return true;
        }


        //提取返回消息
        protected internal virtual Msg getMsg(string msg, string userID_To = "@*测试群")
        {
            if (msg + "" == "") return null;
            if (userID_To + "" == "") return null;

            //组装消息
            Msg pMsg = new Msg()
            {
                msgID = "",
                msg = msg + "",
                msgType = typeMsg.TEXT,
                msgLink = "",
                usrNameNick = userID_To,
                usrPlat = typeMsger.wx,
                UserName_src = "System",
                msgTime = DateTime.Now,
                IsSend = true
            };
            return pMsg;
        }
        //提取返回消息-前缀
        protected internal virtual string getMsg_Perfix()
        {
            //组装消息
            string tagRF = _data.Value_RF == 0 ? "平" : (_data.Value_RF > 0 ? "涨" : "跌");
            string tagUnit = _data.IsIndex() ? "" : "元";
            int digits = _data.IsIndex() ? 3 : 2;
            string msg = string.Format("{0}：{1}{2}, {3} {4}%.", _data.StockName, Math.Round(_data.Value, digits), tagUnit, tagRF, Math.Round(_data.Value_RF * 100, 2));
            return msg;
        }
        //提取返回消息-中缀
        protected internal virtual string getMsg_Infix()
        {
            return "";
        }
        //提取返回消息-后缀
        protected internal virtual string getMsg_Suffix()
        {
            return string.Format("\n--zxcRobot(Stock) {0}", DateTime.Now.ToString("HH:mm:ss"));
        }

        //数据分析触发事件
        protected internal virtual string getUser_str()
        {
            string usrTo = _data.StockType == typeStock.Option ? "期权行情" : _data.IsIndex() ? "大盘行情" : "自选行情";
            usrTo = "@*股票监测--" + usrTo;
            return usrTo;
        }

        /// <summary>提取值字符串（含单位，指数没有单位）
        /// </summary>
        /// <returns></returns>
        protected internal virtual string getValue_str(double dValue)
        {
            //组装消息
            string tagUnit = _data.IsIndex() ? "" : "元";
            int digits = _data.IsIndex() ? 3 : 2;
            string strValue = string.Format("{0}{1}", Math.Round(dValue, digits), tagUnit);
            return strValue;
        }

    }
}

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Xml.Linq;
using zxcCore.Common;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息类
    /// </summary>
    public class Msg : Data_Models, IMsg
    {
        #region 属性及构造

        /// <summary>来源用户ID
        /// </summary>
        public string usrID
        {
            get; set;
        }
        /// <summary>群组ID
        /// </summary>
        public string groupID
        {
            get; set;
        }
        /// <summary>来源用户名
        /// </summary>
        public string usrName
        {
            get; set;
        }
        /// <summary>来源用户别名
        /// </summary>
        public string usrNameNick
        {
            get; set;
        }
        /// <summary>用户平台
        /// </summary>
        public typeMsger usrPlat
        {
            get; set;
        }


        /// <summary>消息ID
        /// </summary>
        public string msgID
        {
            get; set;
        }
        /// <summary>消息类型
        /// </summary>
        public typeMsg msgType
        {
            get; set;
        }
        /// <summary>消息内容
        /// </summary>
        public string msg
        {
            get; set;
        }
        /// <summary>消息内容-完整
        /// </summary>
        public string msgContent
        {
            get; set;
        }
        /// <summary>消息链接
        /// </summary>
        public string msgLink
        {
            get; set;
        }

        /// <summary>消息时间
        /// </summary>
        public DateTime msgTime
        {
            get; set;
        }

        string _usrName_src = "";
        /// <summary>消息源用户
        /// </summary>
        public string UserName_src
        {
            get
            {
                if (string.IsNullOrEmpty(_usrName_src))
                {
                    if (!IsSend)
                        _usrName_src = string.IsNullOrEmpty(usrName) ? usrNameNick : usrName;
                }
                return _usrName_src;
            }
            set
            {
                _usrName_src = value;
            }
        }
        bool _IsUserGroup = false;
        /// <summary>目标用户是否为群组
        /// </summary>
        public bool IsUserGroup
        {
            get
            {
                if (string.IsNullOrEmpty(usrName)) return false;
                if (string.IsNullOrEmpty(usrNameNick)) return false;
                _IsUserGroup = usrName.Substring(0, 2) == "@*" ? true : usrNameNick.Substring(0, 2) == "@*" ? true : (groupID != "" ? true : false);
                return _IsUserGroup;
            }
            set
            {
                _IsUserGroup = value;
            }
        }
        bool _IsFromRobot = false;
        /// <summary>是否来源于robot的自动消息
        /// </summary>
        public bool IsFromRobot
        {
            get
            {
                return _IsFromRobot;
            }
            set
            {
                _IsFromRobot = value;
            }
        }
        /// <summary>是否为发送消息（false为接收消息）
        /// </summary>
        public bool IsSend
        {
            get; set;
        }
        /// <summary>是否已经保存，记录日志
        /// </summary>
        public bool IsSaved
        {
            get; set;
        }

        public Msg()
        {
        }
        public Msg(string msg)
        {
            this.msg = msg;
        }
        ~Msg()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>提取群名称（没有返回""）
        /// </summary>
        /// <returns></returns>
        public virtual string GetNameGroup()
        {
            string nameGroup = this.IsUserGroup ? this.usrName : "";
            return nameGroup;
        }
        /// <summary>提取用户名称（没有返回""）
        /// </summary>
        /// <returns></returns>
        public virtual string GetNameUser()
        {
            string nameUser = "";
            if (this.IsUserGroup)
            {
                nameUser = this.usrNameNick;
            }
            else
            {
                nameUser = this.usrName;
                if (string.IsNullOrEmpty(nameUser))
                    nameUser = this.usrNameNick;
            }
            return nameUser;
        }

        /// <summary>提取XML内容
        /// </summary>
        /// <returns></returns>
        public virtual XElement GetMsg_ForXml()
        {
            if (this.msgContent.Contains("></"))
            {
                this.msgContent = this.msgContent.Replace("※i※", "\"");
                XElement pElemment = XElement.Parse(this.msgContent);
                return pElemment;
            }
            return null;
        }


        public virtual dynamic ToDict()
        {
            var msgWx = new
            {
                usrID = usrID,
                usrName = usrName,
                usrNameNick = usrNameNick,
                groupID = groupID,
                usrPlat = usrPlat,
                msgType = msgType,
                msg = msg,
                msgID = msgID,
                msgContent = msgContent,
                msgLink = msgLink,
                msgTime = msgTime,
            };
            return msgWx;
        }

        public override dynamic ToJson()
        {
            var result = JsonConvert.SerializeObject(this.ToDict());
            return result;
        }
        public override bool FromJson(dynamic jsonData)
        {
            if (jsonData == null) return false;
            JObject jMsg = null;

            Type typeMsg = jsonData.GetType();
            if (typeMsg.Name == "JObject")
                jMsg = (JObject)jsonData;
            else
            {
                jMsg = JsonConvert.DeserializeObject(jsonData + "");
            }

            //赋值
            usrID = Convert.ToString(jMsg["usrID"]);
            usrName = Convert.ToString(jMsg["usrName"]);
            usrNameNick = Convert.ToString(jMsg["usrNameNick"]);
            groupID = Convert.ToString(jMsg["groupID"]);
            usrPlat = (typeMsger)Enum.Parse(typeof(typeMsger), Convert.ToString(jMsg["usrPlat"]));
            msgType = (typeMsg)Enum.Parse(typeof(typeMsg), Convert.ToString(jMsg["msgType"]));
            msg = Convert.ToString(jMsg["msg"]);
            msgID = Convert.ToString(jMsg["msgID"]);
            msgContent = Convert.ToString(jMsg["msgContent"]);
            msgLink = Convert.ToString(jMsg["msgLink"]);
            msgTime = Convert.ToDateTime(jMsg["msgTime"]);
            return true;
        }

    }
}

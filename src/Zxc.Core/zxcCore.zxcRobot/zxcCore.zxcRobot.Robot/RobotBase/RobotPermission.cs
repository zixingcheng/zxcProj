﻿using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.Common;
using zxcCore.zxcDataCache.MemoryDB;
using zxcCore.zxcRobot.Monitor.Msg;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.Robot.Power;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>机器人-权限类
    /// </summary>
    public class RobotPermission
    {
        #region 属性及构造

        /// <summary>是否初始
        /// </summary>
        public bool IsInited
        {
            get; set;
        }
        /// <summary>是否运行中
        /// </summary>
        public bool IsRunning
        {
            get; set;
        }
        /// <summary>开始运行时间
        /// </summary>
        public DateTime TimeStartRun
        {
            get; set;
        }

        /// <summary>是否单一实例(所有用户共用)
        /// </summary>
        public bool IsSingleUse
        {
            get; set;
        }
        /// <summary>是否后台运行
        /// </summary>
        public bool IsBackProc
        {
            get; set;
        }
        protected internal int _ValidMaxTime = -1;
        /// <summary>有效时长(秒)，小于0则永久有效
        /// </summary>
        public int ValidMaxTime
        {
            set { _ValidMaxTime = value; }
            get { return _ValidMaxTime; }
        }


        /// <summary>是否有效
        /// </summary>
        public bool IsValid
        {
            get; set;
        }

        /// <summary>是否有效-群组
        /// </summary>
        public bool IsValid_Group
        {
            get; set;
        }
        /// <summary>是否有效-全部群组
        /// </summary>
        public bool IsValid_GroupAll
        {
            get; set;
        }
        /// <summary>是否有效-全部群组全部用户
        /// </summary>
        public bool IsValid_GroupAll_UserALL
        {
            get; set;
        }

        /// <summary>是否有效-个人私聊
        /// </summary>
        public bool IsValid_Personal
        {
            get; set;
        }
        /// <summary>是否有效-全部个人
        /// </summary>
        public bool IsValid_PersonalAll
        {
            get; set;
        }


        /// <summary>配置文件信息
        /// </summary>
        protected internal ConfigurationHelper _configDataCache = null;
        protected internal string _configPerFix = "";   //设置前缀
        protected internal string _configMidFix = "";   //设置中缀
        public RobotPermission(string configPerFix, string configMidFix, dynamic setting = null)
        {
            _configMidFix = configMidFix;
            _configPerFix = configPerFix;
            _configDataCache = new ConfigurationHelper("appsettings_" + configPerFix + ".json");
            this.InitSetting(setting);
            this.Init();
        }
        ~RobotPermission()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>初始配置信息
        /// </summary>
        /// <param name="setting"></param>
        /// <returns></returns>
        protected internal virtual bool InitSetting(dynamic setting)
        {
            return true;
        }
        protected internal virtual bool Init()
        {
            //实例生效->未初始？-> 默认配置生成（群组有效？、全部群组有效？、群组全员有效？、私聊有效？、私聊全员有效？） -> 已初始;
            if (this.IsInited) return true;

            string path = _configPerFix + ":" + _configMidFix;
            string title = _configDataCache.config[path + ":Title"] + "";
            if (title == "") return false;

            this.IsValid = Convert.ToBoolean(_configDataCache.config[path + ":IsValid"] + "");
            ValidMaxTime = Convert.ToInt32(_configDataCache.config[path + ":ValidMaxTime"] + "");

            this.IsSingleUse = Convert.ToBoolean(_configDataCache.config[path + ":IsSingleUse"] + "");
            this.IsBackProc = Convert.ToBoolean(_configDataCache.config[path + ":IsBackProc"] + "");

            this.IsValid_Group = Convert.ToBoolean(_configDataCache.config[path + ":IsValid_Group"] + "");
            this.IsValid_GroupAll = Convert.ToBoolean(_configDataCache.config[path + ":IsValid_GroupAll"] + "");
            this.IsValid_GroupAll_UserALL = Convert.ToBoolean(_configDataCache.config[path + ":IsValid_GroupAll_UserALL"] + "");

            this.IsValid_Personal = Convert.ToBoolean(_configDataCache.config[path + ":IsValid_Personal"] + "");
            this.IsValid_PersonalAll = Convert.ToBoolean(_configDataCache.config[path + ":IsValid_PersonalAll"] + "");

            //同步用户信息-群组
            string name = _configPerFix;
            int ind = 0;
            string IsValid_GroupName = _configDataCache.config[path + ":IsValid_GroupNames:" + ind.ToString() + ":nameGroup"] + "";
            while (IsValid_GroupName != "")
            {
                string nameUser = _configDataCache.config[path + ":IsValid_GroupNames:" + ind.ToString() + ":nameUser"] + "";
                string usrPlat = _configDataCache.config[path + ":IsValid_GroupNames:" + ind.ToString() + ":usrPlat"] + "";
                string strValid = _configDataCache.config[path + ":IsValid_GroupNames:" + ind.ToString() + ":isValid"] + "";
                string bindTag = _configDataCache.config[path + ":IsValid_GroupNames:" + ind.ToString() + ":bindTag"] + "";
                bool isValid = strValid == "" ? false : Convert.ToBoolean(strValid);
                this.Add_Permission(name, IsValid_GroupName, nameUser, usrPlat, isValid, bindTag);

                ind++;
                IsValid_GroupName = _configDataCache.config[path + ":IsValid_GroupNames:" + ind.ToString() + ":nameGroup"] + "";
            }

            //同步用户信息-个人
            ind = 0;
            string IsValid_PersonalName = _configDataCache.config[path + ":IsValid_PersonalNames:" + ind.ToString() + ":nameUser"] + "";
            while (IsValid_PersonalName != "")
            {
                string usrPlat = _configDataCache.config[path + ":IsValid_PersonalNames:" + ind.ToString() + ":usrPlat"] + "";
                string strValid = _configDataCache.config[path + ":IsValid_PersonalNames:" + ind.ToString() + ":isValid"] + "";
                string bindTag = _configDataCache.config[path + ":IsValid_PersonalNames:" + ind.ToString() + ":bindTag"] + "";
                bool isValid = strValid == "" ? false : Convert.ToBoolean(strValid);
                this.Add_Permission(name, "", IsValid_PersonalName, usrPlat, isValid, bindTag);

                ind++;
                IsValid_PersonalName = _configDataCache.config[path + ":IsValid_PersonalNames:" + ind.ToString() + ":nameUser"] + "";
            }
            this.IsInited = true;
            return true;
        }


        /// <summary>权限检查
        /// </summary>
        /// <returns></returns>
        public virtual bool Check_Permission(string nameGroup, string usrID, string usrPlat)
        {
            bool isValid = false;
            if (this.IsRunning && this.IsValid)
            {
                //超时检查
                if (this.ValidMaxTime > 0)
                {
                    var deltaT = (DateTime.Now - TimeStartRun).TotalSeconds;
                    if (deltaT > _ValidMaxTime)
                    {
                        isValid = false; return isValid;
                    }
                }

                //群权限检查
                if (this.IsValid_Group && !string.IsNullOrEmpty(nameGroup))
                {
                    if (this.IsValid_GroupAll)
                    {
                        if (this.IsValid_GroupAll_UserALL) return true;     //全部群、全部人员有效

                        //查询群组信息--通用(指定群、指定人员)
                        Power_Robot pPower = Robot_Manager._dbRobot._powerRobot.Find(e => e.NameRobot == _configPerFix && (e.NameGroup == nameGroup || e.NameGroup == "@*" + nameGroup) && (e.NameUser == usrID || e.NameUser == "") && e.UsrPlat == usrPlat && e.IsDel == false);
                        if (pPower != null && pPower.IsValid)
                        {
                            return true;                                    //指定群、指定人员有效
                        }
                    }
                    else
                    {
                        //查询群组信息--通用(指定群)
                        List<Power_Robot> lstPower = Robot_Manager._dbRobot._powerRobot.FindAll(e => e.NameRobot == _configPerFix && (e.NameGroup == nameGroup || e.NameGroup == "@*" + nameGroup) && e.UsrPlat == usrPlat && e.IsDel == false);
                        if (lstPower.Count > 0)
                        {
                            if (this.IsValid_GroupAll_UserALL) return true;     //全部群、全部人员有效

                            Power_Robot pPower = lstPower.Find(e => e.NameUser == usrID || e.NameUser == "");
                            if (pPower != null && pPower.IsValid) return true;  //指定群、指定人员有效
                        }
                        else
                            return false;                                       //群无效             
                    }
                }

                //个人权限检查
                if (this.IsValid_Personal && string.IsNullOrEmpty(nameGroup))
                {
                    if (this.IsValid_PersonalAll) return true;          //全部人有权限

                    //查询个人信息--通用(指定群、指定人员)
                    Power_Robot pPower = Robot_Manager._dbRobot._powerRobot.Find(e => e.NameRobot == _configPerFix && (e.NameGroup == "" || e.NameGroup == null) && (e.NameUser == usrID || e.NameUser == "") && e.UsrPlat == usrPlat && e.IsDel == false);
                    if (pPower != null && pPower.IsValid)
                    {
                        return true;                                    //指指定人员有效
                    }
                }

                //查询用户信息--特定
                isValid = Check_Permission_SysUsr(usrID, usrPlat);
            }
            return isValid;
        }
        /// <summary>权限检查-单一设置
        /// </summary> 
        /// <returns></returns>
        public virtual bool Check_Permission_SingleSet(string nameGroup, string usrID, string usrPlat)
        {
            bool isValid = false;
            if (this.IsRunning && this.IsValid)
            {
                //超时检查
                if (this.ValidMaxTime > 0)
                {
                    var deltaT = (DateTime.Now - TimeStartRun).TotalSeconds;
                    if (deltaT > _ValidMaxTime)
                    {
                        isValid = false; return isValid;
                    }
                }

                //群权限检查
                if (this.IsValid_Group && !string.IsNullOrEmpty(nameGroup))
                {
                    //查询群组信息--通用(指定群、指定人员)
                    Power_Robot pPower = Robot_Manager._dbRobot._powerRobot.Find(e => e.NameRobot == _configPerFix && (e.NameGroup == nameGroup || e.NameGroup == "@*" + nameGroup) && (e.NameUser == usrID || e.NameUser == "") && e.UsrPlat == usrPlat && e.IsDel == false);
                    if (pPower != null && pPower.IsValid)
                    {
                        return true;                                    //指定群、指定人员有效
                    }
                }

                //个人权限检查
                if (this.IsValid_Personal && string.IsNullOrEmpty(nameGroup))
                {
                    //查询个人信息--通用(指定群、指定人员)
                    Power_Robot pPower = Robot_Manager._dbRobot._powerRobot.Find(e => e.NameRobot == _configPerFix && (e.NameGroup == "" || e.NameGroup == null) && (e.NameUser == usrID || e.NameUser == "") && e.UsrPlat == usrPlat && e.IsDel == false);
                    if (pPower != null && pPower.IsValid)
                    {
                        return true;                                    //指指定人员有效
                    }
                }

                //查询用户信息--特定
                isValid = Check_Permission_SysUsr(usrID, usrPlat);
            }
            return isValid;
        }
        /// <summary>权限检查--系统管理员（特例）
        /// </summary>
        /// <returns></returns>
        public virtual bool Check_Permission_SysUsr(string usrID, string usrPlat)
        {
            //查询用户信息--特定
            if (string.IsNullOrEmpty(usrID) || usrPlat == "None")
                return false;

            User_zxc usr = UserManager._Users.GetUser(usrID, usrID, usrPlat);
            if (usr != null)
            {
                if (usr.usrType == typeUser.sysadmin)
                    return true;                                //系统管理员有效
            }
            return false;
        }

        /// <summary>权限新增
        /// </summary>
        /// <returns></returns>
        public virtual bool Add_Permission(string nameRobot, string nameGroup, string usrID, string usrPlat, bool isValid, string bindTag)
        {
            Power_Robot pPowerInfo = new Power_Robot()
            {
                NameRobot = nameRobot,
                NameUser = usrID,
                NameGroup = nameGroup,
                UsrPlat = usrPlat,
                IsValid = isValid,
                BindTag = bindTag
            };
            Robot_Manager._dbRobot._powerRobot.Add(pPowerInfo);
            return true;
        }
        /// <summary>权限删除
        /// </summary>
        /// <returns></returns>
        public virtual bool Del_Permission(string usrID, bool isGroup = false)
        {
            return true;
        }
        /// <summary>权限查询
        /// </summary>
        /// <returns></returns>
        public virtual bool Get_Permission()
        {
            return true;
        }

    }
}

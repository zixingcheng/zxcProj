﻿using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcData.Cache.Swap;

namespace zxcCore.zxcRobot.Monitor.Msg
{
    /// <summary>消息监测对象管理类-Msg
    /// </summary>
    public class DataMonitor_Msg
    {
        #region 属性及构造

        protected internal DataSwap_IOFiles _swapIOFiles = null;
        protected internal zxcConfigurationHelper _configDataCache = new zxcConfigurationHelper("appsettings.json");
        public DataMonitor_Msg()
        {
            string dirSwap = _configDataCache.config["DataCache.Swap:Monitor_Msg"] + "";
            _swapIOFiles = new DataSwap_IOFiles("msgWx", dirSwap, 0, typeof(Msger.Msg), "", true);
            //_swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 60 * 5, typeof(Data_Quote), "", true);      //忽略5分钟前数据

            //注册消息交换事件
            _swapIOFiles.SwapData_Change += new DataSwapChange_EventHandler(EventHandler_DataSwapChange);
        }
        ~DataMonitor_Msg()
        {
            // 缓存数据？
        }

        #endregion


        //数据对象监测开始
        public bool Start(int nSteps = -1, int nStepSwaps = 8, int nFrequency = 200)
        {
            return _swapIOFiles.Start(nSteps, nStepSwaps, nFrequency);
        }
        //数据对象监测结束
        public bool Stop()
        {
            return _swapIOFiles.Stop();
        }


        //交换文件监测变化事件
        private void EventHandler_DataSwapChange(object sender, DataSwap_Event e)
        {
            //ConsoleHelper.Debug(false, DateTime.Now + "::");
            foreach (IMsg item in e.Datas)
            {
                //加入全局消息
                MsgerHelper.Msger.CacheMsg(item);
                //List<Msger.Msg> aa = MsgerHelper.Msger.FindMsg(e => e.IsSend == false);
            }
        }

    }
}
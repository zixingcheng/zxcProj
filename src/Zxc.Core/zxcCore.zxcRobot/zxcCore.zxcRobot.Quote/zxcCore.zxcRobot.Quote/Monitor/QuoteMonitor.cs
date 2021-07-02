//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：QuoteMonitor_Manager --行情监测管理器
// 创建标识：zxc   2021-07-02
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using System.Reflection;
using zxcCore.Common;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcData.Cache.Swap;
using zxcCore.zxcRobot.Monitor.Msger;
using zxcCore.zxcRobot.Monitor.DataCheck;

namespace zxcCore.zxcRobot.Monitor.Quote
{
    /// <summary>行情监测管理器
    /// </summary>
    public class QuoteMonitor : QuoteMonitor_Manager
    {
        #region 属性及构造

        public QuoteMonitor() : base()
        {
        }
        ~QuoteMonitor()
        {
            // 缓存数据？
        }

        #endregion


        //初始数据交换对象信息
        public override bool InitDataSawp()
        {
            string dirSwap = _configDataCache.config["DataCache.Swap:Monitor_Quote"] + "";
            //_swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 0, typeof(Data_Quote_Swap), "", false);
            _swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 60 * 5, typeof(Data_Quote_Swap), "", true);      //忽略5分钟前数据
            _swapIOFiles.SwapData_Change += new DataSwapChange_EventHandler(EventHandler_DataSwapChange);


            //初始时间频率信息
            this.InitData_TimeFrequency(typeTimeFrequency.Second, 60 * 2);            //2分钟数据 120 条
            this.InitData_TimeFrequency(typeTimeFrequency.Minute_1, 60 * 1);          //1小时数据 120 条
            this.InitData_TimeFrequency(typeTimeFrequency.Minute_5, 12 * 5);          //5小时数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.Minute_15, 4 * 15);         //4天数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.Minute_30, 2 * 60);         //7.5天数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.Minute_60, 4 * 15);         //15天数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.Minute_120, 2 * 30);        //30天数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.Day, 1 * 60);               //60天数据 60 条
            //this.InitData_TimeFrequency(typeTimeFrequency.Week, 1 * 60);              //60周数据 60 条
            return true;
        }



        //初始数据检查对象集合-分钟级别
        public override bool InitDataCheck(IDataChecks pDataChecks, typeTimeFrequency timeFrequency)
        {
            //集成基类实现
            if (!base.InitDataCheck(pDataChecks, timeFrequency))
                return false;

            //按时间频率分类设置
            switch (timeFrequency)
            {
                case typeTimeFrequency.None:
                    break;
                case typeTimeFrequency.Second:
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_RiseFall_Fixed<Data_Quote_Swap>));
                    break;
                case typeTimeFrequency.Second_30:
                    break;
                case typeTimeFrequency.Minute_1:
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_Risk<Data_Quote_Swap>));
                    break;
                case typeTimeFrequency.Minute_5:
                    break;
                case typeTimeFrequency.Minute_10:
                    break;
                case typeTimeFrequency.Minute_15:
                    break;
                case typeTimeFrequency.Minute_30:
                    break;
                case typeTimeFrequency.Minute_60:
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_Hourly<Data_Quote_Swap>));
                    break;
                case typeTimeFrequency.Minute_120:
                    break;
                case typeTimeFrequency.Day:
                    break;
                default:
                    break;
            }
            return true;
        }


    }
}
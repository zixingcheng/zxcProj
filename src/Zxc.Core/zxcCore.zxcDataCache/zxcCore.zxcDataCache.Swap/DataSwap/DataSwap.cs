using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Threading;
using System.Threading.Tasks;

namespace zxcCore.zxcDataCache.Swap
{
    public abstract class DataSwap : IDataSwap
    {
        #region 属性及构造

        /// <summary数据交换事件
        /// </summary>
        public event DataSwapChange_EventHandler SwapData_Change;

        protected internal bool _is_Running = false;
        public bool Is_Running
        {
            get { return _is_Running; }
        }

        protected internal string _tagName = "";
        public string Tag_Name
        {
            get { return _tagName; }
        }

        protected internal Type _dest_ObjType = null;               //目标数据类型
        public Type Dest_ObjType
        {
            get { return _dest_ObjType; }
        }
        protected internal string _dest_NameMethod = "FromJson";    //目标数据对象方法名
        public string Dest_NameMethod
        {
            get { return _dest_NameMethod; }
        }

        protected internal int _nSteps = -1;                //交换次数，为0则永不停止
        protected internal List<AckInfo> _ackInfo = null;   //确认信息
        protected internal bool _useAck = false;            //是否使用数据确认模式
        protected internal bool _canDebug = false;          //是否允许打印调试信息
        protected internal int _delayedTime = 0;            //交换数据延迟有效时长(s)
        protected internal Task<bool> _taskSwap = null;     //任务进程
        public DataSwap(string tagName, int delayedTime = 0, Type classType = null, string nameMethod = "", bool canDebug = true, bool useAck = false)
        {
            _tagName = tagName;
            _useAck = useAck;
            _canDebug = canDebug;
            _delayedTime = delayedTime;
            _dest_ObjType = classType;
            if (nameMethod != "") _dest_NameMethod = nameMethod;
            _ackInfo = new List<AckInfo>();
        }
        ~DataSwap()
        {
            // 缓存数据？
        }

        #endregion

        /// <summary>开始数据交换
        /// </summary>
        /// <param name="nSteps">交换次数，为0则永不停止</param>
        /// <param name="nStepSwaps">单次交换数据条数，默认为1</param>
        /// <param name="nFrequency">单次交换数据后延时时间</param>
        /// <returns></returns>
        public virtual bool Start(int nSteps = 0, int nStepSwaps = 1, int nFrequency = 1000)
        {
            _nSteps = nSteps;
            if (_taskSwap == null || _taskSwap.Status != TaskStatus.Running)
                _taskSwap = Task.Run(() => thrdSwapData_Out(nStepSwaps, nFrequency));
            _is_Running = _taskSwap.Status == TaskStatus.Running;
            return true;
        }
        /// <summary>停止数据交换
        /// </summary>
        /// <returns></returns>
        public virtual bool Stop()
        {
            _nSteps = 0;
            if (_taskSwap != null)
            {
                _taskSwap.Dispose();
                _taskSwap = null;
            }
            return true;
        }

        /// <summary>数据交换-泵入
        /// </summary>
        /// <param name="nStepSwaps">交换数据数量</param>
        /// <param name="ackInfo">交换确认信息</param>
        /// <returns></returns>
        public virtual List<dynamic> SwapData_In(int nStepSwaps, out AckInfo ackInfo)
        {
            ackInfo = null;
            return null;
        }
        /// <summary>数据交换-泵出
        /// </summary>
        /// <param name="value"></param>
        /// <returns></returns>
        public virtual bool SwapData_Out(dynamic value)
        {
            return false;
        }
        /// <summary>数据交换-泵出（线程处理蹦出数据）
        /// </summary>
        /// <param name="nStepSwaps"></param>
        /// <param name="nFrequency"></param>
        /// <returns></returns>
        protected virtual bool thrdSwapData_Out(int nStepSwaps = 1, int nFrequency = 1000)
        {
            while (_nSteps != 0)
            {
                try
                {
                    _nSteps--;
                    AckInfo ackInfo = null;
                    List<dynamic> lstDatas = SwapData_In(nStepSwaps, out ackInfo);

                    if (this.SwapData_Change != null)
                    {
                        if (lstDatas.Count > 0)
                        {
                            this.SwapData_Change(this, this.CreateDataSwap_EventArgs(lstDatas, ackInfo));
                        }
                    }
                    Thread.Sleep(nFrequency);         //模拟长时间运算

                    //确认操作监测、修正
                    this.SwapData_Check();
                }
                catch (Exception e)
                {
                    Console.WriteLine("Error(DataSwap IOFiles)：" + e.ToString());
                    //throw;
                }
            }
            return true;
        }


        /// <summary>缓存确认信息
        /// </summary>
        /// <param name="ackInfo"></param>
        /// <returns></returns>
        protected virtual bool SwapData_Buffer(string ackTag, dynamic ackInfo)
        {
            if (!_useAck) return false;
            var query = _ackInfo.Where(e => e.AckTag == ackTag);
            if (query.Count() == 0)
            {
                AckInfo pAckInfo = new AckInfo(ackTag, ackInfo);
                _ackInfo.Add(pAckInfo);
                return true;
            }
            return false;
        }
        /// <summary>是否缓存确认信息
        /// </summary>
        /// <param name="ackInfo"></param>
        /// <returns></returns>
        protected virtual bool SwapData_AckNeed(dynamic ackTag)
        {
            if (!_useAck) return false;
            AckInfo pAckInfo = SwapData_AckQuery(ackTag);
            if (pAckInfo != null)
            {
                if (!pAckInfo.Acked)
                    return true;
            }
            return false;
        }
        /// <summary>提取确认对象
        /// </summary>
        /// <param name="ackInfo"></param>
        /// <returns></returns>
        protected virtual AckInfo SwapData_AckQuery(dynamic ackTag)
        {
            if (!_useAck) return null;
            var query = _ackInfo.Where(e => e.AckTag == ackTag);
            return query.FirstOrDefault();
        }
        /// <summary>确认操作
        /// </summary>
        /// <param name="ackInfo"></param>
        /// <returns></returns>
        public virtual bool SwapData_Ack(dynamic ackTag)
        {
            if (!_useAck) return false;
            AckInfo pAckInfo = SwapData_AckQuery(ackTag);
            if (pAckInfo != null)
            {
                pAckInfo.Acked = true;
                return true;
            }
            return false;
        }
        /// <summary>确认操作监测、修正
        /// </summary>
        /// <returns></returns>
        public virtual bool SwapData_Check()
        {
            List<AckInfo> lstDel = new List<AckInfo>();
            List<AckInfo> lstDelay = new List<AckInfo>();
            foreach (var item in _ackInfo)
            {
                if (item.Acked)
                {
                    if (File.Exists(item.SwapInfo))
                    {
                        File.Delete(item.SwapInfo);
                        lstDel.Add(item);
                    }
                }
                else
                {
                    if ((DateTime.Now - item.Time).TotalSeconds > 30)
                    {
                        lstDelay.Add(item);
                    }
                }
            }

            //移除已确认
            foreach (var item in lstDel)
            {
                _ackInfo.Remove(item);
            }

            //移除确认超时
            foreach (var item in lstDelay)
            {
                _ackInfo.Remove(item);
            }
            return true;
        }

        /// <summary>缓存数据备份
        /// </summary>
        /// <param name="path">文件路径</param>
        /// <param name="dir">目标文件夹路径</param>
        /// <returns></returns>
        public virtual bool SwapData_BackUp(string path, string dir)
        {
            try
            {
                string fileName = Path.GetFileName(path);
                int ind = fileName.IndexOf("_");
                string destDir = dir + "/" + fileName.Substring(ind + 1);

                if (Directory.Exists(destDir) == false)
                    Directory.CreateDirectory(destDir);
                if (!File.Exists(destDir + "/" + fileName))
                {
                    File.Copy(path, destDir + "/" + fileName);
                }

                if (File.Exists(destDir + "/" + fileName))
                {
                    if (!SwapData_AckNeed(path))
                        File.Delete(path);
                }
                return true;
            }
            catch (Exception)
            {
                //throw;
            }
            return false;
        }


        /// <summary>配置转为字符串
        /// </summary>
        public override string ToString()
        {
            return "";
        }
        /// <summary>字符串转配置
        /// </summary>
        public virtual void FromString()
        {
        }

        /// <summary>创建数据对象
        /// </summary>
        /// <param name="jsonData"></param>
        /// <returns></returns>
        protected internal dynamic CreateData_ClassObj(dynamic jsonData)
        {
            if (_dest_ObjType == null) return null;

            var instance = Activator.CreateInstance(_dest_ObjType);
            MethodInfo methodInfo = _dest_ObjType.GetMethod(_dest_NameMethod);
            if (methodInfo == null) return null;

            methodInfo.Invoke(instance, new object[] { jsonData });
            return instance;

            //泛型
            //Type constructedType = classType.MakeGenericType(typeof(T));
        }
        /// <summary>创建数据交换事件对象
        /// </summary>
        /// <param name="datas"></param>
        /// <param name="ackInfo"></param>
        /// <returns></returns>
        protected internal DataSwap_Event CreateDataSwap_EventArgs(List<dynamic> datas, AckInfo ackInfo = null)
        {
            DataSwap_Event pArgs = new DataSwap_Event();
            pArgs._Datas = datas;
            pArgs._AckInfo = ackInfo;
            return pArgs;
        }

    }
}

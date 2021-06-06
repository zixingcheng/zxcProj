using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;

namespace zpCore.zpDataCache.Swap
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
        protected internal int _nSteps = -1;
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


        protected internal dynamic _ackInfo = new { isAcked = false, time = DateTime.Now, retrys = 0, path = "" };
        protected internal Dictionary<string, DataSwap_AckInfo> _ackInfos;
        protected internal bool _useAck = true;             //启用数据确认模式
        protected internal int _delayedTime = 0;            //交换数据延迟有效时长(s)
        public DataSwap(string tagName, int delayedTime = 0, Type classType = null, string nameMethod = "", bool useAck = true)
        {
            _useAck = useAck;
            if (useAck)
                _ackInfos = new Dictionary<string, DataSwap_AckInfo>();
            _tagName = tagName;
            _delayedTime = delayedTime;
            _dest_ObjType = classType;
            if (nameMethod != "") _dest_NameMethod = nameMethod;
        }
        ~DataSwap()
        {
            // 缓存数据？
        }

        #endregion

        public virtual bool Start(int nSteps = 0, int nStepSwaps = 1, int nFrequency = 1000)
        {
            return false;
        }
        public virtual bool Stop()
        {
            _nSteps = 0;
            return false;
        }

        public virtual List<dynamic> SwapData_In(int nStepSwaps = 1)
        {
            return null;
        }
        public virtual bool SwapData_Out(dynamic value)
        {
            return false;
        }

        //判断是否需要确认
        public virtual bool checkNeedAck(string fileName)
        {
            if (_useAck == false) return false;
            if (!_ackInfos.ContainsKey(fileName)) return false;
            DataSwap_AckInfo pAckInfo = _ackInfos[fileName];

            bool bAcked = false;
            if (pAckInfo.IsAcked)
            {
                bAcked = true;
                if (this.SwapData_BackUp(pAckInfo.Path, ""))
                    _ackInfos.Remove(fileName);
            }
            else
            {
                DateTime dtNow = DateTime.Now;
                if ((dtNow - pAckInfo.Time).TotalSeconds > 10)
                {
                    pAckInfo.Retrys += 1;
                }
                else
                    bAcked = true;

                //重试过多则忽略
                if (pAckInfo.Retrys > 10)
                {
                    bAcked = true;
                    this.SwapData_BackUp(pAckInfo.Path, "");
                }
            }
            return bAcked;
        }
        //确认已接收
        public virtual bool ackDataSwap(dynamic ackInfo)
        {
            if (_useAck == false) return false;
            if (ackInfo == null) return false;

            var fileName = ackInfo.tagAck.Value + "";
            if (fileName == "") return false;

            if (!_ackInfos.ContainsKey(fileName)) return false;
            DataSwap_AckInfo pAckInfo = _ackInfos[fileName];

            pAckInfo.IsAcked = true;
            pAckInfo.TimeAcked = DateTime.Now;
            if (this.SwapData_BackUp(pAckInfo.Path, ""))
                _ackInfos.Remove(fileName);
            return true;
        }

        public virtual bool SwapData_BackUp(string path, string dir)
        {
            try
            {
                string fileName = Path.GetFileName(path);
                string[] temps = fileName.Split('_');
                string destDir = dir + "/" + temps[temps.Length - 1].Substring(0, 10);

                if (Directory.Exists(destDir) == false)
                    Directory.CreateDirectory(destDir);
                if (!File.Exists(destDir + "/" + fileName))
                    File.Copy(path, destDir + "/" + fileName);

                if (File.Exists(destDir + "/" + fileName))
                    File.Delete(path);
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

        protected internal dynamic CreateData_ClassObj(dynamic jsonData)
        {
            if (_dest_ObjType == null) return jsonData;

            var instance = Activator.CreateInstance(_dest_ObjType);
            MethodInfo methodInfo = _dest_ObjType.GetMethod(_dest_NameMethod);
            if (methodInfo == null) return jsonData;

            methodInfo.Invoke(instance, new object[] { jsonData });
            return instance;

            //泛型
            //Type constructedType = classType.MakeGenericType(typeof(T));
        }
        protected internal DataSwap_EventArgs CreateDataSwap_EventArgs(List<dynamic> datas)
        {
            DataSwap_EventArgs pArgs = new DataSwap_EventArgs();
            pArgs._Datas = datas;
            return pArgs;
        }
    }
}

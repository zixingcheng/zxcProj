using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;

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


        protected internal int _delayedTime = 0;           //交换数据延迟有效时长(s)
        public DataSwap(string tagName, int delayedTime = 0, Type classType = null, string nameMethod = "")
        {
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


        public virtual bool SwapData_BackUp(string path, string dir)
        {
            try
            {
                string fileName = Path.GetFileName(path);
                string destDir = dir + "/" + fileName.Split('_')[1].Substring(0, 10);

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
            if (_dest_ObjType == null) return null;

            var instance = Activator.CreateInstance(_dest_ObjType);
            MethodInfo methodInfo = _dest_ObjType.GetMethod(_dest_NameMethod);
            if (methodInfo == null) return null;

            methodInfo.Invoke(instance, new object[] { jsonData });
            return instance;

            //泛型
            //Type constructedType = classType.MakeGenericType(typeof(T));
        }
        protected internal DataSwap_Event CreateDataSwap_EventArgs(List<dynamic> datas)
        {
            DataSwap_Event pArgs = new DataSwap_Event();
            pArgs._Datas = datas;
            return pArgs;
        }
    }
}

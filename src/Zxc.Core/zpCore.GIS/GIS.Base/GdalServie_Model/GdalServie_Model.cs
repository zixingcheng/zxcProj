using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using zpCore.GIS.Renderer;

namespace zpCore.GIS.Models.Service
{
    public abstract class GdalServie_Model : IGdalServie_Model
    {
        #region 属性及构造

        protected internal emModeState _ModeState = emModeState.None;
        /// <summary>模型状态
        /// </summary> 
        public emModeState ModeState
        {
            get { return _ModeState; }
        }

        protected internal string _dtTag = "";          //参数传入的时间标识，用于限定输出文件
        protected internal string _nameTag = "";        //文件名标识，用于限定输出文件
        protected internal JObject _Result = null;
        protected internal JObject _Datas = null;
        protected internal JObject _Params = null;
        protected internal JObject _Renderer = null;
        protected internal string _FloderGis = "";
        protected internal string _FloderTemp = "";
        protected internal string _FloderOutput = "";
        protected internal string _FloderRenderer = "";
        protected internal string _Params_str = "";
        protected internal string _Params_test = "";
        protected internal string _Params_run = "";
        protected internal string _Params_renderer = "";
        protected internal emRenderType _RenderType;
        protected internal List<string> _Errors = new List<string>();

        public GdalServie_Model(string baseFloder = "BaseGis")
        {
            _FloderGis = GdalCommon.psDirData_BaseGis + baseFloder + "/";
            _FloderTemp = GdalCommon.psDirData_BaseGis + GdalCommon.configGisBase.config["GisSetOptions:GisDataDirs:TempDir"] + "";
            _FloderOutput = GdalCommon.psDirData_OutputGis;
            this.InitResult();
        }
        ~GdalServie_Model()
        {
        }

        #endregion

        /// <summary> 初始默认测试参数
        /// </summary>
        /// <returns></returns>
        public virtual string InitParam_Test(string tag = "")
        {
            return "";
        }

        /// <summary> 初始参数
        /// </summary>
        /// <param name="strParams">参数</param>
        /// <param name="useTestParam">是否使用默认测试参数（未传入参数时）</param>
        /// <returns></returns>
        public virtual bool InitParams(string strParams, bool useTestParam = false)
        {
            if (useTestParam && strParams == "")
            {
                strParams = InitParam_Test();
            }
            _RenderType = emRenderType.None;
            _Params_str = strParams;
            _Errors.Clear();

            try
            {
                _Params = JsonConvert.DeserializeObject<dynamic>(_Params_str);
                _Renderer = (JObject)_Params["rendererParms"];
                if (_Renderer != null)
                    Enum.TryParse<emRenderType>(_Renderer["rendererType"].ToString(), out _RenderType);

                DateTime dt = DateTime.Now;
                if (_Params["dataTime"].ToString() != "")
                    dt = Convert.ToDateTime(_Params["dataTime"].ToString());
                _dtTag = dt.ToString("_yyyyMMdd_HHmmss_ffff");
            }
            catch (System.Exception e)
            {
                _Errors.Add(e.Message);
                return false;
            }
            return this.CheckParams();
        }
        /// <summary>模型参数校检
        /// </summary>
        /// <returns></returns>
        public virtual bool CheckParams()
        {
            if (_Errors.Count > 0) return false;
            _ModeState = emModeState.Preparing;
            return true;
        }

        /// <summary> 初始模型结果返回结构
        /// </summary>
        /// <returns></returns>
        public virtual bool InitResult()
        {
            // 组装返回结果
            _Result = new JObject();
            _Result.Add("code", 0);
            _Result.Add("success", false);
            _Result.Add("msg", null);
            _Result.Add("datas", null);
            return true;
        }

        /// <summary>初始模型错误信息
        /// </summary>
        /// <param name="strErr">错误信息</param>
        /// <param name="bRunend">是否停止</param>
        /// <returns></returns>
        public virtual bool InitError(string strErr, bool bRunend = false)
        {
            _Errors.Add(strErr);
            if (bRunend)
                _ModeState = emModeState.Runerror;
            return true;
        }


        /// <summary>运行模型
        /// </summary>
        /// <param name="strParams_run">运行参数</param>
        /// <returns></returns>
        public virtual bool RunModel(string strParams_run = "")
        {
            if (this._ModeState != emModeState.Preparing)
                return false;

            _Params_run = strParams_run;
            _ModeState = emModeState.Running;
            return true;
        }
        /// <summary>渲染模型结果
        /// </summary>
        /// <param name="strParams_renderer">渲染参数</param>
        /// <returns></returns>
        public virtual bool Renderer(string strParams_renderer = "")
        {
            _Params_renderer = strParams_renderer;
            if (this._ModeState != emModeState.Runout) return false;
            if (_Renderer == null) return false;

            if (_FloderRenderer != "")
                if (!Directory.Exists(_FloderRenderer))
                    Directory.CreateDirectory(_FloderRenderer);
            return true;
        }


        /// <summary>提取模型运行结果
        /// </summary>
        /// <returns></returns>
        public virtual string GetResult(bool autoSave = true)
        {
            string outFilename = _FloderOutput + _nameTag + ".json";
            if (_Datas != null)
            {
                _Datas["path"] = outFilename;
            }

            _Result["success"] = _Errors.Count == 0;
            _Result["datas"] = _Datas;
            _Result["msg"] = string.Join(";", _Errors);

            if (Convert.ToBoolean(_Params["outputParams"]))
                _Result["params"] = this._Params;

            string result = JsonConvert.SerializeObject(_Result);
            if (autoSave)
                File.WriteAllText(outFilename, result);
            return result;
        }

        /// <summary>提取模型运行状态
        /// </summary>
        /// <returns></returns>
        public virtual emModeState GetModelState()
        {
            return ModeState;
        }

    }
}



using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using zpCore.Image;

namespace zpCore.GIS.Renderer
{

    public abstract class Renderer : IRenderer
    {
        #region 属性及构造

        protected internal emRenderType _RenderType;
        public emRenderType RenderType
        {
            get { return _RenderType; }
        }

        protected internal bool _IsRaster = false;
        public bool IsRaster
        {
            get { return _IsRaster; }
        }

        protected internal string[] _Titles = null;
        public string[] Titles
        {
            get { return _Titles; }
        }

        protected internal string[] _TitlesAlias = null;
        public string[] TitlesAlias
        {
            get { return _TitlesAlias; }
        }

        protected internal string[] _Colors = null;
        public string[] Colors
        {
            get { return _Colors; }
        }

        protected internal dynamic[] _Values = null;
        public dynamic[] Values
        {
            get { return _Values; }
        }

        protected internal double[] _Breaks = null;
        public double[] Breaks
        {
            get { return _Breaks; }
        }

        protected internal ImageObj _Image = null;
        public ImageObj Image
        {
            get { return _Image; }
        }

        protected internal IGdalRead _GdalRead = null;
        protected internal IMetadata _Metadata = null;
        protected internal JObject _Result = null;
        protected internal JObject _Params = null;
        protected internal List<ImageColor> _ImageColors = new List<ImageColor>();
        public Renderer(IGdalRead gdalRead)
        {
            _GdalRead = gdalRead;
        }
        ~Renderer()
        {
        }

        #endregion

        protected internal virtual string InitParam_Test()
        {
            var jsonParams_Test = new
            {
                rendererType = "Classify",
                rendererInfo = new
                {
                    breaksInfo = new[] { 0, 50, 100, 150, 200, 300, 400, int.MaxValue },
                    levelsInfo = new[] { "一级", "二级", "三级", "四级", "五级", "六级" },
                    titlesInfo = new[] { "优", "良", "轻度污染", "中度污染", "重度污染", "严重污染" },
                    colorsInfo = new[] { "#008000", "#FFFF00", "#FFA500", "#FF0000", "#800080", "8E236B" },
                    //colorsInfo = new[] { "绿色", "黄色", "橙色", "红色", "紫色", "褐红色" },   //'深褐红色': "#8E236B"
                },
                legendInfo = new
                {
                    titlesInfo = new[] { "0-50", "50-100", "100-150", "150-200", "200-300", "300-500" },
                    colorsInfo = new[] { "#008000", "#FFFF00", "#FFA500", "#FF0000", "#800080", "#8E236B" }
                }
            };
            return JsonConvert.SerializeObject(jsonParams_Test);
        }

        /// <summary> 初始参数
        /// </summary>
        /// <param name="strParams">参数</param>
        /// <param name="useTestParam">是否使用默认测试参数（未传入参数时）</param>
        /// <returns></returns>
        public virtual bool InitParams(string strParams, bool useTestParam = false)
        {
            if (useTestParam && strParams == "")
                strParams = InitParam_Test();

            var parmObj = JObject.Parse(strParams);
            return this.InitParams(parmObj);
        }
        /// <summary> 初始参数
        /// </summary>
        /// <param name="strParams">参数</param>
        /// <param name="useTestParam">是否使用默认测试参数（未传入参数时）</param>
        /// <returns></returns>
        public virtual bool InitParams(JObject parmObj)
        {
            _Params = parmObj;
            Enum.TryParse<emRenderType>(_Params["rendererType"].ToString(), out _RenderType);
            return this.InitValues() && this.InitBreaks() && this.InitInfos();
        }

        /// <summary>初始值集信息
        /// </summary>
        /// <returns></returns>
        protected internal virtual bool InitValues()
        {
            if (_Params == null) return false;
            JObject rendererInfo = (JObject)_Params["rendererInfo"];
            if (rendererInfo == null) return false;

            JArray valuesInfo = (JArray)rendererInfo["valuesInfo"];
            if (valuesInfo == null) return false;

            _Values = new dynamic[valuesInfo.Count];
            for (int i = 0; i < valuesInfo.Count; i++)
            {
                _Values[i] = valuesInfo[i];
            }
            return true;
        }
        /// <summary>初始断点信息
        /// </summary>
        /// <returns></returns>
        protected internal virtual bool InitBreaks()
        {
            if (_Params == null) return false;
            JObject rendererInfo = (JObject)_Params["rendererInfo"];
            if (rendererInfo == null) return false;

            JArray breaksInfo = (JArray)rendererInfo["breaksInfo"];
            if (breaksInfo == null) return false;

            _Breaks = new double[breaksInfo.Count];
            for (int i = 0; i < breaksInfo.Count; i++)
            {
                _Breaks[i] = Convert.ToDouble(breaksInfo[i]);
            }
            return true;
        }
        /// <summary>初始信息集
        /// </summary>
        /// <returns></returns>
        protected internal virtual bool InitInfos()
        {
            return this.InitRenderInfos("levelsInfo", ref _Titles)
                && this.InitRenderInfos("titlesInfo", ref _TitlesAlias)
                && this.InitRenderInfos("colorsInfo", ref _Colors);
        }
        /// <summary>初始信息
        /// </summary>
        /// <param name="tag">json节点rendererInfo下信息标识</param>
        /// <param name="values">值数组</param>
        /// <returns></returns>
        protected internal virtual bool InitRenderInfos(string tag, ref string[] values, string keyNode = "rendererInfo")
        {
            if (_Params == null) return false;
            JObject rendererInfo = (JObject)_Params[keyNode];
            if (rendererInfo == null) return false;

            JArray tempsInfo = (JArray)rendererInfo[tag];
            if (tempsInfo == null) return false;

            values = new string[tempsInfo.Count];
            for (int i = 0; i < tempsInfo.Count; i++)
            {
                values[i] = tempsInfo[i].ToString();
            }
            return true;
        }

        public virtual bool Render(ImageObj img = null)
        {
            //初始颜色对象集
            if (_Colors == null) return true;
            for (int i = 0; i < _Colors.Length; i++)
            {
                _ImageColors.Add(new ImageColor(_Colors[i]));
            }

            _Image = img;
            _Result = new JObject();
            _Result["params"] = _Params;
            _Result["renderer"] = new JObject();
            return true;
        }
        public virtual bool Render_Draw(ImageObj img = null)
        {
            double pixResoultion = 0.0005;

            //提取数据信息
            if (_GdalRead == null) return false;
            IMetadataR pMetadata = (IMetadataR)_GdalRead.GetMetadata();
            if (pMetadata == null) return false;

            pMetadata.Cols = (int)Math.Floor((_Metadata.MaxX - _Metadata.MinX) / pixResoultion);
            pMetadata.Rows = (int)Math.Floor((_Metadata.MaxY - _Metadata.MinY) / pixResoultion);

            //绘图 
            if (img == null)
                if (_Image == null)
                    _Image = new ImageObj(pMetadata.Cols, pMetadata.Rows);
                else
                    _Image = img;
            _Metadata = pMetadata;
            return true;
        }
        public virtual ImageColor GetColor(double value)
        {
            return null;
        }

        /// <summary>提取模型运行结果
        /// </summary>
        /// <returns></returns>
        public virtual dynamic ToRendererStr(bool toStr = true)
        {
            JObject extent = new JObject();
            if (_Metadata != null)
            {
                extent["MinX"] = _Metadata.MinX;
                extent["MinY"] = _Metadata.MinY;
                extent["MaxX"] = _Metadata.MaxX;
                extent["MaxY"] = _Metadata.MaxY;
            }
            _Result["extent"] = extent;

            if (toStr)
            {
                string result = JsonConvert.SerializeObject(_Result);
                return result;
            }
            else
                return _Result;
        }

        public virtual bool Output(string path, string name = "")
        {
            bool bResult = true;
            if (_Image != null)
            {
                if (name + "" != "")
                    _Image.Name = name;
                bResult = _Image.Save(path);
                name = _Image.Name + _Image.Suffix;
            }

            if (_Result != null)
            {
                if (_Result["renderer"] != null)
                {
                    _Result["renderer"]["route"] = path;
                    _Result["renderer"]["name"] = name;
                    _Result["renderer"]["nameLegend"] = "";
                    _Result["renderer"]["namePublish"] = "";
                }
            }
            return bResult;
        }
    }
}
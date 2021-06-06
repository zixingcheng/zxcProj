using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Text;
using zpCore.GIS.Trans.Algorithm;
using zpCore.GIS.Trans;
using Newtonsoft.Json;
using System.IO;
using Newtonsoft.Json.Linq;
using zpCore.GIS.Renderer;
using zpCore.Image;

namespace zpCore.GIS.Models.Service
{
    public class Servie_Distribution : GdalServie_Model
    {
        #region 属性及构造

        string _dstRasterFile = "";
        public Servie_Distribution(string baseFloder = "BaseGis") : base(baseFloder)
        {
            _FloderTemp = GdalCommon.psDirData_BaseGis + GdalCommon.configGisBase.config["GisSetOptions:GisDataDirs:TempIDWDir"] + "";
        }
        ~Servie_Distribution()
        {
        }

        #endregion

        public override string InitParam_Test(string tag = "")
        {
            if (tag == "")
            {
                var jsonParams_Test = new
                {
                    dataTime = "2021-1-22 18:08:00",
                    srcData = new
                    {
                        srcVectorFilename = GdalCommon.psDirData_BaseGis + @"Data_Temp/test.geojson",
                        srcTimeType = "Day"
                    },
                    algType = "IDW",
                    algParms = new      //按具体算法类型设置
                    {
                        algAtrrName = "Aqi",
                        algCellSize = 0.0005,
                        algEnvelope_offsetX = 0.085,
                        algEnvelope_offsetY = 0.065,
                        Power = 2,
                        Smoothing = 0,
                        Radius1 = 0,
                        Radius2 = 0,
                        NoDataValue = -9999
                    },
                    clipData = new
                    {
                        //infoDivision = "广东省.东莞市",
                        //clipWhere = "O_Name='南城区'"
                        infoDivision = "",
                        clipWhere = "WZ",
                        clipVaild = true
                    },
                    dstContour = new
                    {
                        //LevelIntervals = new[] { 30, 40, 50, 60 },
                        LevelIntervals = new[] { 10, 20, 30, 40, 50,
                        60, 70, 80, 90, 100,
                        110, 120, 130, 140, 150,
                        160, 170, 180, 190, 200,
                        220, 240, 260, 280, 300,
                        340, 380, 420, 460 },
                        LevelBase = 10,
                        IsPolygon = true,
                        dstFileName = ""
                    },
                    rendererParms = new
                    {
                        rendererType = "Classify",      //只允许Classify
                        rendererInfo = new
                        {
                            //breaksInfo = new[] { 0, 50, 100, 150, 200, 300, 400, int.MaxValue },
                            //levelsInfo = new[] { "一级", "二级", "三级", "四级", "五级", "六级" },
                            //titlesInfo = new[] { "优", "良", "轻度污染", "中度污染", "重度污染", "严重污染" },
                            //colorsInfo = new[] { "#008000", "#FFFF00", "#FFA500", "#FF0000", "#800080", "8E236B" },
                            //colorsInfo = new[] { "绿色", "黄色", "橙色", "红色", "紫色", "褐红色" },   //'深褐红色': "#8E236B"
                            breaksInfo = new[] { 0, 10, 20, 30, 40, 50,
                            60, 70, 80, 90, 100,
                            110, 120, 130, 140, 150,
                            160, 170, 180, 190, 200,
                            220, 240, 260, 280, 300,
                            340, 380, 420, 460, 500
                            },
                            levelsInfo = new[] { "一级-1", "一级-2", "一级-3", "一级-4", "一级-5",
                            "二级-1", "二级-2", "二级-3", "二级-4", "二级-5",
                            "三级-1", "三级-2", "三级-3", "三级-4", "三级-5",
                            "四级-1", "四级-1", "四级-1", "四级-1", "四级-1",
                            "五级-1", "五级-1", "五级-1", "五级-1", "五级-1",
                            "六级-1", "六级-2", "六级-3", "六级-4", "六级-5"
                            },
                            titlesInfo = new[] { "优-1", "优-2", "优-3", "优-4", "优-5",
                            "良-1", "良-2", "良-3", "良-4", "良-5",
                            "轻度污染-1", "轻度污染-2", "轻度污染-3", "轻度污染-4", "轻度污染-5",
                            "中度污染-1", "中度污染-2", "中度污染-3", "中度污染-4", "中度污染-5",
                            "重度污染-1", "重度污染-2", "重度污染-3", "重度污染-4", "重度污染-5",
                            "严重污染-1", "严重污染-2", "严重污染-3", "严重污染-4", "严重污染-5"
                            },
                            colorsInfo = new[] { "#00BC00", "#00C600", "#00D000", "#00DA00", "#00E400",
                            "#AFFF00", "#C3FF00", "#D7FF00", "#EBFF00", "#FFFF00",
                            "#ffe100", "#ffc800", "#ffaf00", "#ff9600", "#FF7E00",
                            "#ff6800", "#ff4e00", "#ff3400", "#ff1a00", "#FF0000",
                            "#e9004c", "#d5004c", "#c1004c", "#ad004c", "#86003c",
                            "#940042", "#8e0038", "#89002d", "#830023", "#7E0019",
                            }
                        },
                        legendInfo = new
                        {
                            titlesInfo = new[] { "0-50", "50-100", "100-150", "150-200", "200-300", "300-500" },
                            colorsInfo = new[] { "#008000", "#FFFF00", "#FFA500", "#FF0000", "#800080", "#8E236B" }
                        },
                        rendererOutputLegend = true,
                        rendererOutputPublish = true
                    },
                    outputParams = true
                };
                _Params_test = JsonConvert.SerializeObject(jsonParams_Test);
            }
            else
            {
                string path = Directory.GetCurrentDirectory() + "/ModelData/GIS/DistributionMap/Param/" + tag + ".json";
                if (File.Exists(path))
                    _Params_test = File.ReadAllText(path);
            }
            return _Params_test;
        }

        public override bool CheckParams()
        {
            if (!base.CheckParams()) return false;

            _RenderType = emRenderType.Classify;
            return true;
        }


        public override bool RunModel(string strParams_run = "")
        {
            bool bRes = base.RunModel(strParams_run);

            return bRes && RunModel_Distribution() && Renderer();
        }

        public override bool Renderer(string strParams_renderer = "")
        {
            bool bResult = true;
            _FloderRenderer = _FloderOutput;
            if (base.Renderer(strParams_renderer))
            {
                //载入结果栅格
                if (_dstRasterFile == "") return true;
                GdalRead_TIFF gdalRead_TIFF = new GdalRead_TIFF();
                gdalRead_TIFF.InitDataset(_dstRasterFile, 0, false);

                string fileName = _Datas["title"] + _dtTag;
                IRasterRenderer pRender = (IRasterRenderer)Renderer_Factory.CreateRenderer(emRenderType.Classify, gdalRead_TIFF);
                pRender.InitParams(_Renderer);
                pRender.Render();
                pRender.Output(_FloderRenderer, fileName);


                //图例处理等
                JObject renderInfo = (JObject)pRender.ToRendererStr(false);
                _Result["renderer"] = renderInfo;
                _Renderer = (JObject)_Params["rendererParms"];
                if (_Renderer != null)
                {
                    //创建图例
                    if (Convert.ToBoolean(_Renderer["rendererOutputLegend"]))
                    {
                        bResult = bResult && pRender.Create_Legend(_FloderRenderer, "Legend_" + _Datas["title"]);
                        if (bResult)
                            _Result["renderer"]["renderer"]["nameLegend"] = pRender.Image_Legend.Name + pRender.Image_Legend.Suffix;
                    }

                    //创建发布图
                    if (Convert.ToBoolean(_Renderer["rendererOutputPublish"]))
                    {
                        //含图例的渲染图
                        ImageObj _Image = pRender.Image, _Image_legend = pRender.Image_Legend;
                        if (_Image_legend == null)
                        {
                            bResult = bResult && pRender.Create_Legend(_FloderRenderer, "Legend_" + _Datas["title"]);
                            _Image_legend = pRender.Image_Legend;
                        }

                        ImageColor pColor = new ImageColor("#192734");
                        ImageObj _Image_Scale = pRender.Create_Scale();
                        ImageObj img = new ImageObj(_Image.Width + _Image_legend.Width, _Image.Height > _Image_legend.Height ? _Image.Height : _Image_legend.Height);
                        img.DrawImage(_Image_legend.Width, 0, _Image, 1);
                        img.DrawImage(0, (int)((img.Height - _Image_legend.Height)), _Image_legend, 1);
                        img.DrawImage((int)(_Image_legend.Width * 1.2), (int)((img.Height - _Image_Scale.Height * 1.2)), _Image_Scale, 1);
                        img.DrawPolygon(0, 20, pColor.Color, 1, img.Width - 1, img.Height - 21);
                        img.Name = fileName + "_publish";
                        bResult = bResult && img.Save(_FloderRenderer);
                        if (bResult)
                            _Result["renderer"]["renderer"]["namePublish"] = img.Name + img.Suffix;
                    }
                }
            }
            return true;
        }


        /// <summary>分布图
        /// </summary>
        /// <param name="strParams">json参数</param>
        /// <returns></returns>
        private bool RunModel_Distribution()
        {
            // 解析参数
            var jsonParams = _Params;

            // 初始插值方法对象
            GdalAlg_IWD gdalAlg = null;
            string algType = jsonParams["algType"] + "";
            string algParms = JsonConvert.SerializeObject(jsonParams["algParms"]);
            switch (algType)
            {
                case "IDW":
                    gdalAlg = (GdalAlg_IWD)InitGdalAlg_IWD(algParms);
                    break;
                default:
                    break;
            }

            // 初始格网生成参数
            string srcVectorFilename = jsonParams["srcData"]["srcVectorFilename"] + "";
            string srcTimeType = jsonParams["srcData"]["srcTimeType"] + "";
            string strAtrrName = jsonParams["algParms"]["algAtrrName"] + "";
            if (srcTimeType != "")
                srcTimeType = "_" + srcTimeType + "";
            double dCellSize = Convert.ToDouble(jsonParams["algParms"]["algCellSize"] + "");
            double dEnvelope_offsetX = Convert.ToDouble(jsonParams["algParms"]["algEnvelope_offsetX"] + "");
            double dEnvelope_offsetY = Convert.ToDouble(jsonParams["algParms"]["algEnvelope_offsetY"] + "");
            double dNoDataValue = -9999;

            string srcFileName = Path.GetFileNameWithoutExtension(srcVectorFilename);
            string dstRasterFilename = _FloderTemp + GdalCommon.CreateName(_FloderTemp, srcFileName, ".tiff") + ".tiff";
            bool isUseClip = Convert.ToBoolean(jsonParams["clipData"]["clipVaild"] + "");
            string clipVectorWhere = jsonParams["clipData"]["clipWhere"] + "";
            string division = clipVectorWhere != "" ? clipVectorWhere : "division";
            string clipVectorFilename = GdalCommon.GetFile_Division(Convert.ToString(jsonParams["clipData"]["infoDivision"])) + division + ".geojson";
            string dstRasterFilenameClip = dstRasterFilename;
            if (isUseClip)
            {
                dstRasterFilenameClip = _FloderTemp + GdalCommon.CreateName(_FloderTemp, srcFileName, ".tiff") + "_Clip.tiff";
            }
            string strFileName = jsonParams["dstContour"]["dstFileName"] + "";
            strFileName = strFileName != "" ? strFileName : _dtTag;    //GdalCommon.CreateName(_FloderTemp, "", ".geojson");
            _nameTag = strAtrrName + srcTimeType + strFileName;
            _FloderOutput = _FloderOutput + "Distribution/" + gdalAlg.AlgName + "/";
            string outFilename = _FloderOutput + _nameTag + ".geojson";
            if (!Directory.Exists(_FloderOutput))
                Directory.CreateDirectory(_FloderOutput);

            // 初始插值源数据
            IGdalRead gdalRead = GdalRead_Factory.CreateGdalRead(srcVectorFilename);
            if (!gdalRead.InitDataSource(srcVectorFilename, Encoding.UTF8, 0, false))
            {
                Console.WriteLine(srcVectorFilename);
                this.InitError(string.Format("插值源数据{0}打开失败！数据不存在或文件错误！", Path.GetFileName(srcVectorFilename)), true);
                return false;
            }

            // 调用IDW插值算法生成格网
            GdalTrans_Grid poTrans = new GdalTrans_Grid(gdalRead, gdalAlg);
            if (poTrans.TransToGrid(strAtrrName, dstRasterFilename, dCellSize, dEnvelope_offsetX, dEnvelope_offsetY) == false)
            {
                this.InitError("IDW插值算法生成格网出错！", true);
                return false;
            }

            // 调用裁剪
            if (isUseClip)
            {
                GdalTrans_Clip poTrans_Clip = new GdalTrans_Clip();
                if (poTrans_Clip.ClipRaster(clipVectorFilename, "", dstRasterFilename, 1, dstRasterFilenameClip, dNoDataValue) == false)
                {
                    this.InitError("IDW插值格网裁剪出错！", true);
                    return false;
                }
            }


            // 初始等值面提取参数
            double[] dLevelIntervals = jsonParams["dstContour"]["LevelIntervals"].ToObject<List<double>>().ToArray();
            double dLevelBase = Convert.ToDouble(jsonParams["dstContour"]["LevelBase"] + "");
            bool isPolygon = Convert.ToBoolean(jsonParams["dstContour"]["IsPolygon"] + "");

            // 调用等值面提取
            GdalTrans_Contour poTrans_Contour = new GdalTrans_Contour(gdalRead);
            poTrans_Contour.ContourGenerate(dstRasterFilenameClip, outFilename, 1, dLevelIntervals, dLevelBase, isPolygon);

            // 组装返回结果
            _ModeState = emModeState.Runout;
            _Datas = new JObject();
            _Datas.Add("typeFile", "GeoJSON");
            _Datas.Add("typeAlg", algType);
            _Datas.Add("title", strAtrrName + srcTimeType);
            _Datas.Add("nameTag", _nameTag);
            _Datas.Add("outFile", outFilename);
            _dstRasterFile = dstRasterFilenameClip;
            return true;
        }

        private IGdalAlg InitGdalAlg_IWD(string algParms)
        {
            #region 参数结构

            //var jsonParams_Test = new
            //{
            //    algParms = new
            //    {
            //        Power = 2,
            //        Smoothing = 0,
            //        Radius1 = 0,
            //        Radius2 = 0,
            //        NoDataValue = -9999
            //    }
            //};
            #endregion

            // 初始IDW权重参数 
            GdalAlg_IWD gdalAlg = new GdalAlg_IWD();
            var paramsIDW = JsonConvert.DeserializeObject<dynamic>(algParms);
            gdalAlg.Power = Convert.ToDouble(paramsIDW["Power"] + "");
            gdalAlg.Smoothing = Convert.ToDouble(paramsIDW["Smoothing"] + "");
            gdalAlg.Radius1 = Convert.ToDouble(paramsIDW["Radius1"] + "");
            gdalAlg.Radius2 = Convert.ToDouble(paramsIDW["Radius2"] + "");
            gdalAlg.NoDataValue = Convert.ToDouble(paramsIDW["NoDataValue"] + "");

            return gdalAlg;
        }

    }
}

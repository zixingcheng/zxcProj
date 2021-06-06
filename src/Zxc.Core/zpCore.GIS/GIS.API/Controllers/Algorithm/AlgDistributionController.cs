using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using zpCore.GIS.API.Common;
using zpCore.GIS;
using zpCore.GIS.Models.Service;
using zpCore.GIS.API.Models;
using Microsoft.Extensions.Options;

namespace zpCore.GIS.API.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class AlgDistributionController : ControllerBase
    {
        private readonly FileSetOptions _fileOptions;
        public AlgDistributionController(IOptions<FileSetOptions> options) => this._fileOptions = options.Value;

        [HttpPost]
        public ActionResult<string> runModel(dynamic value)
        {
            //提取参数
            //JObject pParams = JObject.FromObject(value);
            JObject pParams = JObject.Parse(value + "");
            if (pParams == null || pParams["params"] + "" == "")
                return common.transResult(null, "非有效Json格式参数！", false);
            if (pParams["params"]["srcData"]["srcVectorFilename"] + "" != "")
            {
                string path = Directory.GetCurrentDirectory() + _fileOptions.FileBaseDir + "/" + pParams["params"]["srcData"]["srcVectorFilename"];
                pParams["params"]["srcData"]["srcVectorFilename"] = path.Replace("\\", "/");
            }

            //分布图模型调用
            GdalCommon.RegisterAll();
            Servie_Distribution GdalServie = new Servie_Distribution();

            GdalServie.InitParams(pParams["params"] + "", true);
            GdalServie.RunModel(pParams["params_run"] + "");

            // 通用转换（将绝对路径转换为网页路径）
            string result = GdalServie.GetResult();
            return common.transResult_zpService(result);
        }

    }
}

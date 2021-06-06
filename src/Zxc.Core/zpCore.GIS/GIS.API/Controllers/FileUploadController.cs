using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Newtonsoft.Json.Linq;
using zpCore.GIS.API.Common;
using zpCore.GIS.API.Models;

namespace zpCore.GIS.API.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class FileUploadController : ControllerBase
    {
        private readonly FileSetOptions _fileOptions;
        public FileUploadController(IOptions<FileSetOptions> options) => this._fileOptions = options.Value;

        /// <summary>上传文件
        /// </summary>
        /// <param name="file">来自form表单的文件信息</param>
        /// <param name="newName">文件名(不含后缀)</param>
        /// <returns></returns>
        [HttpPost]
        public IActionResult Post([FromForm(Name = "file")] IFormFile file, [FromForm(Name = "newName")] string newName)
        {
            //var files = Request.Form.Files;
            if (file == null)
                return new JsonResult(new { code = 500, msg = "文件为null" });
            if (file.Length <= this._fileOptions.FileMaxSize)           //检查文件大小
            {
                var suffix = Path.GetExtension(file.FileName);          //提取上传的文件文件后缀
                if (this._fileOptions.FileTypes.IndexOf(suffix) >= 0)   //检查文件格式
                {
                    if (newName + "" == "")
                        newName = common.createName(this._fileOptions.FileBaseDir, suffix);
                    string path = Directory.GetCurrentDirectory() + $@"{this._fileOptions.FileBaseDir}/{newName}{suffix}";
                    if (!Directory.Exists(Path.GetDirectoryName(path)))
                        Directory.CreateDirectory(Path.GetDirectoryName(path));

                    using (FileStream fs = System.IO.File.Create(path))
                    {
                        file.CopyTo(fs);    //将上传的文件文件流，复制到fs中
                        fs.Flush();         //清空文件流
                    }
                    Thread.Sleep(1);
                    string newFileName = $@"{newName}{suffix}";
                    return new JsonResult(new { code = 200, msg = "上传成功", fileName = newFileName, urlImg = this._fileOptions.FileUrl });     //将新文件文件名回传给前端
                }
                else
                    return new JsonResult(new { code = 415, msg = "不支持此文件类型" });    //类型不正确
            }
            else
                return new JsonResult(new { code = 413, msg = $"文件大小不得超过{this._fileOptions.FileMaxSize / (1024f * 1024f)}M" });              //请求体过大，文件大小超标
        }

        /// <summary>上传文件-字符串方式
        /// </summary>
        /// <param name="jsonTxt">json字符串信息</param>
        /// <param name="newName">文件名(不含后缀)</param>
        /// <param name="suffix">文件名后缀</param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> PostFile_ByStr(dynamic value)
        {
            //提取参数
            //JObject pParams = JObject.FromObject(value);
            JObject pParams = JObject.Parse(value + "");
            if (pParams == null || pParams["jsonTxt"] + "" == "")
                return new JsonResult(new { code = 415, msg = "非有效Json格式参数！" });    //类型不正确

            string jsonTxt = pParams["jsonTxt"] + "";
            string newName = pParams["newName"] + "";
            string suffix = pParams["suffix"] + "";
            bool overwrite = Convert.ToBoolean(pParams["overwrite"]);
            if (string.IsNullOrEmpty(jsonTxt))
                return new JsonResult(new { code = 500, msg = "文件为null" });
            if (this._fileOptions.FileTypes.IndexOf(suffix) < 0)                        //检查文件格式
                return new JsonResult(new { code = 415, msg = "不支持此文件类型" });    //类型不正确

            //组装文件路径
            string strPath = Directory.GetCurrentDirectory() + $@"{this._fileOptions.FileBaseDir}/{newName}{suffix}";
            if (!Directory.Exists(Path.GetDirectoryName(strPath)))
                Directory.CreateDirectory(Path.GetDirectoryName(strPath));

            //写入文件
            if (!overwrite && System.IO.File.Exists(strPath))
                return new JsonResult(new { code = 200, msg = "文件已经存在" });
            System.IO.File.WriteAllText(strPath, jsonTxt);

            Thread.Sleep(1);
            string newFileName = $@"{newName}{suffix}";
            return new JsonResult(new { code = 200, msg = "上传成功", fileName = newFileName, urlImg = this._fileOptions.FileUrl });                //将新文件文件名回传给前端
        }

    }
}

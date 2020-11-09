using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using zpCore.MicroStation.Common;
using zpCore.MicroStation.Models;
namespace zpCore.MicroStation.Controllers
{
    [Route("api/[controller]")]
    //[ApiController]
    public class ImageUploadController : ControllerBase
    {
        private readonly PictureOptions _pictureOptions;
        public ImageUploadController(IOptions<PictureOptions> options) => this._pictureOptions = options.Value;

        /// <summary>
        /// 上传文件
        /// </summary>
        /// <param name="file">来自form表单的文件信息</param>
        /// <returns></returns>
        [HttpPost]
        public IActionResult Post([FromForm(Name = "file")] IFormFile file)
        {
            //var files = Request.Form.Files;
            if (file == null)
                return new JsonResult(new { code = 500, msg = "文件为null" });
            if (file.Length <= this._pictureOptions.MaxSize)                //检查文件大小
            {
                var suffix = Path.GetExtension(file.FileName);              //提取上传的文件文件后缀
                if (this._pictureOptions.FileTypes.IndexOf(suffix) >= 0)    //检查文件格式
                {
                    string newName = common.createName(this._pictureOptions.ImageBaseUrl, suffix);
                    string path = Directory.GetCurrentDirectory() + $@"{this._pictureOptions.ImageBaseUrl}/{newName}{suffix}";

                    using (FileStream fs = System.IO.File.Create(path))
                    {
                        file.CopyTo(fs);    //将上传的文件文件流，复制到fs中
                        fs.Flush();         //清空文件流
                    }
                    Thread.Sleep(1);
                    string newFileName = $@"{newName}{suffix}";
                    return new JsonResult(new { code = 200, msg = "上传成功", fileName = newFileName, urlImg = this._pictureOptions.ImageUrl });     //将新文件文件名回传给前端
                }
                else
                    return new JsonResult(new { code = 415, msg = "不支持此文件类型" });    //类型不正确
            }
            else
                return new JsonResult(new { code = 413, msg = $"文件大小不得超过{this._pictureOptions.MaxSize / (1024f * 1024f)}M" });              //请求体过大，文件大小超标
        }
    }

}

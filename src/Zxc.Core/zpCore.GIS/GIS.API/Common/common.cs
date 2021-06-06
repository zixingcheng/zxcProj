using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace zpCore.GIS.API.Common
{
    public class common
    {
        public static int rand = 0;

        /// <summary> 返回Json串(不带双引号)
        /// </summary>
        /// <param name="value"></param>
        /// <returns></returns>
        public static ActionResult<string> transResult(dynamic objDatas, dynamic objMsg = null, bool objSuccess = true, int errCode = 0)
        {
            var data = new { code = errCode, is_success = objSuccess, msg = objMsg, datas = objDatas };
            var result = JsonConvert.SerializeObject(new { data = data });
            return new ContentResult { Content = result, ContentType = "application/json" };
        }
        public static JObject transResult_page(int pageInd, int pageSize, int pageCount)
        {
            JObject objRes = new JObject();
            objRes["pageInfo "] = new JObject();
            objRes["pageInfo "]["pageInd"] = pageInd;
            objRes["pageInfo "]["pageSize"] = pageSize;
            objRes["pageInfo "]["pageCount"] = (int)Math.Ceiling(pageCount * 1.0 / pageSize);
            return objRes;
        }


        /// <summary>通用转换（将绝对路径转换为网页路径）
        /// </summary>
        /// <param name="result"></param>
        /// <returns></returns>
        public static ActionResult<string> transResult_zpService(string result)
        {
            JObject objRes = (JObject)JsonConvert.DeserializeObject(result);
            string dirBase = Directory.GetCurrentDirectory().Replace("\\", "/").Replace("//", "/") + "/wwwroot";

            //转换所有路径为rul路径
            if (objRes["datas"] != null)
            {
                if (objRes["datas"]["path"] != null)        //结果文件路径
                    objRes["datas"]["path"] = objRes["datas"]["path"].ToString().Replace(dirBase, "/src");

                if (objRes["datas"]["outFile"] != null)     //输出文件路径
                    objRes["datas"]["outFile"] = objRes["datas"]["outFile"].ToString().Replace(dirBase, "/src");
            }

            if (objRes["renderer"] != null)
                if (objRes["renderer"]["renderer"]["route"] != null)     //渲染文件路由
                    objRes["renderer"]["renderer"]["route"] = objRes["renderer"]["renderer"]["route"].ToString().Replace(dirBase, "/src");

            result = JsonConvert.SerializeObject(objRes);
            return new ContentResult { Content = result, ContentType = "application/json" };
        }

        public static string createName(string baseDirect, string suffix)
        {
            rand += 1;
            int ind = rand;
            Console.WriteLine(ind.ToString());
            DateTime dtNow = DateTime.Now;
            string newName = $@"file_{dtNow:yyyyMMdd}_{dtNow:HHmm}_{dtNow:ssffff}_" + ind.ToString();
            string path = $@"{baseDirect}/{newName}{suffix}";

            while (Directory.Exists(path))
            {
                dtNow.AddMilliseconds(1);
                newName = $@"file_{dtNow:yyyyMMdd}_{dtNow:HHmm}_{dtNow:ssffff}";
                path = $@"{baseDirect}/{newName}{suffix}";
            }
            if (rand > 1000) rand = 0;
            return newName;
        }
    }
}

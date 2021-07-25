using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Threading.Tasks;

namespace zxcCore.Common
{
    public static class zxcNetHelper
    {
        /// <summary>Post方式调用webAPI或页面
        /// </summary>
        /// <param name="url">url地址</param>
        /// <param name="postData">json格式数据</param>
        /// <param name="statusCode">状态码</param
        /// <param name="headers">请求头</param>
        /// <param name="charSet">编码格式</param>
        /// <returns></returns>
        public static string Post_ByHttpClient(string url, string postData, out string statusCode, string headers = "application/json", string charSet = "utf-8")
        {
            //设置Http的正文、内容标头、字符
            HttpContent httpContent = new StringContent(postData, Encoding.UTF8, "application/json");
            if (headers != "application/json")
            {
                httpContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue(headers);
                if (!string.IsNullOrEmpty(postData))
                    url += postData;
            }
            if (charSet != "utf-8")
                httpContent.Headers.ContentType.CharSet = "utf-8";

            string result = string.Empty;
            using (HttpClient httpClient = new HttpClient())
            {
                //异步Post
                HttpResponseMessage response = httpClient.PostAsync(url, httpContent).Result;
                statusCode = response.StatusCode.ToString();    //输出Http响应状态码
                if (response.IsSuccessStatusCode)               //确保Http响应成功
                {
                    //异步读取json
                    result = response.Content.ReadAsStringAsync().Result;
                    //Task<string> t = response.Content.ReadAsStringAsync();
                    //if (t != null)
                    //{
                    //    return t.Result;
                    //}
                }
            }
            return result;
        }

        /// <summary>Get方式调用webAPI或页面
        /// </summary>
        /// <param name="url">url地址</param>
        /// <param name="postData">json格式数据</param>
        /// <param name="statusCode">状态码</param>
        /// <returns></returns>
        public static string Get_ByHttpClient(string url, string postData, out string statusCode)
        {
            string result = string.Empty;
            using (HttpClient httpClient = new HttpClient())
            {
                //异步Post
                HttpResponseMessage response = httpClient.GetAsync(url + postData).Result;
                statusCode = response.StatusCode.ToString();    //输出Http响应状态码
                if (response.IsSuccessStatusCode)               //确保Http响应成功
                {
                    //异步读取json
                    result = response.Content.ReadAsStringAsync().Result;
                    //Task<string> t = response.Content.ReadAsStringAsync();
                    //if (t != null)
                    //{
                    //    return t.Result;
                    //}
                }
            }
            return result;
        }


        /// <summary>下载指定网络路径图片
        /// </summary>
        /// <param name="urlImage"></param>
        /// <returns></returns>
        public static byte[] Download_Image(string urlImage)
        {
            byte[] bytBuffer;
            HttpWebRequest myReq = (HttpWebRequest)WebRequest.Create(urlImage);
            myReq.Referer = urlImage;
            WebResponse myResp = myReq.GetResponse();

            Stream stream = myResp.GetResponseStream();
            using (BinaryReader br = new BinaryReader(stream))
            {
                //i = (int)(stream.Length);
                bytBuffer = br.ReadBytes(500000);
                br.Close();
            }
            myResp.Close();
            return bytBuffer;
        }

    }
}
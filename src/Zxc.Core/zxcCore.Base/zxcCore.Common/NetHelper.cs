using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace zxcCore.Common
{
    public static class NetHelper
    {
        /// <summary>Post方式调用webAPI或页面
        /// </summary>
        /// <param name="url">url地址</param>
        /// <param name="postData">json格式数据</param>
        /// <param name="statusCode">状态码</param>
        /// <returns></returns>
        public static string Post_ByHttpClient(string url, string postData, out string statusCode)
        {
            //设置Http的正文、内容标头、字符
            HttpContent httpContent = new StringContent(postData);
            httpContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/json");
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

    }
}
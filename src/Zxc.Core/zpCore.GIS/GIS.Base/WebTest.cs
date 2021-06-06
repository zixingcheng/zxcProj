using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using zpCore.zpGis_BasezpCore.Algorithm;

namespace zpCore.zpGis_Base
{
    public class test
    {
        CookieCollection cookie;

        public string HttpClient()
        {
            var url = "https://haokan.baidu.com/videoui/api/videolike";
            var secret = "123456";//假如有 basic 头   jwt
            var post = new
            {
                rl_key = 8288051597031451712,
                vid = 8288051597031451712,
                bs = "haokan_detailpage",
                type = 0,
            };

            //test2.openURl("https://haokan.baidu.com/v?vid=8288051597031451712&tab=");
            //test2.postData("https://haokan.baidu.com", "/videoui/api/videolike", "");

            //body属性传值
            var str = string.Format("rl_key={0}&vid={1}&bs={2}&type={3}", post.rl_key, post.vid, post.bs, post.type);

            // Json属性传值JsonConvert.SerializeObject(post);
            byte[] bytes = Encoding.UTF8.GetBytes(secret);
            var authstr = Convert.ToBase64String(bytes);//basic 认证字符串
            ASCIIEncoding encoding = new ASCIIEncoding();
            byte[] byte1 = encoding.GetBytes(str);//获取header 中的length大小
            HttpContent httpContent = new StringContent(str);//转换body内容对象

            //如果是json模式HttpContent httpContent = new StringContent(str,Encoding.UTF8, "application/json");
            httpContent.Headers.Expires = DateTime.Now;
            httpContent.Headers.ContentType = new MediaTypeHeaderValue("application/x-www-form-urlencoded");
            //json  httpContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");
            httpContent.Headers.ContentLength = byte1.Length;
            httpContent.Headers.ContentType.CharSet = "utf-8";

            HttpClient httpClient = new HttpClient();
            httpClient.BaseAddress = new Uri(url);
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", authstr);
            httpClient.Timeout = new TimeSpan(0, 0, 10);

            HttpResponseMessage response = httpClient.PostAsync(url, httpContent).Result;
            if (response.IsSuccessStatusCode)
            {
                return response.Content.ReadAsStringAsync().Result;
                //结果对象化
                //var result = JsonConvert.DeserializeObject<SuccessResult>(response.Content.ReadAsStringAsync().Result);
            }
            else
            {
                //相应失败结果对象化  这里推荐读一下反应流，否则你只知道是几百错误不知道具体原因
                //var rel = JsonConvert.DeserializeObject<ErrorMsg>(response.Content.ReadAsStringAsync().Result);
                return response.Content.ReadAsStringAsync().Result;
            }
        }


        /// <summary>
        /// 发送登录信息，进行登录
        /// </summary>
        public void Login_Click()
        {
            // 设置登录信息
            string url = "https://baijiahao.baidu.com/builder/theme/bjh/login";
            string postData = "";

            // 发送post信息，进行登录
            string html = HttpTool.GetHtml(url, postData, Method.POST, out cookie);

            if (cookie.Count > 0)
            {
                Console.WriteLine("您已成功登录！");
            }
        }

        /// <summary>
        /// 获取其他页面数据信息(登录成功后,或不需要登录)
        /// </summary>
        public void getURL(string url)
        {
            string data = HttpTool.GetHtml(url);   // 实时获取网页数据
            Console.WriteLine(data);
        }

        /// <summary>
        /// 登录成功后，在浏览器中打开url
        /// </summary>
        public void openURl(string url)
        {
            HttpTool.openUrl(url);
            //System.Diagnostics.Process.Start(url); //直接可以访问的网页打开方式
        }
        public void postData(string urlOrigin, string urlPath, dynamic postData)
        {
            postData = "rl_key=8288051597031451712&vid=8288051597031451712&bs=haokan_detailpage&type=0";

            // 发送post信息
            CookieCollection cookie;
            string html = HttpTool.GetHtml(urlOrigin + urlPath, postData, Method.POST, out cookie);

            if (cookie.Count > 0)
            {
                Console.WriteLine("已完成Post请求！");
            }
            //System.Diagnostics.Process.Start(url); //直接可以访问的网页打开方式
        }
    }

    public enum Method
    {
        POST = 0,
        GET = 1
    }

    /// <summary>
    /// 用于发送http请求，访问WEB页面
    /// </summary>
    public class HttpTool   //此类参考：http://blog.csdn.net/htsnoopy/article/details/7094224
    {
        #region 设置信息

        public static CookieContainer cookie = new CookieContainer();           // 用于记录访问网页时cookie数据
        public static CookieCollection cookieCollection;

        private static string ContentType = "application/x-www-form-urlencoded";
        private static string Accept = "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5";
        private static string UserAgent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14";

        public static void setting(string contentType, string accept, string userAgent)
        {
            ContentType = contentType;
            Accept = accept;
            UserAgent = userAgent;
        }

        public static void setting(CookieContainer cc, string contentType, string accept, string userAgent)
        {
            cookie = cc;
            ContentType = contentType;
            Accept = accept;
            UserAgent = userAgent;
        }

        /// <summary>
        /// 清空cookie数据
        /// </summary>
        public static void clearCookie()
        {
            cookie = new CookieContainer();
        }

        #endregion


        #region 网页数据获取的获取

        /// <summary>
        /// 获取指定的网页数据（不需要登录，可以直接访问的页面；或已登录）
        /// </summary>
        public static string GetHtml(string url)
        {
            return GetHtml(url, out cookieCollection);
        }

        /// <summary>
        /// 获取指定的网页数据（不需要登录，可以直接访问的页面）
        /// </summary>
        public static string GetHtml(string url, out CookieCollection cookieCollection)
        {
            try
            {
                HttpWebRequest httpWebRequest;

                httpWebRequest = (HttpWebRequest)HttpWebRequest.Create(url);
                httpWebRequest.CookieContainer = cookie;

                HttpWebResponse httpWebResponse;
                httpWebResponse = (HttpWebResponse)httpWebRequest.GetResponse();
                Stream responseStream = httpWebResponse.GetResponseStream();
                StreamReader streamReader = new StreamReader(responseStream, Encoding.UTF8);
                string html = streamReader.ReadToEnd();
                streamReader.Close();
                responseStream.Close();

                cookieCollection = cookie.GetCookies(new Uri(url));

                return html;
            }
            catch (Exception)
            {
                cookieCollection = null;
                return null;
            }
        }
        #endregion


        #region 需要验证帐号信息的网页，数据获取

        /// <summary>
        /// post数据到指定的网址，获取cookie数据，和返回页
        /// </summary>
        public static string GetHtml(string url, string postData, Method method)
        {
            return GetHtml(url, postData, method, out cookieCollection);
        }

        /// <summary>
        /// post数据到指定的网址，获取cookie数据，和返回页
        /// </summary>
        public static string GetHtml(string url, string postData, Method method, out CookieCollection cookieCollection)
        {
            try
            {
                if (string.IsNullOrEmpty(postData))
                {
                    cookieCollection = cookie.GetCookies(new Uri(url));
                    return GetHtml(url, out cookieCollection);
                }

                byte[] byteRequest = Encoding.Default.GetBytes(postData);

                HttpWebRequest httpWebRequest;
                httpWebRequest = (HttpWebRequest)HttpWebRequest.Create(url);

                httpWebRequest.CookieContainer = cookie;
                httpWebRequest.ContentType = ContentType;

                httpWebRequest.Referer = url;
                httpWebRequest.Accept = Accept;
                httpWebRequest.UserAgent = UserAgent;
                httpWebRequest.Method = method == Method.POST ? "POST" : "GET";
                httpWebRequest.ContentLength = byteRequest.Length;

                Stream stream = httpWebRequest.GetRequestStream();
                stream.Write(byteRequest, 0, byteRequest.Length);
                stream.Close();

                HttpWebResponse httpWebResponse;
                httpWebResponse = (HttpWebResponse)httpWebRequest.GetResponse();
                Stream responseStream = httpWebResponse.GetResponseStream();
                StreamReader streamReader = new StreamReader(responseStream, Encoding.UTF8);
                string html = streamReader.ReadToEnd();
                streamReader.Close();
                responseStream.Close();

                cookieCollection = cookie.GetCookies(new Uri(url));

                return html;
            }
            catch (Exception)
            {
                cookieCollection = null;
                return null;
            }
        }

        /// <summary>
        /// 登录成功后，在浏览器中打开指定的url
        /// </summary>
        public static void openUrl(string url)
        {
            openUrl(cookieCollection, url);
        }

        public static void openUrl(CookieCollection cookieCollection, string url)
        {
            string tmp = "";
            for (int i = 0; i < cookieCollection.Count; i++)
            {
                Cookie c = cookieCollection[i];
                tmp += (tmp.Equals("") ? "" : "&") + c.Name.ToString() + "=" + c.Value.ToString();
            }

            Process.Start(url + "?" + tmp);
        }

        #endregion

    }
}

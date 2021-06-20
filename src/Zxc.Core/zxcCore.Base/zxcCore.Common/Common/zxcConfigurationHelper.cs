using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using System;
using System.IO;

namespace zxcCore.Common
{
    public static class zxcConfigHelper
    {
        private static zxcConfigurationHelper ConfigurationHelper = null;
        static zxcConfigHelper()
        {
            ConfigurationHelper = new zxcConfigurationHelper();
        }

        /// <summary>
        /// 根据key获取对应的配置值
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public static string GetValue(string key)
        {
            return ConfigurationHelper.config[key];
        }

        /// <summary>
        /// 获取ConnectionStrings下默认的配置连接字符串
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public static string GetConnectionString(string key)
        {
            return ConfigurationHelper.config.GetConnectionString(key);
        }
    }

    public class zxcConfigurationHelper
    {
        public IConfiguration config { get; set; }
        public zxcConfigurationHelper(string fileName = "appsettings.json")
        {
            var builder = new ConfigurationBuilder();       //创建config的builder
            builder.SetBasePath(Directory.GetCurrentDirectory()).AddJsonFile(fileName);       //设置配置文件所在的路径加载配置文件信息
            config = builder.Build();
        }
        //public T GetAppSettings<T>(string key) where T : class, new()
        //{
        //    var appconfig = new ServiceCollection()
        //        .AddOptions()
        //        .Configure<T>(config.GetSection(key))
        //        .BuildServiceProvider()
        //        .GetService<IOptions<T>>()
        //        .Value;
        //    return appconfig;
        //}
    }

    //我比较喜欢单独放这个类，但是这样放更明显
    public class MyServiceProvider
    {
        public static IServiceProvider ServiceProvider { get; set; }
    }

}
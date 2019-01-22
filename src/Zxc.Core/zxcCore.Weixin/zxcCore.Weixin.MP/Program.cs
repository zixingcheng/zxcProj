using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace zxcCore.Weixin.MP
{
    public class Program
    {
        public static void Main(string[] args)
        {
            BuildWebHost(args).Run();
        }

        public static IWebHost BuildWebHost(string[] args) =>
            WebHost.CreateDefaultBuilder(args)
                .UseKestrel()
                .UseContentRoot(Directory.GetCurrentDirectory())
                .UseIISIntegration()

                //如果不配置下面这条信息，会导致无法直接访问//当然不用下面这个可以用Nginx来配置
                .UseUrls("http://*:8670")
                .UseStartup<Startup>()
                .UseApplicationInsights()
                .Build();
    }
}

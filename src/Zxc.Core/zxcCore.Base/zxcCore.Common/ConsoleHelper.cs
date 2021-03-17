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
    public static class ConsoleHelper
    {
        public static bool ps_CanDebug = true;

        //打印信息输出
        public static void Print(string format, params object[] arg)
        {
            Console.WriteLine(format, arg);
        }

        //调试信息输出
        public static void Debug(string format, params object[] arg)
        {
            Console.WriteLine(format, arg);
        }

        //错误信息输出
        public static void Error(string format, params object[] arg)
        {
            Console.WriteLine(format, arg);
        }

    }
}
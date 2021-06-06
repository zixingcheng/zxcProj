using System;
using System.Collections.Generic;
using System.Threading;
using System.Linq;
using System.Diagnostics;
using zpCore.zpDataCache.Memory;
using zxcCore.zxcDataCache.Swap;
using zxcCore.zxcRobot.Monitor;
using zxcCore.zxcRobot.DataAnalysis;
using zxcCore.zxcRobot.Monitor.Quote;
using zxcCore.zxcRobot.User;
using zxcCore.zxcDataCache.MemoryDB;
using zxcCore.zxcDataCache.MemoryDB.Test;
using zxcCore.zxcRobot.Robot;

namespace zxcCore.zxcRobot.Test
{
    class Program
    {
        static void Main(string[] args)
        {
            //数据库测试
            TestDB();

            //机器人测试
            Robot_Manager._Manager.Start();
            while (true)
            {
                Thread.Sleep(2000);         //模拟长时间运算
            }
        }

        //消息交换测试
        static void Main2(string[] args)
        {

            Console.WriteLine("Hello World!");
            Data_Quote_Manager pManager = new Data_Quote_Manager();
            pManager.Start(-1, 1);


            //string dirSwap = @"D:\myCode\zxcProj\src\Zxc.Python\zxcPy.Robot.Spider\Data\Swaps";
            //DataSwap_IOFiles pSwap = new DataSwap_IOFiles("Quote", dirSwap, 0, typeof(Data_Quote));
            //pSwap.SwapData_Change += new DataSwapChange_EventHandler(Program.DataSwapChange_EventHandler);
            //List<dynamic> lstDatas = pSwap.SwapData_In();

            //pSwap.Start(-1, 5);
            //foreach (var item in lstDatas)
            //{
            //    Data_Quote pData = (Data_Quote)item;
            //    if (pData == null) continue;
            //}

            while (true)
            {
                Thread.Sleep(2000);         //模拟长时间运算
            }
        }

        //数据库测试
        private static void TestDB()
        {
            Stopwatch watch = new Stopwatch();

            //转化成Json
            watch.Start();
            Data_Table<DataModels_Test> dbTest = new Data_Table<DataModels_Test>();
            for (int i = 0; i < 100000; i++)
            {
                DataModels_Test obj = new DataModels_Test();
                obj.Id = i;
                obj.Id_str = i.ToString();

                dbTest.Add(obj, false);
            }
            string strJson = Newtonsoft.Json.JsonConvert.SerializeObject(dbTest);
            watch.Stop();
            Console.WriteLine("转化成Json（100000）耗时：" + watch.Elapsed.TotalMilliseconds);

            //反序列化
            watch.Restart();
            Data_Table<DataModels_Test> dbTest2 = Newtonsoft.Json.JsonConvert.DeserializeObject<Data_Table<DataModels_Test>>(strJson);
            Console.WriteLine("反序列化（100000）耗时：" + watch.Elapsed.TotalMilliseconds);


            //初始数据库
            Data_DB_Test _dbTest = new Data_DB_Test("D:/ftpData/DB_Test");

            //测试添加数据
            watch.Restart();
            _dbTest.Data_Test.Add(new DataModels_Test() { Id = 0, Id_str = "0" });
            _dbTest.Data_Test.SaveChanges();
            _dbTest.Data_Test.SaveChanges(true);

            watch.Stop();
            Console.WriteLine("单一添加耗时：" + watch.Elapsed.TotalMilliseconds);

            //单一添加测试
            for (int i = 0; i < 1000; i++)
            {
                DataModels_Test obj = new DataModels_Test();
                obj.Id = i;
                obj.Id_str = i.ToString();

                _dbTest.Data_Test.Add(obj, false);
            }
            watch.Stop();
            Console.WriteLine("单一添加耗时：" + watch.Elapsed.TotalMilliseconds);

            //多个添加测试
            List<DataModels_Test> lstTemp = new List<DataModels_Test>();
            for (int i = 0; i < 1000; i++)
            {
                DataModels_Test obj = new DataModels_Test();
                obj.Id = i;
                obj.Id_str = i.ToString();

                lstTemp.Add(obj);
            }
            _dbTest.Data_Test.AddRange(lstTemp);
            watch.Stop();
            Console.WriteLine("单一添加耗时：" + watch.Elapsed.TotalMilliseconds);


            //Name是传入的参数值
            watch.Restart();
            var query = dbTest2.Where(e => e.Id < 33 && e.Id > 15).ToList();
            watch.Stop();
            Console.WriteLine("查询耗时：" + watch.Elapsed.TotalMilliseconds);
        }
        private static void DataAnalyse()
        {
            //UserManager _Users = new UserManager("");

            Func<IEnumerable<User_zxc>, IEnumerable<User_zxc>> expr1 =
                   l => l.Where(n => n.usrName == "admin");
            User_zxc usr = UserManager._Users.GetUser(expr1);


            //初始数据分析对象
            DataAnalyse pDataAnalyse = new DataAnalyse("Test");
            pDataAnalyse.Init(37.31, 37.31, DateTime.Now, 37.31, 37.31, 0.0025);

            var datas1 = new List<double>() { 36.76, 37.0, 37.01, 37.0, 36.85, 36.98, 36.93, 36.99, 37.28, 37.27, 37.15, 37.07, 37.11, 37.12, 37.12, 37.03, 37.0, 36.9, 36.96, 36.96, 36.99, 36.95, 36.84, 36.52, 36.58, 36.7, 36.7, 36.82, 36.75, 36.65, 36.67, 36.72, 36.72, 36.72, 36.75, 36.8, 36.84, 36.86, 36.8, 36.77, 36.77, 36.77, 36.73, 36.72, 36.68, 36.69, 36.65, 36.61, 36.62, 36.64, 36.68, 36.7, 36.74, 36.8, 36.81, 36.78, 36.74, 36.79, 36.75, 36.72, 36.74, 36.73, 36.72, 36.72, 36.74, 36.71, 36.72, 36.7, 36.66, 36.64, 36.65, 36.62, 36.65, 36.66, 36.69, 36.69, 36.68, 36.69, 36.72, 36.75, 36.76, 36.75, 36.7, 36.71, 36.71, 36.73, 36.71, 36.71, 36.73, 36.68, 36.65, 36.61, 36.62, 36.63, 36.62, 36.62, 36.64, 36.63, 36.65, 36.64, 36.63, 36.62, 36.62, 36.62, 36.61, 36.58, 36.53, 36.52, 36.53, 36.54, 36.52, 36.54, 36.56, 36.59, 36.59, 36.59, 36.58, 36.56, 36.54, 36.54, 36.55, 36.57, 36.61, 36.6, 36.61, 36.62, 36.62, 36.59, 36.59, 36.58, 36.55, 36.56, 36.56, 36.57, 36.63, 36.7, 36.83, 37.0, 37.04, 37.01, 37.14, 37.31, 37.26, 37.12, 37.14, 37.1, 37.0, 36.98, 37.09, 37.06, 37.02, 37.06, 37.12, 37.29, 37.23, 37.15, 37.13, 37.3, 37.44, 37.53, 37.65, 37.48, 37.47, 37.57, 37.63, 37.53, 37.44, 37.36, 37.42, 37.44, 37.43, 37.32, 37.2, 37.2, 37.28, 37.35, 37.38, 37.37, 37.39, 37.32, 37.25, 37.32, 37.42, 37.47, 37.51, 37.54, 37.47, 37.47, 37.57, 37.6, 37.64, 37.74, 37.99, 38.32, 38.58, 38.86, 38.4, 38.43, 38.6, 38.55, 38.19, 38.12, 38.31, 38.46, 38.42, 38.26, 38.2, 38.3, 38.38, 38.47, 38.4, 38.38, 38.39, 38.33, 38.31, 38.28, 38.22, 38.3, 38.42, 38.49, 38.48, 38.46, 38.45, 38.5, 38.69, 38.87, 38.99, 39.02, 38.99, 38.8, 38.72, 38.77, 38.84, 38.86, 38.92, 38.89, 38.82, 38.78, 38.78, 38.78, 38.78 };


            //循环数据进行监测
            foreach (var item in datas1)
            {
                pDataAnalyse.Analysis(item, DateTime.Now);
            }

            Console.WriteLine("Hello World!");
            Data_Quote_Manager pManager = new Data_Quote_Manager();
            pManager.Start(-1, 1);


            //string dirSwap = @"D:\myCode\zxcProj\src\Zxc.Python\zxcPy.Robot.Spider\Data\Swaps";
            //DataSwap_IOFiles pSwap = new DataSwap_IOFiles("Quote", dirSwap, 0, typeof(Data_Quote));
            //pSwap.SwapData_Change += new DataSwapChange_EventHandler(Program.DataSwapChange_EventHandler);
            //List<dynamic> lstDatas = pSwap.SwapData_In();

            //pSwap.Start(-1, 5);
            //foreach (var item in lstDatas)
            //{
            //    Data_Quote pData = (Data_Quote)item;
            //    if (pData == null) continue;
            //}
        }

        //消息交换事件
        private static void DataSwapChange_EventHandler(object sender, DataSwap_Event e)
        {
            Console.WriteLine(DateTime.Now + "::");
            foreach (var item in e.Datas)
            {
                Data_Quote pData = (Data_Quote)item;
                if (pData == null) continue;
                Console.WriteLine("**********" + pData.Time);
            }
        }

    }
}

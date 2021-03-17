using System;
using System.Collections.Generic;
using System.Threading;
using zpCore.zpDataCache.Memory;
using zxcCore.zxcDataCache.Swap;
using zxcCore.zxcRobot.Monitor.Quote;

namespace zxcCore.zxcRobot.Test
{
    class Program
    {
        static void Main(string[] args)
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

        private static void DataSwapChange_EventHandler(object sender, DataSwap_EventArgs e)
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

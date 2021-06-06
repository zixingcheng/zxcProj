using System;
using zpCore.zpDataCache.Memory;
//using zpCore.zpDataCache.Check;
using zpCore.zpDataCache.Test;

namespace zpCore.zpDataCache.Test
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

            //测试因子及设置
            Console.WriteLine("测试因子及设置:");
            DateTime dtBase = DateTime.Now;
            IData_Factor poFactor = new Data_Factor("Factor_001", "Sdssf", "测试因子", "测试标准");
            IDataCache_Set poDataCache_Set = new DataCache_Set("", dtBase, typeTimeFrequency.None, 0, poFactor);

            //测试 DataCache
            Console.WriteLine("测试 DataCache:");
            DataCache<int> dataCache0 = new DataCache<int>("int002", typeTimeFrequency.Hour, 12, poDataCache_Set);
            dataCache0.Init(dtBase);
            dataCache0.SetData(dtBase, 10);
            dataCache0.SetData(dtBase.AddHours(1), 10);

            DataCache<Data_Iot<string>> dataCache2 = new DataCache<Data_Iot<string>>("Data_Iot001", typeTimeFrequency.Minute_1, 60, poDataCache_Set);
            dataCache2.Init(dtBase);
            dataCache2.SetData(dtBase, new Data_Iot<string>(dtBase, "10"));
            dataCache2.SetData(dtBase.AddMinutes(1), new Data_Iot<string>(dtBase.AddMinutes(1), "11"));
            dataCache2.SetData(dtBase.AddMinutes(5), new Data_Iot<string>(dtBase.AddMinutes(5), "15"));

            //测试 IDataCaches
            Console.WriteLine("测试 DataCaches:");
            IDataCaches dataCaches = new DataCaches(poFactor, poDataCache_Set);
            dataCaches.InitDataCache<int>("int002", typeTimeFrequency.Day, 6);
            dataCaches.InitDataCache<Data_Iot<string>>("Data_Iot002", typeTimeFrequency.Hour, 24);
            IDataCache<Data_Iot<string>> poDataCache2 = dataCaches.GetDataCache<Data_Iot<string>>("Data_Iot001", typeTimeFrequency.Minute_1);

            //测试 IDataCaches_Manage
            Console.WriteLine("测试 IDataCaches_Manage:");
            IData_Factors poFactors = new Data_Factors("Factors_001", "Sdssf", "测试因子", "测试标准");
            IDataCaches_Manage dataCaches_Manage = new DataCaches_Manage(poFactors, poDataCache_Set);
            dataCaches_Manage.InitDataCache<int>(poFactor, "manage001", typeTimeFrequency.Day, 7);
            dataCaches_Manage.SetData<int>(poFactor, "manage001", dtBase, 11, typeTimeFrequency.Day);
            int data = dataCaches_Manage.GetData<int>(poFactor, "manage001", dtBase, typeTimeFrequency.Day);

            //测试 DataCaches_Manager
            Console.WriteLine("测试 DataCaches_Manager:");
            DataCaches_Manager dataCaches_Manager = new DataCaches_Manager();
            dataCaches_Manager.Init(dtBase);
            dataCaches_Manager.InitDataCache<int>(poFactors, poFactor, "manage001", typeTimeFrequency.Day, 3);

            IData_Factors poFactors2 = new Data_Factors("Factors_002", "Nosdfsf", "测试因子2", "测试标准2");
            IData_Factor poFactor2 = new Data_Factor("Factor_002", "Sdssf02", "测试因子", "测试标准");
            IData_Factor poFactor3 = new Data_Factor("Factor_003", "Sdssf03", "测试因子", "测试标准");
            dataCaches_Manager.InitDataCache<Data_Iot<int>>(poFactors2, poFactor2, "manage002", typeTimeFrequency.Hour, 12);
            dataCaches_Manager.InitDataCache<Data_Iot<int>>(poFactors2, poFactor2, "manage002", typeTimeFrequency.Minute_1, 5);


            //测试 DataCheck_Test --缓存数据对象
            IDataCheck_Msger poMsger = new DataCheck_Msger_Test(false, 0);

            IDataCaches poDataCaches = dataCaches_Manager.GetDataCaches(poFactors2, poFactor2);
            IDataCache<Data_Iot<int>> poDataCache = poDataCaches.GetDataCache<Data_Iot<int>>("manage002", typeTimeFrequency.Hour);
            IDataChecks poDataChecks = new DataChecks_Test(poDataCache.ID, poDataCache, null, poMsger);
            poDataCache.InitDataChecks(poDataChecks);
            IDataCheck<Data_Iot<int>> poDataCheck = new DataCheck_Test<Data_Iot<int>>(poDataCache.ID, poDataCache);
            poDataChecks.InitDataCheck<Data_Iot<int>>(poDataCheck.Tag, poDataCheck, true);
            dataCaches_Manager.SetData<Data_Iot<int>>(poFactors2, poFactor2, "manage002", dtBase.AddHours(1), new Data_Iot<int>(dtBase, 11), typeTimeFrequency.Hour);

            //测试 DataCheck_Test --缓存数据集对象
            IDataChecks poDataChecks2 = new DataChecks_Test(poDataCaches.ID + "_2", poDataCaches);
            IDataCheck<Data_Iot<int>> poDataCheck2 = new DataCheck_Tests<Data_Iot<int>>(poDataCache.ID + "_2", poDataCache);
            poDataCaches.InitDataChecks(poDataChecks2);
            poDataCaches.InitDataCheck<Data_Iot<int>>(poDataCheck2.Tag, poDataCheck2);

            poDataChecks.InitDataChecks(poDataChecks2);     //设置因子的上级联动IDataChecks
            dataCaches_Manager.SetData<Data_Iot<int>>(poFactors2, poFactor2, "manage002", dtBase.AddHours(1), new Data_Iot<int>(dtBase, 9), typeTimeFrequency.Hour);

            //测试 DataCheck_Test --缓存数据集管理对象
            IDataChecks poDataChecks3 = new DataChecks_Test(poDataCaches.ID + "_3", poDataCaches);
            IDataCheck<Data_Iot<int>> poDataCheck3 = new DataCheck_TestM<Data_Iot<int>>(poDataCache.ID + "_3", poDataCache);
            IDataCaches_Manage poDataCaches_Manage = dataCaches_Manager.GetDataCaches_Manage(poFactors2);
            poDataCaches_Manage.InitDataChecks(poDataChecks3);
            poDataChecks3.InitDataCheck(poDataCheck3.Tag, poDataCheck3);
            poDataChecks2.InitDataChecks(poDataChecks3);     //设置因子集的上级联动IDataChecks
            dataCaches_Manager.SetData<Data_Iot<int>>(poFactors2, poFactor2, "manage002", dtBase.AddHours(1), new Data_Iot<int>(dtBase, 5), typeTimeFrequency.Hour);
            Data_Iot<int> pp = dataCaches_Manager.GetData<Data_Iot<int>>(poFactors2, poFactor2, "manage002", dtBase.AddHours(1), typeTimeFrequency.Hour);


            //压力测试         数据初始建议用 InitDatas 避免历史数据判断
            Console.WriteLine("测试  Stress testing!\n");
            Console.WriteLine("测试 初始：");
            DataCaches_Manager manager = new DataCaches_Manager();
            manager.Init(dtBase);
            DateTime dtStart0 = DateTime.Now;
            int factorsNums = 2000;
            int factorNums = 10;
            int factorTagNums = 5;
            int cachesNums = 10;
            int nsum0 = 0;
            for (int i = 0; i < factorsNums; i++)
            {
                IData_Factors pFactors = new Data_Factors("TestFactors_" + i.ToString(), "Factors_" + i.ToString(), i.ToString(), i.ToString());
                for (int j = 0; j < factorNums; j++)
                {
                    IData_Factor pFactor = new Data_Factor("TestFactor_" + j.ToString(), "Factor_" + j.ToString(), j.ToString(), j.ToString());

                    for (int k = 0; k < factorTagNums; k++)
                    {
                        manager.InitDataCache<Data_Iot<int>>(pFactors, pFactor, k.ToString(), typeTimeFrequency.Minute_1, cachesNums);
                        for (int kk = 0; kk < cachesNums; kk++)
                        {
                            Data_Iot<int> pData = new Data_Iot<int>(dtBase.AddMinutes(-kk), -kk);
                            manager.SetData<Data_Iot<int>>(pFactors, pFactor, k.ToString(), pData.Time, pData, typeTimeFrequency.Minute_1);
                            nsum0++;
                        }
                    }
                }
            }
            DateTime dtEnd0 = DateTime.Now;
            Console.WriteLine(string.Format("测试 初始耗时： {0} s.  {1}个, 频率 {2} 万/s", (dtEnd0 - dtStart0).TotalSeconds, nsum0, nsum0 / 10000 / (dtEnd0 - dtStart0).TotalSeconds));


            Console.WriteLine("测试 赋值：");
            DateTime dtStart1 = DateTime.Now;
            int nsum = 0, nStep = 1, nStpes = 10;
            for (int step = 0; step < nStpes; step++)
            {
                for (int i = 0; i < factorsNums; i++)
                {
                    for (int j = 0; j < factorNums; j++)
                    {
                        for (int k = 0; k < factorTagNums; k++)
                        {
                            for (int kk = 0; kk < cachesNums; kk++)
                            {
                                Data_Iot<int> pData = new Data_Iot<int>(dtBase.AddMinutes(nStep), nStep);
                                manager.SetData<Data_Iot<int>>("TestFactors_" + i.ToString(), "TestFactor_" + j.ToString(), k.ToString(), pData.Time, pData, typeTimeFrequency.Minute_1);
                                nsum++;
                            }
                        }
                    }
                }
            }
            nStep++;
            DateTime dtEnd1 = DateTime.Now;
            Console.WriteLine(string.Format("测试 赋值耗时： {0} s. {1}个, 频率 {2} 万/s", (dtEnd1 - dtStart1).TotalSeconds, nsum, nsum / 10000 / (dtEnd1 - dtStart1).TotalSeconds));

            Console.WriteLine("测试  ended!");



            //DatasCache_Manage_Iot<float> manager = new DatasCache_Manage_Iot<float>(DateTime.Now, (float)-1001.0001);
            //for (int i = 0; i < 10000; i++)
            //{
            //    manager.Init(i.ToString(), (float)-1001.0001);
            //}

            //// 模拟值（载入旧的）
            //IDataCache_Manage<float> datas = manager.GetData("1");
            //IDatas_Iot<float> data = datas.GetDatas(typeTimeFrequency.Hour);
            //DateTime dt = data.DataSet_TypeTime.Time_Start;
            //for (int i = 0; i < data.DataSet_TypeTime.Sum_Step + 2; i++)
            //{
            //    data.SetData(dt.AddHours(i), i);
            //}
            //Dictionary<int, IotDatas_Manage> datas = new Dictionary<int, IotDatas_Manage>();
            //for (int i = 0; i < 1; i++)
            //{
            //    IotDatas_Manage manage = new IotDatas_Manage();
            //    manage.Init();
            //    datas.Add(i, manage);
            //}
        }
    }
}

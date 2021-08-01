using Microsoft.Extensions.Hosting;
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace zxcCore.Common.JobTrigger
{
    /// <summary>管理Job任务
    /// </summary>
    public class JobMananger
    {
        public static Dictionary<string, IJobExecutor> psJobExecutors = new Dictionary<string, IJobExecutor>();

        public static bool Add(IJobExecutor jobExecutor)
        {
            if (jobExecutor != null)
            {
                psJobExecutors.Add(jobExecutor.GetType().Name, jobExecutor);
            }
            return true;
        }
        public static T Get<T>(string key)
        {
            IJobExecutor jobExecutor;
            psJobExecutors.TryGetValue(key, out jobExecutor);
            return (T)jobExecutor;
        }

    }
}
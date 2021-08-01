using Microsoft.Extensions.Hosting;
using System;
using System.Threading;
using System.Threading.Tasks;

namespace zxcCore.Common.JobTrigger
{
    public abstract class BaseJobTrigger
           : IHostedService, IDisposable
    {
        private Timer _timer;
        private readonly TimeSpan _dueTime;
        private readonly TimeSpan _periodTime;

        private readonly IJobExecutor _jobExcutor;

        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="dueTime">到期执行时间</param>
        /// <param name="periodTime">间隔时间</param>
        /// <param name="jobExcutor">任务执行者</param>
        protected BaseJobTrigger(TimeSpan dueTime,
             TimeSpan periodTime,
             IJobExecutor jobExcutor, bool cacheExcutor = false)
        {
            _dueTime = dueTime;
            _periodTime = periodTime;
            _jobExcutor = jobExcutor;
            if (cacheExcutor)
                JobMananger.Add(jobExcutor);
        }

        #region  计时器相关方法

        private void StartTimerTrigger()
        {
            if (_timer == null)
                _timer = new Timer(ExcuteJob, _jobExcutor, _dueTime, _periodTime);
            else
                _timer.Change(_dueTime, _periodTime);
        }

        private void StopTimerTrigger()
        {
            _timer?.Change(Timeout.Infinite, Timeout.Infinite);
        }

        private void ExcuteJob(object obj)
        {
            try
            {
                var excutor = obj as IJobExecutor;
                excutor?.StartJob();
            }
            catch (Exception e)
            {
                Console.WriteLine("Job Err::" + $"执行任务({nameof(GetType)})时出错，信息：{e}");
                //LogUtil.Error($"执行任务({nameof(GetType)})时出错，信息：{e}");
            }
        }

        #endregion

        /// <summary>
        ///  系统级任务执行启动
        /// </summary>
        /// <returns></returns>
        public virtual Task StartAsync(CancellationToken cancellationToken)
        {
            try
            {
                StartTimerTrigger();
            }
            catch (Exception e)
            {
                //LogUtil.Error($"启动定时任务({nameof(GetType)})时出错，信息：{e}");
            }
            return Task.CompletedTask;
        }

        /// <summary>
        ///  系统级任务执行关闭
        /// </summary>
        /// <returns></returns>
        public virtual Task StopAsync(CancellationToken cancellationToken)
        {
            try
            {
                _jobExcutor.StopJob();
                StopTimerTrigger();
            }
            catch (Exception e)
            {
                //LogUtil.Error($"停止定时任务({nameof(GetType)})时出错，信息：{e}");
            }
            return Task.CompletedTask;
        }

        public void Print(bool isStart = true)
        {
            string name = this.GetType().Name.Replace("Excutor", "");
            string prefix = isStart ? "Do" : "Done";
            Console.WriteLine(DateTime.Now.ToString("yy-MM-dd HH:mm:ss ") + prefix + " " + name + " ::");
        }
        public void Dispose()
        {
            _timer?.Dispose();
        }
    }

}

using Microsoft.Extensions.Hosting;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace zxcCore.Common.JobTrigger
{
    public abstract class JobExecutor
           : IJobExecutor
    {
        private readonly TimeSpan _dueTime;
        protected DateTime _endTime = DateTime.Now;
        protected bool _isStoping = false;
        protected bool _isInited = false;

        protected string m_dirFolder = "";
        protected string m_dirFolder_DataPump = "";
        protected DateTime m_dtDatetime_Start;
        protected DateTime m_dtDatetime_End;

        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="periodTime">间隔时间</param>
        /// <param name="jobExcutor">任务执行者</param>
        protected JobExecutor(TimeSpan dueTime)
        {
            _dueTime = dueTime;
            this.Init();
        }
        protected JobExecutor()
        {
        }
        public virtual void StartJob()
        {
        }
        public virtual void StopJob()
        {
            _isStoping = true;
            _isInited = false;
            //LogUtil.Info("系统终止任务");
        }


        public virtual bool Init()
        {
            _endTime = DateTime.Now + _dueTime;
            _isStoping = false;
            return true;
        }
        public virtual bool IsVaild()
        {
            if (_isStoping) return false;
            if (_dueTime.TotalSeconds > 0)
            {
                if (_endTime < DateTime.Now)
                {
                    _isStoping = true;
                    _isInited = false;
                    return false;
                }
            }
            return true;
        }

        public virtual void Print(bool isStart = true)
        {
            string name = this.GetType().Name.Replace("Excutor", "");
            string prefix = isStart ? "Do" : "Done";
            Console.WriteLine(DateTime.Now.ToString("yy-MM-dd HH:mm:ss ") + prefix + " " + name + " ::");
        }

        public virtual void Debug(string strOut)
        {
            Console.WriteLine(DateTime.Now.ToString("yy-MM-dd HH:mm:ss ") + strOut);
        }
    }
}
using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class TaskFeedback
    {
        public string TaskFeedbackOid { get; set; }
        public string Taskordeid { get; set; }
        public string Taskid { get; set; }
        public string Taskobjectname { get; set; }
        public string Supervision { get; set; }
        public ulong? Isitnecessarytorectify { get; set; }
        public ulong? Islawenforcementnecessary { get; set; }
        public ulong? Isitnecessarytopunish { get; set; }
        public string Picturenames { get; set; }
        public string TaskfeedbackpersonId { get; set; }
        public string Taskfeedbackperson { get; set; }
        public string Taskfeedbackpersonphone { get; set; }
        public int? Taskfeedbacktimes { get; set; }
        public DateTime? Taskfeedbacktime { get; set; }
        public string Tasktype { get; set; }
        public string Taskstatus { get; set; }
        public string TaskTypeSrc { get; set; }
        public string TaskTypesubSrc { get; set; }
    }
}

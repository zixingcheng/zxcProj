using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class TaskOrder
    {
        public string TaskOrderOid { get; set; }
        public string Taskid { get; set; }
        public string Tasktitle { get; set; }
        public string Tasktype { get; set; }
        public string Taskstatus { get; set; }
        public string Taskobjectname { get; set; }
        public string TaskTownStreet { get; set; }
        public string TaskCommunity { get; set; }
        public int? AlarmStationnumber { get; set; }
        public string AlarmStationname { get; set; }
        public string Alarmcontent { get; set; }
        public DateTime? Alarmtime { get; set; }
        public string Alarmfactor { get; set; }
        public string Tasksubobjectname { get; set; }
        public string TasksubTownStreet { get; set; }
        public string TasksubCommunity { get; set; }
        public string TasksubobjectOrgcode { get; set; }
        public string Tasksubobjectaddress { get; set; }
        public float? Contributionrate { get; set; }
        public int? Contributionrateranking { get; set; }
        public string Taskcontent { get; set; }
        public string Tasknotes { get; set; }
        public DateTime? Taskstarttime { get; set; }
        public DateTime? Taskdeadline { get; set; }
        public DateTime? Taskreceivingtime { get; set; }
        public ulong? Taskfallback { get; set; }
        public string Taskfallbackreason { get; set; }
        public DateTime? Taskfallbacktime { get; set; }
        public string Collectorid { get; set; }
        public string Collector { get; set; }
        public string Collectorphone { get; set; }
        public string CollectorunitId { get; set; }
        public string CollectorunitName { get; set; }
        public DateTime? Checktime { get; set; }
        public int? Taskfeedbacktimes { get; set; }
        public DateTime? Taskfeedbacktime { get; set; }
        public DateTime? Taskcompletetime { get; set; }
        public DateTime? Taskstatusupdatetime { get; set; }
        public string TaskTypeSrc { get; set; }
        public string TaskTypesubSrc { get; set; }
    }
}

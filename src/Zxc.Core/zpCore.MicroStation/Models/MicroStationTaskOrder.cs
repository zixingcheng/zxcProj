using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class MicroStationTaskOrder
    {
        public string MicroStationTaskOrderOid { get; set; }
        public string TaskId { get; set; }
        public string TaskTitle { get; set; }
        public string TaskType { get; set; }
        public string TaskStatus { get; set; }
        public string TaskStreet { get; set; }
        public string TaskCommunity { get; set; }
        public int? TaskSiteId { get; set; }
        public string TaskSiteName { get; set; }
        public string Tasker { get; set; }
        public string TaskContent { get; set; }
        public string TaskMark { get; set; }
        public DateTime? TaskTimeStart { get; set; }
        public DateTime? TaskTimeEnd { get; set; }
    }
}

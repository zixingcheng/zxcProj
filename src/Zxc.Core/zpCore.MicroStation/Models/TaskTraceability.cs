using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class TaskTraceability
    {
        public string TaskTraceabilityOid { get; set; }
        public string Taskordeid { get; set; }
        public string Taskid { get; set; }
        public int? Sitecode { get; set; }
        public string TargetName { get; set; }
        public string TownStreet { get; set; }
        public string OrgCode { get; set; }
        public string TargetAddr { get; set; }
        public int? PollutionRank { get; set; }
        public float? PollutionRate { get; set; }
    }
}

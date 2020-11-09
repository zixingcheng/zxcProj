using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class Infoalarm
    {
        public string InfoalarmOid { get; set; }
        public int DeployId { get; set; }
        public string AlarmType { get; set; }
        public string Alarmindex { get; set; }
        public string Alarmlevel { get; set; }
        public string Alarmtitle { get; set; }
        public string Alarmcontent { get; set; }
        public DateTime? Alarmtime { get; set; }
        public DateTime? AlarmtimeNormal { get; set; }
        public DateTime? AlarmtimeLast { get; set; }
        public DateTime? Datatime { get; set; }
        public string SrcOid { get; set; }
        public DateTime? Cratetime { get; set; }
    }
}

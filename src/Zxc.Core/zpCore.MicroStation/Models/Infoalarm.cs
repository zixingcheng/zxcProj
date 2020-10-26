using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class Infoalarm
    {
        public string InfoalarmOid { get; set; }
        public int? DeployId { get; set; }
        public string AlarmType { get; set; }
        public string Warningindex { get; set; }
        public string Alarmlevel { get; set; }
        public string Alarmcontent { get; set; }
        public DateTime? Alarmtime { get; set; }
        public DateTime? Cratetime { get; set; }
    }
}

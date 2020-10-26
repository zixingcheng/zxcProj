using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class MicroStation
    {
        public string MicroStationOid { get; set; }
        public int DeployId { get; set; }
        public string SiteName { get; set; }
        public string SiteType { get; set; }
        public string DeviceNumber { get; set; }
        public int? DeviceState { get; set; }
        public double Longitude { get; set; }
        public double Latitude { get; set; }
        public double? LongitudeBd { get; set; }
        public double? LatitudeBd { get; set; }
        public string StreetName { get; set; }
        public string CommunityName { get; set; }
        public string SiteNational { get; set; }
        public string Ownership { get; set; }
        public DateTime? SetupTime { get; set; }
    }
}

using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class KprDeviceDeploy
    {
        public int DeployId { get; set; }
        public int DeviceId { get; set; }
        public string DeviceNumber { get; set; }
        public string AddressDetail { get; set; }
        public decimal? Longitude { get; set; }
        public decimal? Latitude { get; set; }
        public int? ProvinceCode { get; set; }
        public string ProvinceName { get; set; }
        public int? CountyCode { get; set; }
        public string CountyName { get; set; }
        public int? CityCode { get; set; }
        public string CityName { get; set; }
    }
}

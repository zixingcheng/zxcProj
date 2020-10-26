using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class KprMonitorDataDeviceMinute
    {
        public long Id { get; set; }
        public DateTime Pubtime { get; set; }
        public int DeployId { get; set; }
        public string DeviceNumber { get; set; }
        public string AddressDetail { get; set; }
        public int ProvinceCode { get; set; }
        public string ProvinceName { get; set; }
        public int CityCode { get; set; }
        public string CityName { get; set; }
        public int CountyCode { get; set; }
        public string CountyName { get; set; }
        public int? StreetCode { get; set; }
        public string StreetName { get; set; }
        public decimal Latitude { get; set; }
        public decimal Longitude { get; set; }
        public decimal? Temperature { get; set; }
        public decimal? Humidity { get; set; }
        public decimal? Voc { get; set; }
        public decimal? WindSpeed { get; set; }
        public decimal? WindDirection { get; set; }
        public decimal? Pm25 { get; set; }
        public decimal? Pm10 { get; set; }
        public decimal? No2 { get; set; }
        public decimal? O3 { get; set; }
        public decimal? So2 { get; set; }
        public decimal? Co { get; set; }
        public int? Aqi { get; set; }
        public decimal? AirPressure { get; set; }
        public DateTime UpdateDt { get; set; }
        public DateTime CreateDt { get; set; }
    }
}

using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

namespace zpCore.MicroStation.Models
{
    public partial class dg_dbContext : DbContext
    {
        public dg_dbContext()
        {
        }

        public dg_dbContext(DbContextOptions<dg_dbContext> options)
            : base(options)
        {
        }

        public virtual DbSet<KprDeviceDeploy> KprDeviceDeploy { get; set; }
        public virtual DbSet<KprMonitorDataDeviceDay> KprMonitorDataDeviceDay { get; set; }
        public virtual DbSet<KprMonitorDataDeviceHour> KprMonitorDataDeviceHour { get; set; }
        public virtual DbSet<KprMonitorDataDeviceMinute> KprMonitorDataDeviceMinute { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. See http://go.microsoft.com/fwlink/?LinkId=723263 for guidance on storing connection strings.
                optionsBuilder.UseMySql("server=8.129.80.187;userid=dbuser_dg;pwd=kPr@2020#!dGCambRi;port=3306;database=dg_db;sslmode=none", x => x.ServerVersion("5.7.28-mysql"));
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<KprDeviceDeploy>(entity =>
            {
                entity.HasKey(e => e.DeployId)
                    .HasName("PRIMARY");

                entity.ToTable("kpr_device_deploy");

                entity.HasIndex(e => e.DeviceNumber)
                    .HasName("device_number")
                    .IsUnique();

                entity.Property(e => e.DeployId)
                    .HasColumnName("deploy_id")
                    .HasColumnType("int(11)");

                entity.Property(e => e.AddressDetail)
                    .HasColumnName("address_detail")
                    .HasColumnType("varchar(500)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.CityCode)
                    .HasColumnName("city_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CityName)
                    .HasColumnName("city_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_bin");

                entity.Property(e => e.CountyCode)
                    .HasColumnName("county_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CountyName)
                    .HasColumnName("county_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_bin");

                entity.Property(e => e.DeviceId)
                    .HasColumnName("device_id")
                    .HasColumnType("int(11)");

                entity.Property(e => e.DeviceNumber)
                    .HasColumnName("device_number")
                    .HasColumnType("varchar(50)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_bin");

                entity.Property(e => e.Latitude)
                    .HasColumnName("latitude")
                    .HasColumnType("decimal(16,6)");

                entity.Property(e => e.Longitude)
                    .HasColumnName("longitude")
                    .HasColumnType("decimal(16,6)");

                entity.Property(e => e.ProvinceCode)
                    .HasColumnName("province_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.ProvinceName)
                    .HasColumnName("province_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_bin");
            });

            modelBuilder.Entity<KprMonitorDataDeviceDay>(entity =>
            {
                entity.ToTable("kpr_monitor_data_device_day");

                entity.HasIndex(e => new { e.Pubtime, e.DeployId })
                    .HasName("pubtime_deploy_id");

                entity.HasIndex(e => new { e.Pubtime, e.DeviceNumber })
                    .HasName("pubtime_device_number")
                    .IsUnique();

                entity.Property(e => e.Id)
                    .HasColumnName("id")
                    .HasColumnType("bigint(20)");

                entity.Property(e => e.AddressDetail)
                    .IsRequired()
                    .HasColumnName("address_detail")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.AirPressure)
                    .HasColumnName("air_pressure")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Aqi)
                    .HasColumnName("aqi")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CityCode)
                    .HasColumnName("city_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CityName)
                    .IsRequired()
                    .HasColumnName("city_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Co)
                    .HasColumnName("co")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.CountyCode)
                    .HasColumnName("county_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CountyName)
                    .IsRequired()
                    .HasColumnName("county_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.CreateDt)
                    .HasColumnName("create_dt")
                    .HasColumnType("timestamp")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.DeployId)
                    .HasColumnName("deploy_id")
                    .HasColumnType("int(11)");

                entity.Property(e => e.DeviceNumber)
                    .IsRequired()
                    .HasColumnName("device_number")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Humidity)
                    .HasColumnName("humidity")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Latitude)
                    .HasColumnName("latitude")
                    .HasColumnType("decimal(16,6)");

                entity.Property(e => e.Longitude)
                    .HasColumnName("longitude")
                    .HasColumnType("decimal(16,6)");

                entity.Property(e => e.No2)
                    .HasColumnName("no2")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.O3)
                    .HasColumnName("o3")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.O38h)
                    .HasColumnName("o3_8h")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Pm10)
                    .HasColumnName("pm10")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Pm25)
                    .HasColumnName("pm2_5")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.ProvinceCode)
                    .HasColumnName("province_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.ProvinceName)
                    .IsRequired()
                    .HasColumnName("province_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Pubtime)
                    .HasColumnName("pubtime")
                    .HasColumnType("datetime");

                entity.Property(e => e.So2)
                    .HasColumnName("so2")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.StreetCode)
                    .HasColumnName("street_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.StreetName)
                    .HasColumnName("street_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Temperature)
                    .HasColumnName("temperature")
                    .HasColumnType("decimal(16,1)");

                entity.Property(e => e.UpdateDt)
                    .HasColumnName("update_dt")
                    .HasColumnType("timestamp")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.Voc)
                    .HasColumnName("voc")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.WindDirection)
                    .HasColumnName("wind_direction")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.WindSpeed)
                    .HasColumnName("wind_speed")
                    .HasColumnType("decimal(16,4)");
            });

            modelBuilder.Entity<KprMonitorDataDeviceHour>(entity =>
            {
                entity.ToTable("kpr_monitor_data_device_hour");

                entity.HasIndex(e => new { e.Pubtime, e.DeployId })
                    .HasName("pubtime_deploy_id");

                entity.HasIndex(e => new { e.Pubtime, e.DeviceNumber })
                    .HasName("pubtime_device_number")
                    .IsUnique();

                entity.Property(e => e.Id)
                    .HasColumnName("id")
                    .HasColumnType("bigint(20)");

                entity.Property(e => e.AddressDetail)
                    .IsRequired()
                    .HasColumnName("address_detail")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.AirPressure)
                    .HasColumnName("air_pressure")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Aqi)
                    .HasColumnName("aqi")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CityCode)
                    .HasColumnName("city_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CityName)
                    .IsRequired()
                    .HasColumnName("city_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Co)
                    .HasColumnName("co")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.CountyCode)
                    .HasColumnName("county_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CountyName)
                    .IsRequired()
                    .HasColumnName("county_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.CreateDt)
                    .HasColumnName("create_dt")
                    .HasColumnType("timestamp")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.DeployId)
                    .HasColumnName("deploy_id")
                    .HasColumnType("int(11)");

                entity.Property(e => e.DeviceNumber)
                    .IsRequired()
                    .HasColumnName("device_number")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Humidity)
                    .HasColumnName("humidity")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Latitude)
                    .HasColumnName("latitude")
                    .HasColumnType("decimal(16,6)");

                entity.Property(e => e.Longitude)
                    .HasColumnName("longitude")
                    .HasColumnType("decimal(16,6)");

                entity.Property(e => e.No2)
                    .HasColumnName("no2")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.O3)
                    .HasColumnName("o3")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.O38h)
                    .HasColumnName("o3_8h")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Pm10)
                    .HasColumnName("pm10")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Pm25)
                    .HasColumnName("pm2_5")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.ProvinceCode)
                    .HasColumnName("province_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.ProvinceName)
                    .IsRequired()
                    .HasColumnName("province_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Pubtime)
                    .HasColumnName("pubtime")
                    .HasColumnType("datetime");

                entity.Property(e => e.So2)
                    .HasColumnName("so2")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.StreetCode)
                    .HasColumnName("street_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.StreetName)
                    .HasColumnName("street_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Temperature)
                    .HasColumnName("temperature")
                    .HasColumnType("decimal(16,1)");

                entity.Property(e => e.UpdateDt)
                    .HasColumnName("update_dt")
                    .HasColumnType("timestamp")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.Voc)
                    .HasColumnName("voc")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.WindDirection)
                    .HasColumnName("wind_direction")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.WindSpeed)
                    .HasColumnName("wind_speed")
                    .HasColumnType("decimal(16,4)");
            });

            modelBuilder.Entity<KprMonitorDataDeviceMinute>(entity =>
            {
                entity.ToTable("kpr_monitor_data_device_minute");

                entity.HasIndex(e => new { e.Pubtime, e.DeployId })
                    .HasName("pubtime_deploy_id");

                entity.HasIndex(e => new { e.Pubtime, e.DeviceNumber })
                    .HasName("pubtime_device_number")
                    .IsUnique();

                entity.Property(e => e.Id)
                    .HasColumnName("id")
                    .HasColumnType("bigint(20)");

                entity.Property(e => e.AddressDetail)
                    .IsRequired()
                    .HasColumnName("address_detail")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.AirPressure)
                    .HasColumnName("air_pressure")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Aqi)
                    .HasColumnName("aqi")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CityCode)
                    .HasColumnName("city_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CityName)
                    .IsRequired()
                    .HasColumnName("city_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Co)
                    .HasColumnName("co")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.CountyCode)
                    .HasColumnName("county_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.CountyName)
                    .IsRequired()
                    .HasColumnName("county_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.CreateDt)
                    .HasColumnName("create_dt")
                    .HasColumnType("timestamp")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.DeployId)
                    .HasColumnName("deploy_id")
                    .HasColumnType("int(11)");

                entity.Property(e => e.DeviceNumber)
                    .IsRequired()
                    .HasColumnName("device_number")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Humidity)
                    .HasColumnName("humidity")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Latitude)
                    .HasColumnName("latitude")
                    .HasColumnType("decimal(16,6)");

                entity.Property(e => e.Longitude)
                    .HasColumnName("longitude")
                    .HasColumnType("decimal(16,6)");

                entity.Property(e => e.No2)
                    .HasColumnName("no2")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.O3)
                    .HasColumnName("o3")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Pm10)
                    .HasColumnName("pm10")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.Pm25)
                    .HasColumnName("pm2_5")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.ProvinceCode)
                    .HasColumnName("province_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.ProvinceName)
                    .IsRequired()
                    .HasColumnName("province_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Pubtime)
                    .HasColumnName("pubtime")
                    .HasColumnType("datetime");

                entity.Property(e => e.So2)
                    .HasColumnName("so2")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.StreetCode)
                    .HasColumnName("street_code")
                    .HasColumnType("int(11)");

                entity.Property(e => e.StreetName)
                    .HasColumnName("street_name")
                    .HasColumnType("varchar(100)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Temperature)
                    .HasColumnName("temperature")
                    .HasColumnType("decimal(16,1)");

                entity.Property(e => e.UpdateDt)
                    .HasColumnName("update_dt")
                    .HasColumnType("timestamp")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.Voc)
                    .HasColumnName("voc")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.WindDirection)
                    .HasColumnName("wind_direction")
                    .HasColumnType("decimal(16,4)");

                entity.Property(e => e.WindSpeed)
                    .HasColumnName("wind_speed")
                    .HasColumnType("decimal(16,4)");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}

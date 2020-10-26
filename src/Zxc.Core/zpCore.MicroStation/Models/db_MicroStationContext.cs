using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

namespace zpCore.MicroStation.Models
{
    public partial class db_MicroStationContext : DbContext
    {
        public db_MicroStationContext()
        {
        }

        public db_MicroStationContext(DbContextOptions<db_MicroStationContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Infoalarm> Infoalarm { get; set; }
        public virtual DbSet<MicroStation> MicroStation { get; set; }
        public virtual DbSet<MicroStationTaskOrder> MicroStationTaskOrder { get; set; }
        public virtual DbSet<TaskFeedback> TaskFeedback { get; set; }
        public virtual DbSet<TaskOrder> TaskOrder { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. See http://go.microsoft.com/fwlink/?LinkId=723263 for guidance on storing connection strings.
                optionsBuilder.UseMySql("server=120.197.152.99;userid=zpkj;pwd=Zp.666888!@#;port=8606;database=db_MicroStation;sslmode=none", x => x.ServerVersion("5.7.32-mysql"));
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Infoalarm>(entity =>
            {
                entity.HasKey(e => e.InfoalarmOid)
                    .HasName("PRIMARY");

                entity.ToTable("infoalarm");

                entity.HasIndex(e => e.InfoalarmOid)
                    .HasName("infoalarmIndex")
                    .IsUnique();

                entity.Property(e => e.InfoalarmOid)
                    .HasColumnName("infoalarmOID")
                    .HasColumnType("varchar(36)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.AlarmType)
                    .HasColumnType("varchar(30)")
                    .HasComment("告警类型")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Alarmcontent)
                    .HasColumnType("varchar(200)")
                    .HasComment("告警内容")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Alarmlevel)
                    .HasColumnType("varchar(10)")
                    .HasComment("告警等级")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Alarmtime)
                    .HasColumnType("datetime")
                    .HasComment("告警时间");

                entity.Property(e => e.Cratetime)
                    .HasColumnType("datetime")
                    .HasComment("创建时间");

                entity.Property(e => e.DeployId)
                    .HasColumnName("deploy_id")
                    .HasColumnType("int(11)")
                    .HasComment("告警站点");

                entity.Property(e => e.Warningindex)
                    .HasColumnType("varchar(20)")
                    .HasComment("告警指标")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");
            });

            modelBuilder.Entity<MicroStation>(entity =>
            {
                entity.HasKey(e => e.MicroStationOid)
                    .HasName("PRIMARY");

                entity.ToTable("microStation");

                entity.HasIndex(e => e.MicroStationOid)
                    .HasName("microStationIndex")
                    .IsUnique();

                entity.Property(e => e.MicroStationOid)
                    .HasColumnName("microStationOID")
                    .HasColumnType("varchar(36)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.CommunityName)
                    .IsRequired()
                    .HasColumnName("community_name")
                    .HasColumnType("varchar(50)")
                    .HasComment("社区名称")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.DeployId)
                    .HasColumnName("deploy_id")
                    .HasColumnType("int(11)")
                    .HasComment("站点编号");

                entity.Property(e => e.DeviceNumber)
                    .IsRequired()
                    .HasColumnName("device_number")
                    .HasColumnType("varchar(30)")
                    .HasComment("设备编码")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.DeviceState)
                    .HasColumnName("device_state")
                    .HasColumnType("int(11)")
                    .HasComment("设备状态");

                entity.Property(e => e.Latitude)
                    .HasColumnName("latitude")
                    .HasComment("纬度");

                entity.Property(e => e.LatitudeBd)
                    .HasColumnName("latitudeBD")
                    .HasComment("纬度-百度");

                entity.Property(e => e.Longitude)
                    .HasColumnName("longitude")
                    .HasComment("经度");

                entity.Property(e => e.LongitudeBd)
                    .HasColumnName("longitudeBD")
                    .HasComment("经度-百度");

                entity.Property(e => e.Ownership)
                    .HasColumnName("ownership")
                    .HasColumnType("varchar(50)")
                    .HasComment("物业所有权")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.SetupTime)
                    .HasColumnName("setup_time")
                    .HasColumnType("datetime")
                    .HasComment("安装完成时间");

                entity.Property(e => e.SiteName)
                    .IsRequired()
                    .HasColumnName("site_name")
                    .HasColumnType("varchar(100)")
                    .HasComment("站点名称")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.SiteNational)
                    .HasColumnName("site_national")
                    .HasColumnType("varchar(50)")
                    .HasComment("国控站点")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.SiteType)
                    .IsRequired()
                    .HasColumnName("site_type")
                    .HasColumnType("varchar(20)")
                    .HasComment("站点类型")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.StreetName)
                    .IsRequired()
                    .HasColumnName("street_name")
                    .HasColumnType("varchar(20)")
                    .HasComment("镇街名称")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");
            });

            modelBuilder.Entity<MicroStationTaskOrder>(entity =>
            {
                entity.HasKey(e => e.MicroStationTaskOrderOid)
                    .HasName("PRIMARY");

                entity.ToTable("microStationTask_Order");

                entity.HasIndex(e => e.MicroStationTaskOrderOid)
                    .HasName("microStationTask_OrderIndex")
                    .IsUnique();

                entity.Property(e => e.MicroStationTaskOrderOid)
                    .HasColumnName("microStationTask_OrderOID")
                    .HasColumnType("varchar(36)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskCommunity)
                    .HasColumnName("task_community")
                    .HasColumnType("varchar(50)")
                    .HasComment("任务社区")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskContent)
                    .HasColumnName("task_content")
                    .HasColumnType("varchar(300)")
                    .HasComment("任务内容")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskId)
                    .HasColumnName("task_id")
                    .HasColumnType("varchar(50)")
                    .HasComment("任务标识")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskMark)
                    .HasColumnName("task_mark")
                    .HasColumnType("varchar(100)")
                    .HasComment("任务备注")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskSiteId)
                    .HasColumnName("task_site_id")
                    .HasColumnType("int(11)")
                    .HasComment("任务微站编号");

                entity.Property(e => e.TaskSiteName)
                    .HasColumnName("task_site_name")
                    .HasColumnType("varchar(100)")
                    .HasComment("任务微站名称")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskStatus)
                    .HasColumnName("task_status")
                    .HasColumnType("varchar(20)")
                    .HasComment("任务状态")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskStreet)
                    .HasColumnName("task_street")
                    .HasColumnType("varchar(20)")
                    .HasComment("任务镇街")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskTimeEnd)
                    .HasColumnName("task_time_end")
                    .HasColumnType("datetime")
                    .HasComment("任务完成时间");

                entity.Property(e => e.TaskTimeStart)
                    .HasColumnName("task_time_start")
                    .HasColumnType("datetime")
                    .HasComment("任务开始时间");

                entity.Property(e => e.TaskTitle)
                    .HasColumnName("task_title")
                    .HasColumnType("varchar(50)")
                    .HasComment("任务标题")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskType)
                    .HasColumnName("task_type")
                    .HasColumnType("varchar(30)")
                    .HasComment("任务类型")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Tasker)
                    .HasColumnName("tasker")
                    .HasColumnType("varchar(30)")
                    .HasComment("任务人")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");
            });

            modelBuilder.Entity<TaskFeedback>(entity =>
            {
                entity.HasKey(e => e.TaskFeedbackOid)
                    .HasName("PRIMARY");

                entity.ToTable("Task_Feedback");

                entity.HasIndex(e => e.TaskFeedbackOid)
                    .HasName("Task_FeedbackIndex")
                    .IsUnique();

                entity.Property(e => e.TaskFeedbackOid)
                    .HasColumnName("Task_FeedbackOID")
                    .HasColumnType("varchar(36)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Isitnecessarytopunish)
                    .HasColumnType("bit(1)")
                    .HasComment("是否需要处罚");

                entity.Property(e => e.Isitnecessarytorectify)
                    .HasColumnType("bit(1)")
                    .HasComment("是否需要整改");

                entity.Property(e => e.Islawenforcementnecessary)
                    .HasColumnType("bit(1)")
                    .HasComment("是否需要执法");

                entity.Property(e => e.Picturenames)
                    .HasColumnType("varchar(200)")
                    .HasComment("反馈图片名称")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Supervision)
                    .HasColumnType("varchar(200)")
                    .HasComment("督查情况")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskfeedbackperson)
                    .HasColumnType("varchar(20)")
                    .HasComment("任务反馈人")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskfeedbackpersonphone)
                    .HasColumnType("varchar(11)")
                    .HasComment("任务反馈人联系电话")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskfeedbacktime)
                    .HasColumnType("datetime")
                    .HasComment("任务反馈时间");

                entity.Property(e => e.Taskfeedbacktimes)
                    .HasColumnType("int(11)")
                    .HasComment("任务反馈次数");

                entity.Property(e => e.Taskid)
                    .HasColumnType("varchar(36)")
                    .HasComment("任务标识")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskordeid)
                    .HasColumnType("varchar(36)")
                    .HasComment("任务工单ID")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");
            });

            modelBuilder.Entity<TaskOrder>(entity =>
            {
                entity.HasKey(e => e.TaskOrderOid)
                    .HasName("PRIMARY");

                entity.ToTable("Task_Order");

                entity.HasIndex(e => e.TaskOrderOid)
                    .HasName("Task_OrderIndex")
                    .IsUnique();

                entity.Property(e => e.TaskOrderOid)
                    .HasColumnName("Task_OrderOID")
                    .HasColumnType("varchar(36)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.AlarmStationname)
                    .HasColumnType("varchar(100)")
                    .HasComment("告警微站名称")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.AlarmStationnumber)
                    .HasColumnType("int(11)")
                    .HasComment("告警微站编号");

                entity.Property(e => e.Alarmcontent)
                    .HasColumnType("varchar(200)")
                    .HasComment("告警内容")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Alarmfactor)
                    .HasColumnType("varchar(30)")
                    .HasComment("告警关联因子")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Alarmtime)
                    .HasColumnType("datetime")
                    .HasComment("告警时间");

                entity.Property(e => e.Checktime)
                    .HasColumnType("datetime")
                    .HasComment("查收时间");

                entity.Property(e => e.Collector)
                    .HasColumnType("varchar(30)")
                    .HasComment("查收人")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Collectorphone)
                    .HasColumnType("varchar(11)")
                    .HasComment("查收人联系电话")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Contributionrate).HasComment("贡献率");

                entity.Property(e => e.Contributionrateranking)
                    .HasColumnType("int(11)")
                    .HasComment("贡献率排名");

                entity.Property(e => e.TaskCommunity)
                    .HasColumnType("varchar(50)")
                    .HasComment("任务社区")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.TaskTownStreet)
                    .HasColumnType("varchar(20)")
                    .HasComment("任务镇街")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskcompletetime)
                    .HasColumnType("datetime")
                    .HasComment("任务完成时间");

                entity.Property(e => e.Taskcontent)
                    .HasColumnType("varchar(200)")
                    .HasComment("任务内容")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskdeadline)
                    .HasColumnType("datetime")
                    .HasComment("任务截至时间");

                entity.Property(e => e.Taskfallback)
                    .HasColumnType("bit(1)")
                    .HasComment("任务回退");

                entity.Property(e => e.Taskfallbackreason)
                    .HasColumnType("varchar(100)")
                    .HasComment("任务回退理由")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskfallbacktime)
                    .HasColumnType("datetime")
                    .HasComment("任务回退时间");

                entity.Property(e => e.Taskfeedbacktime)
                    .HasColumnType("datetime")
                    .HasComment("任务反馈时间");

                entity.Property(e => e.Taskfeedbacktimes)
                    .HasColumnType("int(11)")
                    .HasComment("任务反馈次数");

                entity.Property(e => e.Taskid)
                    .HasColumnType("varchar(36)")
                    .HasComment("任务标识")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Tasknotes)
                    .HasColumnType("varchar(100)")
                    .HasComment("任务备注")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskobjectaddress)
                    .HasColumnType("varchar(100)")
                    .HasComment("任务对象地址")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskobjectname)
                    .HasColumnType("varchar(50)")
                    .HasComment("任务对象名称")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskreceivingtime)
                    .HasColumnType("datetime")
                    .HasComment("任务接收时间");

                entity.Property(e => e.Taskstatus)
                    .HasColumnType("varchar(20)")
                    .HasComment("任务状态")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Taskstatusupdatetime)
                    .HasColumnType("datetime")
                    .HasComment("任务状态更新时间");

                entity.Property(e => e.Tasktitle)
                    .HasColumnType("varchar(50)")
                    .HasComment("任务标题")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.Tasktype)
                    .HasColumnType("varchar(20)")
                    .HasComment("任务类型")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}

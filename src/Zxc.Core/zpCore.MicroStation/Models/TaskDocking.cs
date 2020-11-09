using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class TaskDocking
    {
        public string TaskDockingOid { get; set; }
        public string Filename { get; set; }
        public string Filepath { get; set; }
        public string Dockingtype { get; set; }
        public string AssociationId { get; set; }
        public string Dockingmode { get; set; }
        public string Dockingresults { get; set; }
        public DateTime? Dockingtime { get; set; }
        public int Dockingtimes { get; set; }
        public string Dockmark { get; set; }
        public DateTime? Createtime { get; set; }
    }
}

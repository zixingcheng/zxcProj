using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class Organization
    {
        public string OrganizationOid { get; set; }
        public int Organizationcategory { get; set; }
        public int Departmenttype { get; set; }
        public string Groupname { get; set; }
        public int GroupType { get; set; }
        public string Organizationcode { get; set; }
        public int Organizationlevel { get; set; }
        public string Parentnodecode { get; set; }
        public string Nodepath { get; set; }
    }
}

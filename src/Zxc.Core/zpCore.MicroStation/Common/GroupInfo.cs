using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace zpCore.MicroStation.Common
{
    public class GroupInfo
    {
        public string groupOID { get; set; }
        public string groupID { get; set; }
        public string groupName { get; set; }
    }
}
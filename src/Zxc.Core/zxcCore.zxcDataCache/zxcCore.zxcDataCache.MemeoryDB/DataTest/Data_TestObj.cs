using System;
using System.Collections.Generic;
using System.Text;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcDataCache.MemoryDB.Test
{
    public partial class Data_TestObj : Data_Models
    {
        public int Id { get; set; }
        public string Id_str { get; set; }
    }
    public partial class TestObj2
    {
        public int Id { get; set; }
        public string Id_str { get; set; }
    }
}
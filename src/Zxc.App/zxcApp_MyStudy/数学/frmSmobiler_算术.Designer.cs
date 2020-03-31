using System;
using Smobiler.Core;
namespace zxcApp.MyStudy
{
    partial class frmSmobiler_算术 : Smobiler.Core.Controls.MobileForm
    {
        #region "SmobilerForm generated code "

        //SmobilerForm overrides dispose to clean up the component list.
        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);
        }


        //NOTE: The following procedure is required by the SmobilerForm
        //It can be modified using the SmobilerForm.  
        //Do not modify it using the code editor.
        [System.Diagnostics.DebuggerStepThrough()]
        private void InitializeComponent()
        {
            this.panel1 = new Smobiler.Core.Controls.Panel();
            this.img_Symbol = new Smobiler.Core.Controls.Image();
            this.img_1 = new Smobiler.Core.Controls.Image();
            this.img_2 = new Smobiler.Core.Controls.Image();
            this.img_3 = new Smobiler.Core.Controls.Image();
            this.img_Result = new Smobiler.Core.Controls.Image();
            this.imgBtn_Help = new Smobiler.Core.Controls.ImageButton();
            this.imgR_0 = new Smobiler.Core.Controls.ImageButton();
            this.imgR_1 = new Smobiler.Core.Controls.ImageButton();
            this.imgR_2 = new Smobiler.Core.Controls.ImageButton();
            this.img_Right = new Smobiler.Core.Controls.Image();
            this.img_Wrong = new Smobiler.Core.Controls.Image();
            this.btn_控制 = new Smobiler.Core.Controls.Button();
            this.timer1 = new Smobiler.Core.Controls.Timer();
            this.img_遮挡 = new Smobiler.Core.Controls.Image();
            this.img_Wrong2 = new Smobiler.Core.Controls.Image();
            this.lab_Countdown = new Smobiler.Plugins.HighLightLabel();
            this.timer2 = new Smobiler.Core.Controls.Timer();
            // 
            // panel1
            // 
            this.panel1.Location = new System.Drawing.Point(0, 170);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(306, 90);
            // 
            // img_Symbol
            // 
            this.img_Symbol.Location = new System.Drawing.Point(110, 73);
            this.img_Symbol.Name = "img_Symbol";
            this.img_Symbol.ResourceID = "+.png";
            this.img_Symbol.ResourcePath = "resNumber";
            this.img_Symbol.Size = new System.Drawing.Size(58, 59);
            // 
            // img_1
            // 
            this.img_1.Location = new System.Drawing.Point(11, 57);
            this.img_1.Name = "img_1";
            this.img_1.ResourceID = "1.png";
            this.img_1.ResourcePath = "resNumber";
            this.img_1.Size = new System.Drawing.Size(92, 87);
            // 
            // img_2
            // 
            this.img_2.Location = new System.Drawing.Point(175, 57);
            this.img_2.Name = "img_2";
            this.img_2.ResourceID = "1.png";
            this.img_2.ResourcePath = "resNumber";
            this.img_2.Size = new System.Drawing.Size(92, 87);
            // 
            // img_3
            // 
            this.img_3.Location = new System.Drawing.Point(272, 78);
            this.img_3.Name = "img_3";
            this.img_3.ResourceID = "=.png";
            this.img_3.ResourcePath = "resNumber";
            this.img_3.Size = new System.Drawing.Size(59, 59);
            // 
            // img_Result
            // 
            this.img_Result.Location = new System.Drawing.Point(337, 78);
            this.img_Result.Name = "img_Result";
            this.img_Result.ResourceID = "2.png";
            this.img_Result.ResourcePath = "resNumber";
            this.img_Result.Size = new System.Drawing.Size(61, 59);
            // 
            // imgBtn_Help
            // 
            this.imgBtn_Help.Location = new System.Drawing.Point(279, 48);
            this.imgBtn_Help.Name = "imgBtn_Help";
            this.imgBtn_Help.ResourceID = "help.jpg";
            this.imgBtn_Help.ResourcePath = "resNumber";
            this.imgBtn_Help.Size = new System.Drawing.Size(43, 44);
            this.imgBtn_Help.Press += new System.EventHandler(this.imgBtn_Help_Press);
            // 
            // imgR_0
            // 
            this.imgR_0.Location = new System.Drawing.Point(404, 8);
            this.imgR_0.Name = "imgR_0";
            this.imgR_0.ResourceID = "1.png";
            this.imgR_0.ResourcePath = "resNumber";
            this.imgR_0.Size = new System.Drawing.Size(85, 80);
            this.imgR_0.Press += new System.EventHandler(this.imgR_Press);
            // 
            // imgR_1
            // 
            this.imgR_1.Location = new System.Drawing.Point(404, 89);
            this.imgR_1.Name = "imgR_1";
            this.imgR_1.ResourceID = "2.png";
            this.imgR_1.ResourcePath = "resNumber";
            this.imgR_1.Size = new System.Drawing.Size(85, 81);
            this.imgR_1.Press += new System.EventHandler(this.imgR_Press);
            // 
            // imgR_2
            // 
            this.imgR_2.Location = new System.Drawing.Point(404, 170);
            this.imgR_2.Name = "imgR_2";
            this.imgR_2.ResourceID = "3.png";
            this.imgR_2.ResourcePath = "resNumber";
            this.imgR_2.Size = new System.Drawing.Size(85, 80);
            this.imgR_2.Press += new System.EventHandler(this.imgR_Press);
            // 
            // img_Right
            // 
            this.img_Right.Location = new System.Drawing.Point(308, 170);
            this.img_Right.Name = "img_Right";
            this.img_Right.ResourceID = "right.png";
            this.img_Right.ResourcePath = "resNumber";
            this.img_Right.Size = new System.Drawing.Size(85, 80);
            this.img_Right.Visible = false;
            // 
            // img_Wrong
            // 
            this.img_Wrong.Location = new System.Drawing.Point(246, 170);
            this.img_Wrong.Name = "img_Wrong";
            this.img_Wrong.ResourceID = "wrong.png";
            this.img_Wrong.ResourcePath = "resNumber";
            this.img_Wrong.Size = new System.Drawing.Size(85, 80);
            this.img_Wrong.Visible = false;
            // 
            // btn_控制
            // 
            this.btn_控制.Location = new System.Drawing.Point(2, 3);
            this.btn_控制.Name = "btn_控制";
            this.btn_控制.Size = new System.Drawing.Size(98, 34);
            this.btn_控制.Text = "开始";
            this.btn_控制.Press += new System.EventHandler(this.btn_控制_Press);
            // 
            // timer1
            // 
            this.timer1.Name = "timer1";
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // img_遮挡
            // 
            this.img_遮挡.Location = new System.Drawing.Point(404, 8);
            this.img_遮挡.Name = "img_遮挡";
            this.img_遮挡.ResourcePath = "resNumber";
            this.img_遮挡.Size = new System.Drawing.Size(85, 242);
            this.img_遮挡.Visible = false;
            // 
            // img_Wrong2
            // 
            this.img_Wrong2.Location = new System.Drawing.Point(246, 170);
            this.img_Wrong2.Name = "img_Wrong2";
            this.img_Wrong2.ResourceID = "wrong.png";
            this.img_Wrong2.ResourcePath = "resNumber";
            this.img_Wrong2.Size = new System.Drawing.Size(85, 80);
            this.img_Wrong2.Visible = false;
            // 
            // lab_Countdown
            // 
            this.lab_Countdown.HighlightBackColor = System.Drawing.Color.OrangeRed;
            this.lab_Countdown.Location = new System.Drawing.Point(110, 7);
            this.lab_Countdown.Name = "lab_Countdown";
            this.lab_Countdown.Size = new System.Drawing.Size(136, 30);
            // 
            // timer2
            // 
            this.timer2.Name = "timer2";
            this.timer2.Tick += new System.EventHandler(this.timer2_Tick);
            // 
            // frmSmobiler_算术
            // 
            this.Components.AddRange(new Smobiler.Core.Controls.MobileComponent[] {
            this.timer1,
            this.timer2});
            this.Controls.AddRange(new Smobiler.Core.Controls.MobileControl[] {
            this.panel1,
            this.img_Symbol,
            this.img_1,
            this.img_2,
            this.img_3,
            this.img_Result,
            this.imgBtn_Help,
            this.imgR_0,
            this.imgR_1,
            this.imgR_2,
            this.img_Right,
            this.img_Wrong,
            this.btn_控制,
            this.img_遮挡,
            this.img_Wrong2,
            this.lab_Countdown});
            this.Direction = Smobiler.Core.Controls.LayoutDirection.Row;
            this.Orientation = Smobiler.Core.Controls.FormOrientation.Landscape;
            this.Size = new System.Drawing.Size(500, 300);
            this.Load += new System.EventHandler(this.FrmSmobiler_算术_Load);
            this.Name = "frmSmobiler_算术";

        }
        #endregion
        private Smobiler.Core.Controls.Panel panel1;
        private Smobiler.Core.Controls.Image img_Symbol;
        private Smobiler.Core.Controls.Image img_1;
        private Smobiler.Core.Controls.Image img_2;
        private Smobiler.Core.Controls.Image img_3;
        private Smobiler.Core.Controls.Image img_Result;
        private Smobiler.Core.Controls.ImageButton imgBtn_Help;
        private Smobiler.Core.Controls.ImageButton imgR_0;
        private Smobiler.Core.Controls.ImageButton imgR_1;
        private Smobiler.Core.Controls.ImageButton imgR_2;
        private Smobiler.Core.Controls.Image img_Right;
        private Smobiler.Core.Controls.Image img_Wrong;
        private Smobiler.Core.Controls.Button btn_控制;
        private Smobiler.Core.Controls.Timer timer1;
        private Smobiler.Core.Controls.Image img_遮挡;
        private Smobiler.Core.Controls.Image img_Wrong2;
        private Smobiler.Plugins.HighLightLabel lab_Countdown;
        private Smobiler.Core.Controls.Timer timer2;
    }
}
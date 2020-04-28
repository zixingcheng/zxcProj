using System;
using Smobiler.Core;
namespace zxcApp.MyStudy
{
    partial class frmSmobiler_成绩 : Smobiler.Core.Controls.MobileForm
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
            this.img_1 = new Smobiler.Core.Controls.Image();
            this.img_2 = new Smobiler.Core.Controls.Image();
            this.lab_R0 = new Smobiler.Plugins.HighLightLabel();
            this.lab_R2 = new Smobiler.Plugins.HighLightLabel();
            this.btn_控制 = new Smobiler.Core.Controls.Button();
            this.lab_Static = new Smobiler.Core.Controls.Label();
            this.img_3 = new Smobiler.Core.Controls.Image();
            // 
            // img_1
            // 
            this.img_1.Location = new System.Drawing.Point(165, 50);
            this.img_1.Name = "img_1";
            this.img_1.ResourceID = "8.png";
            this.img_1.ResourcePath = "resNumber";
            this.img_1.Size = new System.Drawing.Size(92, 87);
            // 
            // img_2
            // 
            this.img_2.Location = new System.Drawing.Point(231, 50);
            this.img_2.Name = "img_2";
            this.img_2.ResourceID = "2.png";
            this.img_2.ResourcePath = "resNumber";
            this.img_2.Size = new System.Drawing.Size(92, 87);
            // 
            // lab_R0
            // 
            this.lab_R0.FontSize = 24F;
            this.lab_R0.HighlightBackColor = System.Drawing.Color.OrangeRed;
            this.lab_R0.HighlightFontSize = 24;
            this.lab_R0.Location = new System.Drawing.Point(53, 76);
            this.lab_R0.Name = "lab_R0";
            this.lab_R0.Size = new System.Drawing.Size(156, 59);
            this.lab_R0.Text = "你的成绩是：";
            // 
            // lab_R2
            // 
            this.lab_R2.FontSize = 24F;
            this.lab_R2.HighlightBackColor = System.Drawing.Color.OrangeRed;
            this.lab_R2.HighlightFontSize = 24;
            this.lab_R2.Location = new System.Drawing.Point(389, 76);
            this.lab_R2.Name = "lab_R2";
            this.lab_R2.Size = new System.Drawing.Size(123, 59);
            this.lab_R2.Text = "分！";
            // 
            // btn_控制
            // 
            this.btn_控制.Location = new System.Drawing.Point(329, 176);
            this.btn_控制.Name = "btn_控制";
            this.btn_控制.Size = new System.Drawing.Size(98, 34);
            this.btn_控制.Text = "确定";
            this.btn_控制.Press += new System.EventHandler(this.btn_控制_Press);
            // 
            // lab_Static
            // 
            this.lab_Static.Location = new System.Drawing.Point(55, 176);
            this.lab_Static.Name = "lab_Static";
            this.lab_Static.Size = new System.Drawing.Size(202, 35);
            this.lab_Static.Text = "总计：答错0题，答对3题。";
            this.lab_Static.Underline = true;
            // 
            // img_3
            // 
            this.img_3.Location = new System.Drawing.Point(297, 50);
            this.img_3.Name = "img_3";
            this.img_3.ResourceID = "0.png";
            this.img_3.ResourcePath = "resNumber";
            this.img_3.Size = new System.Drawing.Size(92, 87);
            // 
            // frmSmobiler_成绩
            // 
            this.Controls.AddRange(new Smobiler.Core.Controls.MobileControl[] {
            this.img_1,
            this.img_2,
            this.lab_R0,
            this.lab_R2,
            this.btn_控制,
            this.lab_Static,
            this.img_3});
            this.Direction = Smobiler.Core.Controls.LayoutDirection.Row;
            this.JustifyAlign = Smobiler.Core.Controls.LayoutJustifyAlign.Center;
            this.Orientation = Smobiler.Core.Controls.FormOrientation.Landscape;
            this.Size = new System.Drawing.Size(500, 250);
            this.Load += new System.EventHandler(this.frmSmobiler_成绩_Load);
            this.Name = "frmSmobiler_成绩";

        }
        #endregion
        private Smobiler.Core.Controls.Image img_1;
        private Smobiler.Core.Controls.Image img_2;
        private Smobiler.Plugins.HighLightLabel lab_R0;
        private Smobiler.Plugins.HighLightLabel lab_R2;
        private Smobiler.Core.Controls.Button btn_控制;
        private Smobiler.Core.Controls.Label lab_Static;
        private Smobiler.Core.Controls.Image img_3;
    }
}
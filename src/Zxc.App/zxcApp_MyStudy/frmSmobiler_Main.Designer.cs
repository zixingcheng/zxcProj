using System;
using Smobiler.Core;
namespace zxcApp.MyStudy
{
    partial class frmSmobiler_Main : Smobiler.Core.Controls.MobileForm
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
            Smobiler.Core.Controls.VoiceRecorder voiceRecorder2;
            this.iconMenuView1 = new Smobiler.Core.Controls.IconMenuView();
            this.button1 = new Smobiler.Core.Controls.Button();
            this.voiceRecorder1 = new Smobiler.Core.Controls.VoiceRecorder();
            this.button2 = new Smobiler.Core.Controls.Button();
            voiceRecorder2 = new Smobiler.Core.Controls.VoiceRecorder();
            // 
            // voiceRecorder2
            // 
            voiceRecorder2.Name = "voiceRecorder2";
            voiceRecorder2.TimeOut = 0;
            // 
            // iconMenuView1
            // 
            this.iconMenuView1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.iconMenuView1.GroupFontSize = 18F;
            this.iconMenuView1.ItemWidth = 80;
            this.iconMenuView1.MenuItemHeight = 100;
            this.iconMenuView1.Name = "iconMenuView1";
            this.iconMenuView1.ShowGroupTitle = true;
            this.iconMenuView1.Size = new System.Drawing.Size(300, 500);
            this.iconMenuView1.ItemPress += new Smobiler.Core.Controls.IconMenuViewItemPressClickHandler(this.iconMenuView1_ItemPress);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(112, 241);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(100, 30);
            this.button1.Text = "button1";
            this.button1.Press += new System.EventHandler(this.button1_Press);
            // 
            // voiceRecorder1
            // 
            this.voiceRecorder1.Name = "voiceRecorder1";
            this.voiceRecorder1.TimeOut = 0;
            this.voiceRecorder1.RecordedAudio += new Smobiler.Core.Controls.AudioRecorderOnlineCallBackHandler(this.voiceRecorder1_RecordedAudio);
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(131, 300);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(100, 30);
            this.button2.Text = "button2";
            this.button2.Press += new System.EventHandler(this.button2_Press);
            // 
            // frmSmobiler_Main
            // 
            this.Components.AddRange(new Smobiler.Core.Controls.MobileComponent[] {
            this.voiceRecorder1,
            voiceRecorder2});
            this.Controls.AddRange(new Smobiler.Core.Controls.MobileControl[] {
            this.iconMenuView1,
            this.button1,
            this.button2});
            this.Load += new System.EventHandler(this.frmSmobiler_Main_Load);
            this.Name = "frmSmobiler_Main";

        }
        #endregion
        private Smobiler.Core.Controls.IconMenuView iconMenuView1;
        private Smobiler.Core.Controls.Button button1;
        private Smobiler.Core.Controls.VoiceRecorder voiceRecorder1;
        private Smobiler.Core.Controls.Button button2;
    }
}
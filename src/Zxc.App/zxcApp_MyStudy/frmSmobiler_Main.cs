using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Smobiler.Core;
using Smobiler.Core.Controls;

namespace zxcApp.MyStudy
{
    partial class frmSmobiler_Main : Smobiler.Core.Controls.MobileForm
    {
        public frmSmobiler_Main() : base()
        {
            //This call is required by the SmobilerForm.
            InitializeComponent();
        }

        private void frmSmobiler_Main_Load(object sender, EventArgs e)
        {
            IconMenuViewGroup ig = new IconMenuViewGroup("我的学习");
            ig.Items.Add(new IconMenuViewItem("1", "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1631881666,2509684710&fm=11&gp=0.jpg", "数学"));
            ig.Items.Add(new IconMenuViewItem("2", "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1585032360768&di=19b6aca86d0f9a0ae40430318dc86337&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fq_70%2Cc_zoom%2Cw_640%2Fimages%2F20171204%2F116e28b1678d4d7cb603fb4dbb4df9f8.gif", "算术"));

            //若使用FontIcon需要指明ImageType，默认的ImageType为image， ig.Items.Add(new IconMenuViewItem("5", "cog", "考勤") { ImageType = ImageEx.ImageStyle.FontIcon });
            iconMenuView1.ColumnNum = 4;
            iconMenuView1.ShowGroupTitle = true;
            iconMenuView1.Groups.Add(ig);
        }

        private void iconMenuView1_ItemPress(object sender, IconMenuViewItemPressEventArgs e)
        {
            switch (e.Item.ID)
            {
                case "2":
                    frmSmobiler_算术 frm_算术 = new frmSmobiler_算术();
                    Show(frm_算术); 
                    break;
                default:
                    break;
            }
        }

        private void button1_Press(object sender, EventArgs e)
        {
            this.voiceRecorder1.GetRecorderAudio();  //在线保存 
        }

        private void voiceRecorder1_RecordedAudio(object sender, BinaryResultArgs e)
        {
            try
            {
                this.Client.ShowOfflineResources();     // 显示离线资源页

                if (string.IsNullOrEmpty(e.error))
                {
                    e.SaveFile();
                    //保存到本地运行项目的文件夹中
                }
            }
            catch (Exception ex)
            {
                Toast(ex.Message);
            }
        }

        private void button2_Press(object sender, EventArgs e)
        {
            try
            {
                this.Client.PlayAudio("wrong.aac", "resNumber", ResourceMode.File);
            }
            catch (Exception ex)
            {
                Toast(ex.Message);
            }
        }
    }
}
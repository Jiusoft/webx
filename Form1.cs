using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FAX
{
    public partial class FAX : Form
    {
        public FAX()
        {
            InitializeComponent();
            webBrowser1.Navigate("https://jiusoft.w3spaces.com/faxstart.html");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            webBrowser1.GoBack();
        }
        private void button2_Click(object sender, EventArgs e)
        {
            webBrowser1.GoForward();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            webBrowser1.Refresh();
        }

        private void button5_Click(object sender, EventArgs e)
        {
            webBrowser1.Navigate(textBox1.Text);
        }

        private void textBox1_KeyDown(System.Object sender, System.Windows.Forms.KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
                webBrowser1.Navigate(textBox1.Text);
        }
        private void webBrowser1_Complete(object sender, EventArgs e)
        {
            string url = Convert.ToString(webBrowser1.Url);
            if (url == "https://jiusoft.w3spaces.com/faxstart.html")
            {
                url = "";
            }
            else if (url == "about:homepage")
            {
                webBrowser1.Navigate("https://jiusoft.w3spaces.com/faxstart.html");
                url = "";
            }
            if (url == "https://jiusoft.w3spaces.com/faxerror.html")
            {
                url = "about:error";
            }
            textBox1.Text = url;
        }

        private void button4_Click(object sender, EventArgs e)
        {
            webBrowser1.Navigate("https://html.duckduckgo.com/html/?q=" + textBox2.Text);
        }
        private void textBox2_KeyDown(System.Object sender, System.Windows.Forms.KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
                webBrowser1.Navigate("https://html.duckduckgo.com/html/?q=" + textBox2.Text);
        }

        private void textBox2_Click(object sender, EventArgs e)
        {
            textBox2.Text = "";
        }
        private void textBox1_Click(object sender, EventArgs e)
        {
            textBox1.SelectAll();
        }
        private void webBrowser1_NewWindow(object sender, System.ComponentModel.CancelEventArgs e)
        {
            e.Cancel = true;
            webBrowser1.Navigate("https://jiusoft.w3spaces.com/faxerror.html");
        }
    }
}

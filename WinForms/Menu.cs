/*
 The MIT License
 
 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in the
 Software without restriction, including without limitation the rights to use, copy,
 modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
 and to permit persons to whom the Software is furnished to do so, subject to the
 following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 
 BillReminder - Copyright (c) 2006 Og Maciel

*/

using System;
using System.Drawing;
using System.Collections;
using System.ComponentModel;
using System.Windows.Forms;
using System.Data;
using System.Xml;
using System.Xml.Serialization;
using System.IO;
using System.Text;

namespace BillReminder
{
	/// <summary>
	/// Used for enumerating bills' status.
	/// </summary>
	enum Status 
	{
		OverDue = -1,
		Due = 0,
		Current = 1
	}

	/// <summary>
	/// Summary description for Menu.
	/// </summary>
	public class Menu : System.Windows.Forms.Form
	{
		private Configuration config;

//		private BillCollection unpaidBills, paidBills;
//		private string UNPAIDFILE = Application.StartupPath + "/unpaid.xml";
//		private string PAIDFILE = Application.StartupPath + "/paid.xml";
		private System.Windows.Forms.Button button6;
		private System.Windows.Forms.Button button1;
		private System.Windows.Forms.Button btnClose;
		private System.Windows.Forms.Button btnHelp;
		private System.Windows.Forms.Button btnDisplay;
		private System.Windows.Forms.Button btnSearch;
		private System.Windows.Forms.Timer timer1;
		private System.Windows.Forms.PictureBox pictureBox1;
		private System.ComponentModel.IContainer components;
		
		public Menu()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			//Configuration Singleton class
			this.config = Configuration.Instance();

//			// Initialize bill collections
//			unpaidBills = config.UnpaidBills;
//			paidBills = config.PaidBills;

			this.BillReminderUI();

			this.timer1.Interval = 6000;
			this.timer1.Enabled = true;
		}

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		protected override void Dispose( bool disposing )
		{
			if( disposing )
			{
				if(components != null)
				{
					components.Dispose();
				}
			}
			base.Dispose( disposing );
		}

		#region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
			this.components = new System.ComponentModel.Container();
			//System.Resources.ResourceManager resources = new System.Resources.ResourceManager("icon");
			this.button6 = new System.Windows.Forms.Button();
			this.btnSearch = new System.Windows.Forms.Button();
			this.btnDisplay = new System.Windows.Forms.Button();
			this.button1 = new System.Windows.Forms.Button();
			this.btnClose = new System.Windows.Forms.Button();
			this.btnHelp = new System.Windows.Forms.Button();
			this.timer1 = new System.Windows.Forms.Timer(this.components);
			this.pictureBox1 = new System.Windows.Forms.PictureBox();
			this.SuspendLayout();
			// 
			// button6
			// 
			//this.button6.Image = ((System.Drawing.Image)(resources.GetObject("button6.Image")));
			this.button6.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
			this.button6.Location = new System.Drawing.Point(8, 216);
			this.button6.Name = "button6";
			this.button6.Size = new System.Drawing.Size(192, 24);
			this.button6.TabIndex = 3;
			this.button6.Text = "Preferences";
			// 
			// btnSearch
			// 
			//this.btnSearch.Image = Image.FromFile("stock_search.png");
			this.btnSearch.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
			this.btnSearch.Location = new System.Drawing.Point(8, 168);
			this.btnSearch.Name = "btnSearch";
			this.btnSearch.Size = new System.Drawing.Size(192, 24);
			this.btnSearch.TabIndex = 2;
			this.btnSearch.Text = "&Search for bill";
			this.btnSearch.Click += new System.EventHandler(this.btnSearch_Click);
			// 
			// btnDisplay
			// 
			this.btnDisplay.Location = new System.Drawing.Point(8, 136);
			this.btnDisplay.Name = "btnDisplay";
			this.btnDisplay.Size = new System.Drawing.Size(192, 24);
			this.btnDisplay.TabIndex = 1;
			this.btnDisplay.Text = "Display all bills";
			this.btnDisplay.Click += new System.EventHandler(this.btnDisplay_Click);
			// 
			// button1
			// 
			//this.button1.Image = ((System.Drawing.Image)(resources.GetObject("button1.Image")));
			this.button1.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
			this.button1.Location = new System.Drawing.Point(8, 96);
			this.button1.Name = "button1";
			this.button1.Size = new System.Drawing.Size(192, 24);
			this.button1.TabIndex = 0;
			this.button1.Text = "&Add a new bill";
			this.button1.Click += new System.EventHandler(this.button1_Click);
			// 
			// btnClose
			// 
			//this.btnClose.Image = ((System.Drawing.Image)(resources.GetObject("btnClose.Image")));
			this.btnClose.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
			this.btnClose.Location = new System.Drawing.Point(112, 256);
			this.btnClose.Name = "btnClose";
			this.btnClose.Size = new System.Drawing.Size(88, 32);
			this.btnClose.TabIndex = 5;
			this.btnClose.Text = "&Close";
			this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
			// 
			// btnHelp
			// 
			//this.btnHelp.Image = ((System.Drawing.Image)(resources.GetObject("btnHelp.Image")));
			this.btnHelp.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
			this.btnHelp.Location = new System.Drawing.Point(8, 256);
			this.btnHelp.Name = "btnHelp";
			this.btnHelp.Size = new System.Drawing.Size(88, 32);
			this.btnHelp.TabIndex = 4;
			this.btnHelp.Text = "&Help";
			// 
			// timer1
			// 
			this.timer1.Interval = 1000;
			this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
			// 
			// pictureBox1
			// 
			this.pictureBox1.Image = Image.FromFile("header.jpg");
			//this.pictureBox1.Image = logo;
			this.pictureBox1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.pictureBox1.Location = new System.Drawing.Point(8, 8);
			this.pictureBox1.Name = "pictureBox1";
			this.pictureBox1.Size = new System.Drawing.Size(200, 80);
			this.pictureBox1.TabIndex = 6;
			this.pictureBox1.TabStop = false;
			// 
			// Menu
			// 
			this.AutoScaleBaseSize = new System.Drawing.Size(6, 15);
			this.ClientSize = new System.Drawing.Size(217, 296);
			this.Controls.Add(this.pictureBox1);
			this.Controls.Add(this.button6);
			this.Controls.Add(this.btnSearch);
			this.Controls.Add(this.btnDisplay);
			this.Controls.Add(this.button1);
			this.Controls.Add(this.btnClose);
			this.Controls.Add(this.btnHelp);
			this.MaximizeBox = false;
			this.Name = "Menu";
			this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
			this.Text = "BillReminder";
                        //this.Icon = ((System.Drawing.Icon)(resources.GetObject("icon.ico")));
			//this.Icon = ((System.Drawing.Icon)(Image.FromFile("icon.ico")));
			this.ResumeLayout(false);

		}
		#endregion

		[STAThread]
		static void Main() 
		{
			Application.Run(new Menu());
		}

		private void BillReminderUI() 
		{
			System.Reflection.AssemblyName asm = 
				System.Reflection.Assembly.GetEntryAssembly().GetName();		
			string appname = asm.Name;
			string version = String.Format("{0}.{1}.{2}", asm.Version.Major, 
				asm.Version.Minor, asm.Version.Build);

			this.Text = appname + " - " + version;
			
//			this.DisplayIntro(this.rtbDisplay);
		}

		private void DisplayBills(BillCollection bc) 
		{
			// New instance of Display.cs
			Display w = new Display(bc);

			// Hides current Menu.cs
			this.Hide();
			// and shows (modal) Display.cs
			w.ShowDialog();

			// Clean up
			w = null;

			// Back to Menu.cs
			this.Show();
		}

		private void AddBill() 
		{
			// Instantiate NewBill form
			NewBill w = new NewBill();

			// Hides Menu.cs
			this.Hide();

			// Shows NewBill.cs 
			w.ShowDialog(this);

			// Extract new Bill object
			Bill newBill = w.GetBill;

			// Properly disposes of form
			w.Dispose();

			// Back to Menu.cs
			this.Show();

			// First check if new bill was returned
			if (newBill != null)
				try 
				{
					this.config.UnpaidBills.Add(newBill);
					//Automatically saves collection
					Configuration.Write(Configuration.BillType.Unpaid);
				}
				catch (ArgumentException ae) 
				{
					MessageBox.Show(ae.Message);
				}

		}

		private void SearchBills() 
		{
			// Instantiate NewBill form
			Search w = new Search();

			// Shows Search.cs 
			w.ShowDialog(this);

			// Properly disposes of form
			w.Dispose();			
			
			// Any result returned?
			if (this.config.SearchedBills != null)
				// Display them
				this.DisplayBills(this.config.SearchedBills);
			else
				// Display all (default)
				this.DisplayBills(null);
		}
		
		private void DisplayLateBills() 
		{
			// Calculate offset to midnight
			this.timer1.Interval = this.MillisecondsToMidnight();

			//Used to hold list of (over)due bills
			StringBuilder msg = new StringBuilder();

			msg.Append("The following bills are due:\n\n");

			foreach (Bill b in this.config.UnpaidBills)
				if (b.Status != (int)Status.Current)
					msg.Append(String.Format("{0}  -  {1}\n", b.Payee, b.AmountDue.ToString("c")));
					

			/// TODO:
			/// Check if previous instance of AlertWindow already exists
			/// in which case we want to re-use it.
			
			// Displays list of late/due bills in a window
			AlertWindow aw = new AlertWindow(msg.ToString(),"Overdue");
			aw.ShowDialog(this);
			aw = null;

			//MessageBox.Show(msg.ToString(),"Overdue");
		}

		private int MillisecondsToMidnight() 
		{
			// Time now
			DateTime now = System.DateTime.Now;
			
			// Time tomorrow at midnight
			DateTime tomorrow = new DateTime(now.Year,now.Month,now.Day + 1,0,0,0);
			
			// Milliseconds remaining untill tomorrow
			TimeSpan diff = tomorrow.Subtract(now);

			return Convert.ToInt32(diff.TotalMilliseconds);

		}

		private void btnDisplay_Click(object sender, System.EventArgs e)
		{
			this.DisplayBills(null);
		}

		private void button1_Click(object sender, System.EventArgs e)
		{
			this.AddBill();
		}

		private void btnClose_Click(object sender, System.EventArgs e)
		{
			this.Close();
		}

		private void btnSearch_Click(object sender, System.EventArgs e)
		{
			this.SearchBills();
		}

		private void timer1_Tick(object sender, System.EventArgs e)
		{
//			this.timer1.Interval = this.MillisecondsToMidnight();

			this.DisplayLateBills();

		}

                protected override void OnPaint(PaintEventArgs e)
                {
                        base.OnPaint(e);
                }

	
	}
}

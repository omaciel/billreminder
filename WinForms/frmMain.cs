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
	/// Summary description for frmMain.
	/// </summary>
	public class frmMain : System.Windows.Forms.Form
	{

		// Singleton
		private Configuration config;
		// Temporary container
		private BillCollection billsToDisplay;
		
		private System.Windows.Forms.Panel pnTop;
		private System.Windows.Forms.Panel pnBottom;
		private System.Windows.Forms.ListView lvBills;
		private System.Windows.Forms.Button btnAdd;
		private System.Windows.Forms.Button btnRemove;
		private System.Windows.Forms.Button btnEdit;
		private System.Windows.Forms.StatusBar sbStatus;
		private System.Windows.Forms.Button btnPaid;
		private System.Windows.Forms.Button btnExit;
		private System.Windows.Forms.StatusBarPanel sbPanel1;
		private System.Windows.Forms.StatusBarPanel sbPanel2;
		private System.Windows.Forms.MainMenu mainMenu1;
		private System.Windows.Forms.MenuItem menuItem1;
		private System.Windows.Forms.MenuItem menuItem2;
		private System.Windows.Forms.MenuItem menuItem3;
		private System.Windows.Forms.MenuItem menuItem4;
		private System.Windows.Forms.MenuItem menuItem5;
		private System.Windows.Forms.MenuItem menuItem6;
		private System.Windows.Forms.MenuItem menuItem7;
		private System.Windows.Forms.Timer timer1;
		private System.ComponentModel.IContainer components;
		/// <summary>
		/// Required designer variable.
		/// </summary>
		//private System.ComponentModel.Container components = null;

		public frmMain()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();
			
			//Configuration Singleton class
			this.config = Configuration.Instance();
			
			// Initializes the timer
			this.timer1.Interval = 6000;
			this.timer1.Enabled = true;
			
			// Form initialization and record population
			this.FormatListView();
			this.PopulateListView();
		}

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		protected override void Dispose( bool disposing )
		{
			if( disposing )
			{
				if (components != null) 
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
			this.pnTop = new System.Windows.Forms.Panel();
			this.lvBills = new System.Windows.Forms.ListView();
			this.pnBottom = new System.Windows.Forms.Panel();
			this.btnExit = new System.Windows.Forms.Button();
			this.btnPaid = new System.Windows.Forms.Button();
			this.btnEdit = new System.Windows.Forms.Button();
			this.btnRemove = new System.Windows.Forms.Button();
			this.btnAdd = new System.Windows.Forms.Button();
			this.sbStatus = new System.Windows.Forms.StatusBar();
			this.sbPanel1 = new System.Windows.Forms.StatusBarPanel();
			this.sbPanel2 = new System.Windows.Forms.StatusBarPanel();
			this.mainMenu1 = new System.Windows.Forms.MainMenu();
			this.menuItem1 = new System.Windows.Forms.MenuItem();
			this.menuItem2 = new System.Windows.Forms.MenuItem();
			this.menuItem3 = new System.Windows.Forms.MenuItem();
			this.menuItem4 = new System.Windows.Forms.MenuItem();
			this.menuItem5 = new System.Windows.Forms.MenuItem();
			this.menuItem6 = new System.Windows.Forms.MenuItem();
			this.menuItem7 = new System.Windows.Forms.MenuItem();
			this.timer1 = new System.Windows.Forms.Timer(this.components);
			this.pnTop.SuspendLayout();
			this.pnBottom.SuspendLayout();
			((System.ComponentModel.ISupportInitialize)(this.sbPanel1)).BeginInit();
			this.SuspendLayout();
			// 
			// pnTop
			// 
			this.pnTop.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.pnTop.Controls.Add(this.lvBills);
			this.pnTop.DockPadding.All = 5;
			this.pnTop.Location = new System.Drawing.Point(8, 8);
			this.pnTop.Name = "pnTop";
			this.pnTop.Size = new System.Drawing.Size(384, 312);
			this.pnTop.TabIndex = 0;
			// 
			// lvBills
			// 
			this.lvBills.Dock = System.Windows.Forms.DockStyle.Fill;
			this.lvBills.Location = new System.Drawing.Point(5, 5);
			this.lvBills.Name = "lvBills";
			this.lvBills.Size = new System.Drawing.Size(372, 300);
			this.lvBills.TabIndex = 0;
			// 
			// pnBottom
			// 
			this.pnBottom.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.pnBottom.Controls.Add(this.btnExit);
			this.pnBottom.Controls.Add(this.btnPaid);
			this.pnBottom.Controls.Add(this.btnEdit);
			this.pnBottom.Controls.Add(this.btnRemove);
			this.pnBottom.Controls.Add(this.btnAdd);
			this.pnBottom.Location = new System.Drawing.Point(400, 8);
			this.pnBottom.Name = "pnBottom";
			this.pnBottom.Size = new System.Drawing.Size(104, 312);
			this.pnBottom.TabIndex = 1;
			// 
			// btnExit
			// 
			this.btnExit.Location = new System.Drawing.Point(8, 272);
			this.btnExit.Name = "btnExit";
			this.btnExit.Size = new System.Drawing.Size(80, 24);
			this.btnExit.TabIndex = 4;
			this.btnExit.Text = "E&xit";
			this.btnExit.Click += new System.EventHandler(this.btnExit_Click);
			// 
			// btnPaid
			// 
			this.btnPaid.Location = new System.Drawing.Point(8, 136);
			this.btnPaid.Name = "btnPaid";
			this.btnPaid.Size = new System.Drawing.Size(80, 24);
			this.btnPaid.TabIndex = 3;
			this.btnPaid.Text = "Paid";
			this.btnPaid.Click += new System.EventHandler(this.btnPaid_Click);
			// 
			// btnEdit
			// 
			this.btnEdit.Location = new System.Drawing.Point(8, 96);
			this.btnEdit.Name = "btnEdit";
			this.btnEdit.Size = new System.Drawing.Size(80, 24);
			this.btnEdit.TabIndex = 2;
			this.btnEdit.Text = "Edit";
			this.btnEdit.Click += new System.EventHandler(this.btnEdit_Click);
			// 
			// btnRemove
			// 
			this.btnRemove.Location = new System.Drawing.Point(8, 56);
			this.btnRemove.Name = "btnRemove";
			this.btnRemove.Size = new System.Drawing.Size(80, 24);
			this.btnRemove.TabIndex = 1;
			this.btnRemove.Text = "&Remove";
			this.btnRemove.Click += new System.EventHandler(this.btnRemove_Click);
			// 
			// btnAdd
			// 
			this.btnAdd.Location = new System.Drawing.Point(8, 16);
			this.btnAdd.Name = "btnAdd";
			this.btnAdd.Size = new System.Drawing.Size(80, 24);
			this.btnAdd.TabIndex = 0;
			this.btnAdd.Text = "&Add";
			this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);
			// 
			// sbStatus
			// 
			this.sbStatus.Location = new System.Drawing.Point(10, 342);
			this.sbStatus.Name = "sbStatus";
			this.sbStatus.Panels.AddRange(new System.Windows.Forms.StatusBarPanel[] {
																						this.sbPanel1, this.sbPanel2});
			this.sbStatus.Size = new System.Drawing.Size(492, 26);
			this.sbStatus.SizingGrip = false;
			this.sbStatus.TabIndex = 2;
			this.sbStatus.Text = "statusBar1";
			this.sbStatus.ShowPanels = true;
			// 
			// timer1
			// 
			this.timer1.Interval = 1000;
			this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
			// 
			// sbPanel1
			// 
			this.sbPanel1.AutoSize = System.Windows.Forms.StatusBarPanelAutoSize.Spring;
			this.sbPanel1.Text = "statusBarPanel1";
			this.sbPanel1.Width = 200;
			//
			// sbPanel2
			//
			this.sbPanel2.AutoSize = System.Windows.Forms.StatusBarPanelAutoSize.Spring;
			this.sbPanel2.Text = "Status";
			this.sbPanel2.Width = 510;
			// 
			// mainMenu1
			// 
			this.mainMenu1.MenuItems.AddRange(new System.Windows.Forms.MenuItem[] {
																					  this.menuItem1,
																					  this.menuItem7});
			// 
			// menuItem1
			// 
			this.menuItem1.Index = 0;
			this.menuItem1.MenuItems.AddRange(new System.Windows.Forms.MenuItem[] {
																					  this.menuItem2,
																					  this.menuItem3,
																					  this.menuItem4,
																					  this.menuItem5,
																					  this.menuItem6});
			this.menuItem1.Text = "&File";
			// 
			// menuItem2
			// 
			this.menuItem2.Index = 0;
			this.menuItem2.Text = "&Add";
			this.menuItem2.Click += new System.EventHandler(this.menuItem2_Click);
			// 
			// menuItem3
			// 
			this.menuItem3.Index = 1;
			this.menuItem3.Text = "&Edit";
			this.menuItem3.Click += new System.EventHandler(this.menuItem3_Click);
			// 
			// menuItem4
			// 
			this.menuItem4.Index = 2;
			this.menuItem4.Text = "&Remove";
			this.menuItem4.Click += new System.EventHandler(this.menuItem4_Click);
			// 
			// menuItem5
			// 
			this.menuItem5.Index = 3;
			this.menuItem5.Text = "-";
			// 
			// menuItem6
			// 
			this.menuItem6.Index = 4;
			this.menuItem6.Text = "E&xit";
			this.menuItem6.Click += new System.EventHandler(this.menuItem6_Click);
			// 
			// menuItem7
			// 
			this.menuItem7.Index = 1;
			this.menuItem7.Text = "A&bout";
			this.menuItem7.Click += new System.EventHandler(this.menuItem7_Click);
			// 
			// frmMain
			// 
			this.AutoScaleBaseSize = new System.Drawing.Size(6, 15);
			this.ClientSize = new System.Drawing.Size(512, 368);
			this.Controls.Add(this.sbStatus);
			this.Controls.Add(this.pnTop);
			this.Controls.Add(this.pnBottom);
			this.DockPadding.All = 10;
			this.MaximizeBox = false;
			this.Menu = this.mainMenu1;
			this.Name = "frmMain";
			this.Text = "BillReminder";
			this.Load += new System.EventHandler(this.frmMain_Load);
			this.pnTop.ResumeLayout(false);
			this.pnBottom.ResumeLayout(false);
			((System.ComponentModel.ISupportInitialize)(this.sbPanel1)).EndInit();
			this.ResumeLayout(false);

		}
		#endregion

		/// <summary>
		/// The main entry point for the application.
		/// </summary>
		[STAThread]
		static void Main() 
		{
			Application.Run(new frmMain());
		}

		#region "Methods"

		private void RefreshForm(BillCollection bc) 
		{
			// Use this collection to display
			this.billsToDisplay = bc;

			// Refresh ListView
			this.PopulateListView();
		}

		/// <summary>
		/// Formats the ListView object to conform with the layout
		/// needed to display records.
		/// </summary>
		private void FormatListView() 
		{
			this.lvBills.BeginUpdate();

			this.lvBills.GridLines = true;
			this.lvBills.FullRowSelect = true;
			this.lvBills.Items.Clear();
			this.lvBills.View = View.Details;

			this.lvBills.Columns.Clear();
			this.lvBills.Columns.Add("Payee",110,HorizontalAlignment.Center);
			this.lvBills.Columns.Add("Amount",80,HorizontalAlignment.Center);
			this.lvBills.Columns.Add("Due Date",80,HorizontalAlignment.Center);
			this.lvBills.Columns.Add("Status",80,HorizontalAlignment.Center);

			this.lvBills.EndUpdate();
		}
	
		/// <summary>
		/// Populates ListView object with records contained in the
		/// billsToDisplay collection.
		/// </summary>
		private void PopulateListView() 
		{
			// Resets ListView control
			this.lvBills.Items.Clear();
			this.lvBills.BeginUpdate();

			// TODO: Add sorting capability

			foreach (Bill b in this.config.Bills) 
			{
				ListViewItem iBill = new ListViewItem(b.Payee);
				iBill.SubItems.Add(b.AmountDue.ToString("c"));
				iBill.SubItems.Add(b.DueDate.ToShortDateString());
				iBill.SubItems.Add((((Status)(b.Status)).ToString()));
				iBill.Tag = b.Notes;

				// some color coding
				if (b.Paid == true)
				{
				    iBill.ForeColor = Color.Gray;
				}
				else if (b.Status == (int)Status.OverDue) 
				{
					iBill.ForeColor = Color.Red;
				} 
				else if (b.Status == (int)Status.Current)
				{
					iBill.ForeColor = Color.Green;
				} 
				else
				{
					iBill.ForeColor = Color.Blue;
				}

				this.lvBills.Items.Add(iBill);
			}

			this.lvBills.EndUpdate();

			if (this.lvBills.Items.Count > 0)
				this.lvBills.Items[0].Selected = true;
			this.lvBills.Select();

			Console.WriteLine("Count: " + this.lvBills.Items.Count.ToString());
			this.sbPanel1.Text = String.Format("Count: {0}",this.lvBills.Items.Count);
		}

		/// <summary>
		/// Routine used to add a new Bill to unpaid collection.
		/// </summary>
		private void AddBill() 
		{
			// Instantiate frmBillDialog form
			frmBillDialog w = new frmBillDialog();

			// Shows frmBillDialog.cs 
			w.ShowDialog(this);

			// Extract new Bill object
			Bill newBill = w.GetBill;

                        Console.WriteLine(w.DialogResult.ToString());

			// Check if Save was clicked and new bill was returned
			if ((w.DialogResult == DialogResult.OK) && (newBill != null))
				try 
				{
					//Add new bill to collection
					this.config.Bills.Add(newBill);
					//Automatically saves collection
					Configuration.Write();
					//Confirmation Message
					MessageBox.Show(string.Format("Bill: {0} added.",newBill));
					//Refresh form
					this.RefreshForm(this.config.Bills);
				}
				catch (ArgumentException ae) 
				{
					MessageBox.Show(ae.Message);
				}
			
			// Properly disposes of form
			w.Dispose();
		}

		/// <summary>
		/// Routine used to edit an existing Bill from unpaid collection.
		/// </summary>
		private void EditBill() 
		{
			// Paid bill instance
			Bill b = null;

			// Extract individually selected unpaidBills
			foreach (ListViewItem item in this.lvBills.SelectedItems) 
			{
				// Temporary holder for selected unpaidBill
				b = new Bill();
				b.Payee = item.Text;
				b.AmountDue = Convert.ToDouble(item.SubItems[1].Text.Remove(0,1));
				b.DueDate = Convert.ToDateTime(item.SubItems[2].Text);
		
				// Get actual object reference from collection
				BillCollection bc = this.config.Bills.Search(b.Payee, b.DueDate,b.AmountDue);

				// Shouldn't really loop since only one object should exist
				foreach (Bill c in bc) 
				{
					// Get index of Bill within original collection
					int idx = this.config.Bills.IndexOf(c);

					// Instantiate new window
					frmBillDialog w = new frmBillDialog();
					// Assign selected bill to bill holder
					w.GetBill = c;
					// Show window
					w.ShowDialog(this);

					// If user did NOT cancel action
					if (w.DialogResult != DialogResult.Cancel) 
					{
						// Get object back
						this.config.Bills[idx] = w.GetBill;

						//Serialize it
						Configuration.Write();
						//Refresh form
						this.RefreshForm(this.config.Bills);

						// Properly disposes of window
						w.Dispose();
					}
				}		
			}
		}

		/// <summary>
		/// Routine used to remove an existing Bill from unpaid collection.
		/// </summary>
		private void RemoveBill() 
		{
			// Paid bill instance
			Bill b = null;

			// Extract individually selected unpaidBills
			foreach (ListViewItem item in this.lvBills.SelectedItems) 
			{
				// Temporary holder for selected unpaidBill
				b = new Bill();
				b.Payee = item.Text;
				b.AmountDue = Convert.ToDouble(item.SubItems[1].Text.Remove(0,1));
				b.DueDate = Convert.ToDateTime(item.SubItems[2].Text);
		
				// Get actual object reference from collection
				BillCollection bc = this.config.Bills.Search(b.Payee, b.DueDate,b.AmountDue);

				// Shouldn't really loop since only one object should exist
				foreach (Bill c in bc) 
				{
					// Get index of Bill within original collection
					int idx = this.config.Bills.IndexOf(c);

					// Remove bill from collection
					this.config.Bills.RemoveAt(idx);
				}
			}

			//Serialize it
			Configuration.Write();
			//Refresh form
			this.RefreshForm(this.config.Bills);
		}

		/// <summary>
		/// Marks an existing Bill as "paid" and moves it from the 
		/// unpaid collection to the paid collection.
		/// </summary>
		private void PayBill() 
		{
			// Paid bill instance
			Bill b = null;

			// Extract individually selected unpaidBills
			foreach (ListViewItem item in this.lvBills.SelectedItems) 
			{
				// Temporary holder for selected unpaidBill
				b = new Bill();
				b.Payee = item.Text;
				b.AmountDue = Convert.ToDouble(item.SubItems[1].Text.Remove(0,1));
				b.DueDate = Convert.ToDateTime(item.SubItems[2].Text);
		
				// Get actual object reference from collection
				BillCollection bc = this.config.Bills.Search(b.Payee, b.DueDate,b.AmountDue);

				// Shouldn't really loop since only one object should exist
				foreach (Bill c in bc) 
				{
					// Get index of Bill within original collection
					int idx = this.config.Bills.IndexOf(c);

					// Mark it as paid
					this.config.Bills[idx].Paid = true;
					
					// Add it to Paid collection
					//if (!this.config.PaidBills.Contains(c))
						//this.config.PaidBills.Add(c);

					// Remove bill from collection
					//this.config.Bills.RemoveAt(idx);
				}
			}

			//Serialize it both paid and unpaid collections
			Configuration.Write();
			//Configuration.Write(Configuration.BillType.Paid);
			//Refresh form
			this.RefreshForm(this.config.Bills);
		}

		private void DisplayLateBills() 
		{
			// Calculate offset to midnight
			this.timer1.Interval = this.MillisecondsToMidnight();

			//Used to hold list of (over)due bills
			StringBuilder msg = new StringBuilder();

			msg.Append("The following bills are due:\n\n");

			if (this.config.Bills.Count > 0)
			{
				foreach (Bill b in this.config.Bills)
					if (b.Status != (int)Status.Current)
						msg.Append(String.Format("{0}  -  {1}\n", b.Payee, b.AmountDue.ToString("c")));
						

				/// TODO:
				/// Check if previous instance of AlertWindow already exists
				/// in which case we want to re-use it.
				
				// Displays list of late/due bills in a window
				frmAlert aw = new frmAlert(msg.ToString(),"Overdue");
				aw.ShowDialog();
				aw.Dispose();
				aw = null;
			}
			
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
		
		#endregion

		private void menuItem2_Click(object sender, System.EventArgs e)
		{
			// Add
		
		}

		private void menuItem3_Click(object sender, System.EventArgs e)
		{
			// Edit
		
		}

		private void menuItem4_Click(object sender, System.EventArgs e)
		{
			// Remove
		
		}

		private void menuItem6_Click(object sender, System.EventArgs e)
		{
			// Exit
		
		}

		private void menuItem7_Click(object sender, System.EventArgs e)
		{
			// About
			frmAbout about = new frmAbout();
			about.ShowDialog();

			about.Dispose();
			about = null;
		
		}

		private void btnAdd_Click(object sender, System.EventArgs e)
		{
			this.AddBill();
		}

		private void btnRemove_Click(object sender, System.EventArgs e)
		{
			this.RemoveBill();
		}

		private void btnEdit_Click(object sender, System.EventArgs e)
		{
			this.EditBill();
		}

		private void btnPaid_Click(object sender, System.EventArgs e)
		{
			this.PayBill();
		}

		private void btnExit_Click(object sender, System.EventArgs e)
		{
			this.Close();
		}

		private void frmMain_Load(object sender, System.EventArgs e)
		{
		
		}
		
		private void timer1_Tick(object sender, System.EventArgs e)
		{
//			this.timer1.Interval = this.MillisecondsToMidnight();

			this.DisplayLateBills();

		}
		
	}
}

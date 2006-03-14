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

namespace BillReminder
{
	/// <summary>
	/// Summary description for Display.
	/// </summary>
	public class Display : System.Windows.Forms.Form
	{
		// Singleton
		private Configuration config;
		// Temporary container
		private BillCollection billsToDisplay;

		private System.Windows.Forms.Panel panel1;
		private System.Windows.Forms.ListView lvDisplay;
		private System.Windows.Forms.Panel panel2;
		private System.Windows.Forms.Button btnPaid;
		private System.Windows.Forms.Button btnEdit;
		private System.Windows.Forms.Button btnRemoveBill;
		private System.Windows.Forms.Button btnAddBill;
		private System.Windows.Forms.Button btnClose;

		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.Container components = null;

		public Display(BillCollection bc)
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			//Configuration Singleton class
			this.config = Configuration.Instance();
			
			// Initializes temporary container
			this.Records = bc;
			
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
			this.panel1 = new System.Windows.Forms.Panel();
			this.lvDisplay = new System.Windows.Forms.ListView();
			this.panel2 = new System.Windows.Forms.Panel();
			this.btnPaid = new System.Windows.Forms.Button();
			this.btnEdit = new System.Windows.Forms.Button();
			this.btnRemoveBill = new System.Windows.Forms.Button();
			this.btnAddBill = new System.Windows.Forms.Button();
			this.btnClose = new System.Windows.Forms.Button();
			this.panel1.SuspendLayout();
			this.panel2.SuspendLayout();
			this.SuspendLayout();
			// 
			// panel1
			// 
			this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.panel1.Controls.Add(this.lvDisplay);
			this.panel1.DockPadding.All = 5;
			this.panel1.Location = new System.Drawing.Point(5, 8);
			this.panel1.Name = "panel1";
			this.panel1.Size = new System.Drawing.Size(395, 256);
			this.panel1.TabIndex = 0;
			// 
			// lvDisplay
			// 
			this.lvDisplay.Dock = System.Windows.Forms.DockStyle.Fill;
			this.lvDisplay.Location = new System.Drawing.Point(5, 5);
			this.lvDisplay.Name = "lvDisplay";
			this.lvDisplay.Size = new System.Drawing.Size(383, 244);
			this.lvDisplay.TabIndex = 0;
			// 
			// panel2
			// 
			this.panel2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.panel2.Controls.Add(this.btnClose);
			this.panel2.Controls.Add(this.btnPaid);
			this.panel2.Controls.Add(this.btnEdit);
			this.panel2.Controls.Add(this.btnRemoveBill);
			this.panel2.Controls.Add(this.btnAddBill);
			this.panel2.Location = new System.Drawing.Point(408, 8);
			this.panel2.Name = "panel2";
			this.panel2.Size = new System.Drawing.Size(88, 256);
			this.panel2.TabIndex = 1;
			// 
			// btnPaid
			// 
			this.btnPaid.Location = new System.Drawing.Point(8, 112);
			this.btnPaid.Name = "btnPaid";
			this.btnPaid.Size = new System.Drawing.Size(72, 24);
			this.btnPaid.TabIndex = 13;
			this.btnPaid.Text = "Paid";
			this.btnPaid.Click += new System.EventHandler(this.btnPaid_Click);
			// 
			// btnEdit
			// 
			this.btnEdit.Location = new System.Drawing.Point(8, 48);
			this.btnEdit.Name = "btnEdit";
			this.btnEdit.Size = new System.Drawing.Size(72, 24);
			this.btnEdit.TabIndex = 12;
			this.btnEdit.Text = "Edit";
			this.btnEdit.Click += new System.EventHandler(this.btnEdit_Click);
			// 
			// btnRemoveBill
			// 
			this.btnRemoveBill.Location = new System.Drawing.Point(8, 80);
			this.btnRemoveBill.Name = "btnRemoveBill";
			this.btnRemoveBill.Size = new System.Drawing.Size(72, 24);
			this.btnRemoveBill.TabIndex = 11;
			this.btnRemoveBill.Text = "Remove";
			this.btnRemoveBill.Click += new System.EventHandler(this.btnRemoveBill_Click);
			// 
			// btnAddBill
			// 
			this.btnAddBill.Location = new System.Drawing.Point(8, 16);
			this.btnAddBill.Name = "btnAddBill";
			this.btnAddBill.Size = new System.Drawing.Size(72, 24);
			this.btnAddBill.TabIndex = 10;
			this.btnAddBill.Text = "Add";
			this.btnAddBill.Click += new System.EventHandler(this.btnAddBill_Click);
			// 
			// btnClose
			// 
			this.btnClose.Location = new System.Drawing.Point(8, 216);
			this.btnClose.Name = "btnClose";
			this.btnClose.Size = new System.Drawing.Size(72, 24);
			this.btnClose.TabIndex = 14;
			this.btnClose.Text = "Close";
			this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
			// 
			// Display
			// 
			this.AutoScaleBaseSize = new System.Drawing.Size(6, 15);
			this.ClientSize = new System.Drawing.Size(506, 268);
			this.Controls.Add(this.panel2);
			this.Controls.Add(this.panel1);
			this.DockPadding.All = 5;
			this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
			this.MaximizeBox = false;
			this.Name = "Display";
			this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
			this.Text = "Display";
			this.panel1.ResumeLayout(false);
			this.panel2.ResumeLayout(false);
			this.ResumeLayout(false);

		}
		#endregion

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
			this.lvDisplay.BeginUpdate();

			this.lvDisplay.GridLines = true;
			this.lvDisplay.FullRowSelect = true;
			this.lvDisplay.Items.Clear();
			this.lvDisplay.View = View.Details;

			this.lvDisplay.Columns.Clear();
			this.lvDisplay.Columns.Add("Payee",190,HorizontalAlignment.Center);
			this.lvDisplay.Columns.Add("Amount",80,HorizontalAlignment.Center);
			this.lvDisplay.Columns.Add("Due Date",80,HorizontalAlignment.Center);

			this.lvDisplay.EndUpdate();
		}
	
		/// <summary>
		/// Populates ListView object with records contained in the
		/// billsToDisplay collection.
		/// </summary>
		private void PopulateListView() 
		{
			// Resets ListView control
			this.lvDisplay.Items.Clear();
			this.lvDisplay.BeginUpdate();

			// TODO: Add sorting capability

			foreach (Bill b in this.billsToDisplay) 
			{
				ListViewItem iBill = new ListViewItem(b.Payee);
				iBill.SubItems.Add(b.AmountDue.ToString("c"));
				iBill.SubItems.Add(b.DueDate.ToShortDateString());
				iBill.Tag = b.Notes;

				// some color coding
				if (b.Status == (int)Status.OverDue) 
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

				this.lvDisplay.Items.Add(iBill);
			}

			this.lvDisplay.EndUpdate();

			if (this.lvDisplay.Items.Count > 0)
				this.lvDisplay.Items[0].Selected = true;
			this.lvDisplay.Select();

			//this.statusBar1.Panels[0].Text = String.Format("Count: {0}",this.listView1.Items.Count);
		}

		/// <summary>
		/// Routine used to add a new Bill to unpaid collection.
		/// </summary>
		private void AddBill() 
		{
			// Instantiate NewBill form
			NewBill w = new NewBill();

			// Shows NewBill.cs 
			w.ShowDialog(this);

			// Extract new Bill object
			Bill newBill = w.GetBill;

                        Console.WriteLine(w.DialogResult.ToString());

			// Check if Save was clicked and new bill was returned
			if ((w.DialogResult == DialogResult.OK) && (newBill != null))
				try 
				{
					//Add new bill to collection
					this.config.UnpaidBills.Add(newBill);
					//Automatically saves collection
					Configuration.Write(Configuration.BillType.Unpaid);
					//Confirmation Message
					MessageBox.Show(string.Format("Bill: {0} added.",newBill));
					//Refresh form
					this.RefreshForm(this.config.UnpaidBills);
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
			foreach (ListViewItem item in this.lvDisplay.SelectedItems) 
			{
				// Temporary holder for selected unpaidBill
				b = new Bill();
				b.Payee = item.Text;
				b.AmountDue = Convert.ToDouble(item.SubItems[1].Text.Remove(0,1));
				b.DueDate = Convert.ToDateTime(item.SubItems[2].Text);
		
				// Get actual object reference from collection
				BillCollection bc = this.config.UnpaidBills.Search(b.Payee, b.DueDate,b.AmountDue);

				// Shouldn't really loop since only one object should exist
				foreach (Bill c in bc) 
				{
					// Get index of Bill within original collection
					int idx = this.config.UnpaidBills.IndexOf(c);

					// Instantiate new window
					NewBill w = new NewBill();
					// Assign selected bill to bill holder
					w.GetBill = c;
					// Show window
					w.ShowDialog(this);

					// If user did NOT cancel action
					if (w.DialogResult != DialogResult.Cancel) 
					{
						// Get object back
						this.config.UnpaidBills[idx] = w.GetBill;

						//Serialize it
						Configuration.Write(Configuration.BillType.Unpaid);
						//Refresh form
						this.RefreshForm(this.config.UnpaidBills);

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
			foreach (ListViewItem item in this.lvDisplay.SelectedItems) 
			{
				// Temporary holder for selected unpaidBill
				b = new Bill();
				b.Payee = item.Text;
				b.AmountDue = Convert.ToDouble(item.SubItems[1].Text.Remove(0,1));
				b.DueDate = Convert.ToDateTime(item.SubItems[2].Text);
		
				// Get actual object reference from collection
				BillCollection bc = this.config.UnpaidBills.Search(b.Payee, b.DueDate,b.AmountDue);

				// Shouldn't really loop since only one object should exist
				foreach (Bill c in bc) 
				{
					// Get index of Bill within original collection
					int idx = this.config.UnpaidBills.IndexOf(c);

					// Remove bill from collection
					this.config.UnpaidBills.RemoveAt(idx);
				}
			}

			//Serialize it
			Configuration.Write(Configuration.BillType.Unpaid);
			//Refresh form
			this.RefreshForm(this.config.UnpaidBills);
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
			foreach (ListViewItem item in this.lvDisplay.SelectedItems) 
			{
				// Temporary holder for selected unpaidBill
				b = new Bill();
				b.Payee = item.Text;
				b.AmountDue = Convert.ToDouble(item.SubItems[1].Text.Remove(0,1));
				b.DueDate = Convert.ToDateTime(item.SubItems[2].Text);
		
				// Get actual object reference from collection
				BillCollection bc = this.config.UnpaidBills.Search(b.Payee, b.DueDate,b.AmountDue);

				// Shouldn't really loop since only one object should exist
				foreach (Bill c in bc) 
				{
					// Get index of Bill within original collection
					int idx = this.config.UnpaidBills.IndexOf(c);

					// Add it to Paid collection
					if (!this.config.PaidBills.Contains(c))
						this.config.PaidBills.Add(c);

					// Remove bill from collection
					this.config.UnpaidBills.RemoveAt(idx);
				}
			}

			//Serialize it both paid and unpaid collections
			Configuration.Write(Configuration.BillType.Unpaid);
			Configuration.Write(Configuration.BillType.Paid);
			//Refresh form
			this.RefreshForm(this.config.UnpaidBills);
		}

		#endregion

		#region "Events"

		private void btnAddBill_Click(object sender, System.EventArgs e)
		{
			this.AddBill();
		}

		private void btnEdit_Click(object sender, System.EventArgs e)
		{
			this.EditBill();
		}

		private void btnRemoveBill_Click(object sender, System.EventArgs e)
		{
			this.RemoveBill();
		}

		private void btnPaid_Click(object sender, System.EventArgs e)
		{
			this.PayBill();
		}

		private void btnClose_Click(object sender, System.EventArgs e)
		{
			this.Close();
		}

		#endregion



		#region "Properties"

		private BillCollection Records 
		{
//			get 
//			{ 
//				return this.config.SearchedBills;
//			}

			set 
			{
				if (value != null)
					this.billsToDisplay = value;
				else
					this.billsToDisplay = this.config.UnpaidBills;
			}
		}

		
		#endregion

	}
}

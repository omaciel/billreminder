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
	/// Summary description for Search.
	/// </summary>
	public class Search : System.Windows.Forms.Form
	{
		private Configuration config;

		private System.Windows.Forms.Panel panel1;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.Label label4;
		private System.Windows.Forms.Panel panel2;
		private System.Windows.Forms.ComboBox cboPayee;
		private System.Windows.Forms.DateTimePicker dtpDueDate;
		private System.Windows.Forms.TextBox txtAmountDue;
		private System.Windows.Forms.TextBox txtNotes;
		private System.Windows.Forms.Button btnSearch;
		private System.Windows.Forms.Button btnClear;
		private System.Windows.Forms.Button btnCancel;
		private System.Windows.Forms.CheckBox chkDueDate;
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.Container components = null;

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
			//System.Resources.ResourceManager resources = new System.Resources.ResourceManager(typeof(Search));
			this.panel1 = new System.Windows.Forms.Panel();
			this.chkDueDate = new System.Windows.Forms.CheckBox();
			this.txtNotes = new System.Windows.Forms.TextBox();
			this.label4 = new System.Windows.Forms.Label();
			this.txtAmountDue = new System.Windows.Forms.TextBox();
			this.label3 = new System.Windows.Forms.Label();
			this.dtpDueDate = new System.Windows.Forms.DateTimePicker();
			this.label2 = new System.Windows.Forms.Label();
			this.cboPayee = new System.Windows.Forms.ComboBox();
			this.label1 = new System.Windows.Forms.Label();
			this.panel2 = new System.Windows.Forms.Panel();
			this.btnCancel = new System.Windows.Forms.Button();
			this.btnClear = new System.Windows.Forms.Button();
			this.btnSearch = new System.Windows.Forms.Button();
			this.panel1.SuspendLayout();
			this.panel2.SuspendLayout();
			this.SuspendLayout();
			// 
			// panel1
			// 
			this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.panel1.Controls.Add(this.chkDueDate);
			this.panel1.Controls.Add(this.txtNotes);
			this.panel1.Controls.Add(this.label4);
			this.panel1.Controls.Add(this.txtAmountDue);
			this.panel1.Controls.Add(this.label3);
			this.panel1.Controls.Add(this.dtpDueDate);
			this.panel1.Controls.Add(this.label2);
			this.panel1.Controls.Add(this.cboPayee);
			this.panel1.Controls.Add(this.label1);
			this.panel1.Location = new System.Drawing.Point(8, 8);
			this.panel1.Name = "panel1";
			this.panel1.Size = new System.Drawing.Size(352, 192);
			this.panel1.TabIndex = 0;
			// 
			// chkDueDate
			// 
			this.chkDueDate.Location = new System.Drawing.Point(136, 40);
			this.chkDueDate.Name = "chkDueDate";
			this.chkDueDate.Size = new System.Drawing.Size(24, 24);
			this.chkDueDate.TabIndex = 1;
			this.chkDueDate.CheckedChanged += new System.EventHandler(this.chkDueDate_CheckedChanged);
			// 
			// txtNotes
			// 
			this.txtNotes.Enabled = false;
			this.txtNotes.Location = new System.Drawing.Point(136, 104);
			this.txtNotes.Multiline = true;
			this.txtNotes.Name = "txtNotes";
			this.txtNotes.Size = new System.Drawing.Size(184, 72);
			this.txtNotes.TabIndex = 5;
			this.txtNotes.Text = "textBox2";
			// 
			// label4
			// 
			this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label4.Location = new System.Drawing.Point(16, 104);
			this.label4.Name = "label4";
			this.label4.Size = new System.Drawing.Size(120, 24);
			this.label4.TabIndex = 6;
			this.label4.Text = "Note(s):";
			// 
			// txtAmountDue
			// 
			this.txtAmountDue.Location = new System.Drawing.Point(160, 72);
			this.txtAmountDue.Name = "txtAmountDue";
			this.txtAmountDue.Size = new System.Drawing.Size(160, 22);
			this.txtAmountDue.TabIndex = 4;
			this.txtAmountDue.Text = "textBox1";
			this.txtAmountDue.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
			// 
			// label3
			// 
			this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label3.Location = new System.Drawing.Point(16, 72);
			this.label3.Name = "label3";
			this.label3.Size = new System.Drawing.Size(128, 24);
			this.label3.TabIndex = 4;
			this.label3.Text = "Amount:";
			// 
			// dtpDueDate
			// 
			this.dtpDueDate.Format = System.Windows.Forms.DateTimePickerFormat.Short;
			this.dtpDueDate.Location = new System.Drawing.Point(160, 40);
			this.dtpDueDate.Name = "dtpDueDate";
			this.dtpDueDate.Size = new System.Drawing.Size(160, 22);
			this.dtpDueDate.TabIndex = 2;
			// 
			// label2
			// 
			this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label2.Location = new System.Drawing.Point(16, 40);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(112, 16);
			this.label2.TabIndex = 2;
			this.label2.Text = "Due Date:";
			// 
			// cboPayee
			// 
			this.cboPayee.Location = new System.Drawing.Point(136, 8);
			this.cboPayee.Name = "cboPayee";
			this.cboPayee.Size = new System.Drawing.Size(184, 24);
			this.cboPayee.TabIndex = 0;
			this.cboPayee.Text = "comboBox1";
			// 
			// label1
			// 
			this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label1.Location = new System.Drawing.Point(16, 8);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(104, 16);
			this.label1.TabIndex = 0;
			this.label1.Text = "Payee:";
			// 
			// panel2
			// 
			this.panel2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.panel2.Controls.Add(this.btnCancel);
			this.panel2.Controls.Add(this.btnClear);
			this.panel2.Controls.Add(this.btnSearch);
			this.panel2.Location = new System.Drawing.Point(8, 208);
			this.panel2.Name = "panel2";
			this.panel2.Size = new System.Drawing.Size(352, 40);
			this.panel2.TabIndex = 1;
			// 
			// btnCancel
			// 
			this.btnCancel.Location = new System.Drawing.Point(238, 8);
			this.btnCancel.Name = "btnCancel";
			this.btnCancel.Size = new System.Drawing.Size(96, 24);
			this.btnCancel.TabIndex = 2;
			this.btnCancel.Text = "Cancel";
			this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);
			// 
			// btnClear
			// 
			this.btnClear.Location = new System.Drawing.Point(127, 8);
			this.btnClear.Name = "btnClear";
			this.btnClear.Size = new System.Drawing.Size(96, 24);
			this.btnClear.TabIndex = 1;
			this.btnClear.Text = "Clear";
			this.btnClear.Click += new System.EventHandler(this.btnClear_Click);
			// 
			// btnSearch
			// 
			//this.btnSearch.Image = ((System.Drawing.Image)(resources.GetObject("btnSearch.Image")));
			this.btnSearch.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
			this.btnSearch.Location = new System.Drawing.Point(16, 8);
			this.btnSearch.Name = "btnSearch";
			this.btnSearch.Size = new System.Drawing.Size(96, 24);
			this.btnSearch.TabIndex = 0;
			this.btnSearch.Text = "Search";
			this.btnSearch.Click += new System.EventHandler(this.btnSearch_Click);
			// 
			// Search
			// 
			this.AutoScaleBaseSize = new System.Drawing.Size(6, 15);
			this.ClientSize = new System.Drawing.Size(368, 256);
			this.Controls.Add(this.panel2);
			this.Controls.Add(this.panel1);
			this.Name = "Search";
			this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
			this.Text = "Search";
			this.panel1.ResumeLayout(false);
			this.panel2.ResumeLayout(false);
			this.ResumeLayout(false);

		}
		#endregion

		#region "Constructors"

		public Search()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			//Singleton
			this.config = Configuration.Instance();

			// Reset the form
			this.ResetForm();
		}

		
		#endregion

		#region "Methods"

		private void ResetForm() 
		{
			this.cboPayee.Text = string.Empty;
			this.dtpDueDate.Value = System.DateTime.Today;
			this.txtAmountDue.Text = string.Empty;

			//TODO: Proper text search within notes
			this.txtNotes.Text = string.Empty;
			this.txtNotes.Enabled = false;

			this.chkDueDate.Checked = false;

			this.PopulatePayee();
		}
		
		private void PopulatePayee() 
		{
			if (this.config.UnpaidBills.Count > 0) 
			{
				foreach (Bill b in this.config.UnpaidBills) 
				{
					string payee = b.Payee;
					if (!this.cboPayee.Items.Contains(payee))
						this.cboPayee.Items.Add(payee);
				}

			}
		}

		
		private void SearchBills() 
		{
			
			//This code could potentially be part of a subclassed text box
			double amnt = 0;
			
			if (this.txtAmountDue.Text.Length > 0)
				amnt = double.Parse(this.txtAmountDue.Text);

			//Only search by date if requested
			DateTime dt;

			if (this.chkDueDate.Checked)
				dt = this.dtpDueDate.Value;
			else
				dt = DateTime.MinValue;
			
			//New collection
			//this.searchResults = new BillCollection();
			//Returned Bills from search
			//this.searchResults = this.config.UnpaidBills.Search(this.cboPayee.Text, dt, amnt);

			this.config.SearchedBills = this.config.UnpaidBills.Search(this.cboPayee.Text, dt, amnt);

		}

		#endregion

		private void btnCancel_Click(object sender, System.EventArgs e)
		{
			this.Close();
		}

		private void btnClear_Click(object sender, System.EventArgs e)
		{
			this.ResetForm();
		}

		private void btnSearch_Click(object sender, System.EventArgs e)
		{
			this.SearchBills();

			if (this.config.SearchedBills == null)
				MessageBox.Show("No matches have been found!", "Search Results");
			this.Close();
		}

		private void chkDueDate_CheckedChanged(object sender, System.EventArgs e)
		{
			// dtpDueDate toggle
			if (this.chkDueDate.Checked)
				this.dtpDueDate.Enabled = true;
			else
				this.dtpDueDate.Enabled = false;
		}




	}
}

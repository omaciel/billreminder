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
using System.Globalization;

namespace BillReminder
{
	/// <summary>
	/// Summary description for frmBillDialog.
	/// </summary>
	public class frmBillDialog : System.Windows.Forms.Form
	{
	
		private Configuration config;
		private Bill m_Bill;
		
		private System.Windows.Forms.Panel pnLeft;
		private System.Windows.Forms.MonthCalendar mcCalendar;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.ComboBox cboPayee;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.TextBox txtAmount;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.TextBox txtNotes;
		private System.Windows.Forms.Panel pnRight;
		private System.Windows.Forms.Button btnSave;
		private System.Windows.Forms.Button btnClear;
		private System.Windows.Forms.Button btnCancel;
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.Container components = null;

		public frmBillDialog(string title)
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			// Sets window title
			this.Text = title;
			
			this.config = Configuration.Instance();
			this.PopulatePayee();
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
			this.pnLeft = new System.Windows.Forms.Panel();
			this.mcCalendar = new System.Windows.Forms.MonthCalendar();
			this.label1 = new System.Windows.Forms.Label();
			this.cboPayee = new System.Windows.Forms.ComboBox();
			this.label2 = new System.Windows.Forms.Label();
			this.txtAmount = new System.Windows.Forms.TextBox();
			this.label3 = new System.Windows.Forms.Label();
			this.txtNotes = new System.Windows.Forms.TextBox();
			this.pnRight = new System.Windows.Forms.Panel();
			this.btnSave = new System.Windows.Forms.Button();
			this.btnClear = new System.Windows.Forms.Button();
			this.btnCancel = new System.Windows.Forms.Button();
			this.pnLeft.SuspendLayout();
			this.pnRight.SuspendLayout();
			this.SuspendLayout();
			// 
			// pnLeft
			// 
			this.pnLeft.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.pnLeft.Controls.Add(this.txtNotes);
			this.pnLeft.Controls.Add(this.label3);
			this.pnLeft.Controls.Add(this.txtAmount);
			this.pnLeft.Controls.Add(this.label2);
			this.pnLeft.Controls.Add(this.cboPayee);
			this.pnLeft.Controls.Add(this.label1);
			this.pnLeft.Controls.Add(this.mcCalendar);
			this.pnLeft.Location = new System.Drawing.Point(8, 8);
			this.pnLeft.Name = "pnLeft";
			this.pnLeft.Size = new System.Drawing.Size(424, 248);
			this.pnLeft.TabIndex = 0;
			// 
			// mcCalendar
			// 
			this.mcCalendar.Location = new System.Drawing.Point(8, 8);
			this.mcCalendar.Name = "mcCalendar";
			this.mcCalendar.TabIndex = 0;
			// 
			// label1
			// 
			this.label1.Location = new System.Drawing.Point(256, 8);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(160, 16);
			this.label1.TabIndex = 1;
			this.label1.Text = "Payee:";
			// 
			// cboPayee
			// 
			this.cboPayee.Location = new System.Drawing.Point(256, 32);
			this.cboPayee.Name = "cboPayee";
			this.cboPayee.Size = new System.Drawing.Size(160, 24);
			this.cboPayee.TabIndex = 2;
			this.cboPayee.Text = "";
			// 
			// label2
			// 
			this.label2.Location = new System.Drawing.Point(256, 64);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(160, 16);
			this.label2.TabIndex = 3;
			this.label2.Text = "Amount:";
			// 
			// txtAmount
			// 
			this.txtAmount.Location = new System.Drawing.Point(256, 88);
			this.txtAmount.Name = "txtAmount";
			this.txtAmount.Size = new System.Drawing.Size(160, 22);
			this.txtAmount.TabIndex = 4;
			this.txtAmount.Text = "";
			// 
			// label3
			// 
			this.label3.Location = new System.Drawing.Point(256, 120);
			this.label3.Name = "label3";
			this.label3.Size = new System.Drawing.Size(160, 16);
			this.label3.TabIndex = 5;
			this.label3.Text = "Notes:";
			// 
			// txtNotes
			// 
			this.txtNotes.Location = new System.Drawing.Point(256, 144);
			this.txtNotes.Multiline = true;
			this.txtNotes.Name = "txtNotes";
			this.txtNotes.Size = new System.Drawing.Size(160, 40);
			this.txtNotes.TabIndex = 6;
			this.txtNotes.Text = "";
			// 
			// pnRight
			// 
			this.pnRight.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.pnRight.Controls.Add(this.btnCancel);
			this.pnRight.Controls.Add(this.btnClear);
			this.pnRight.Controls.Add(this.btnSave);
			this.pnRight.Location = new System.Drawing.Point(440, 8);
			this.pnRight.Name = "pnRight";
			this.pnRight.Size = new System.Drawing.Size(96, 248);
			this.pnRight.TabIndex = 1;
			// 
			// btnSave
			// 
			this.btnSave.Location = new System.Drawing.Point(8, 8);
			this.btnSave.Name = "btnSave";
			this.btnSave.Size = new System.Drawing.Size(80, 24);
			this.btnSave.TabIndex = 0;
			this.btnSave.Text = "&Save";
			this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
			// 
			// btnClear
			// 
			this.btnClear.Location = new System.Drawing.Point(8, 40);
			this.btnClear.Name = "btnClear";
			this.btnClear.Size = new System.Drawing.Size(80, 24);
			this.btnClear.TabIndex = 1;
			this.btnClear.Text = "Clear";
			this.btnClear.Click += new System.EventHandler(this.btnClear_Click);
			// 
			// btnCancel
			// 
			this.btnCancel.Location = new System.Drawing.Point(8, 168);
			this.btnCancel.Name = "btnCancel";
			this.btnCancel.Size = new System.Drawing.Size(80, 24);
			this.btnCancel.TabIndex = 2;
			this.btnCancel.Text = "Cancel";
			this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);
			// 
			// frmBillDialog
			// 
			this.AutoScaleBaseSize = new System.Drawing.Size(6, 15);
			this.ClientSize = new System.Drawing.Size(576, 256);
			this.Controls.Add(this.pnRight);
			this.Controls.Add(this.pnLeft);
			this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
			this.MaximizeBox = false;
			this.MinimizeBox = false;
			this.Name = "frmBillDialog";
			this.Text = "frmBillDialog";
			this.Load += new System.EventHandler(this.BillDialog_Load);
			this.Closed += new System.EventHandler(this.BillDialog_Closed);
			this.pnLeft.ResumeLayout(false);
			this.pnRight.ResumeLayout(false);
			this.ResumeLayout(false);

		}
		#endregion

		#region "Events"

		private void btnSave_Click(object sender, System.EventArgs e)
		{
			// TODO: Call validating routine

			// Creates bill object
                        this.CreateBill();

                        this.ClosingRoutine();
		}

		private void btnCancel_Click(object sender, System.EventArgs e)
		{
			// Null bill object is passed back
                        this.m_Bill = null;
			
                        this.ClosingRoutine();
		}

		private void btnClear_Click(object sender, System.EventArgs e)
		{
			this.PopulateForm();
		}

		private void BillDialog_Load(object sender, System.EventArgs e)
		{
			this.PopulateForm();
		}

		private void BillDialog_Closed(object sender, System.EventArgs e)
		{
		        this.ClosingRoutine();
		}

		#endregion

		#region "Methods"

                private void ClosingRoutine()
                {
                        if (this.m_Bill == null)
				this.DialogResult = DialogResult.Cancel;
			else
				this.DialogResult = DialogResult.OK;

                        this.Close();
                }

		private void PopulateForm() 
		{
			if (this.m_Bill != null) 
			{
				//Populate Bill object
				this.cboPayee.Text = this.m_Bill.Payee;
				this.txtAmount.Text = this.m_Bill.AmountDue.ToString();
				this.mcCalendar.SetDate(this.m_Bill.DueDate);
				this.txtNotes.Text = this.m_Bill.Notes;

				//Disable Clear button
				this.btnClear.Enabled = false;
			} 
			else 
			{
				this.ResetForm();
			}
		}

		private void ResetForm() 
		{
			this.mcCalendar.SetDate(System.DateTime.Today);
			this.txtAmount.Text = string.Empty;
			this.txtNotes.Text = string.Empty;
		}

		private void CreateBill() 
		{
			this.m_Bill = new Bill();
			this.m_Bill.Payee = this.cboPayee.Text;
			this.m_Bill.DueDate = this.mcCalendar.SelectionEnd;
			// Keep in mind globalization
                        this.m_Bill.AmountDue = double.Parse(this.txtAmount.Text, NumberStyles.Currency, CultureInfo.CurrentCulture);
			this.m_Bill.Notes = this.txtNotes.Text;
		}

		private void PopulatePayee() 
		{
			if (config.Bills.Count > 0) 
			{
				foreach (Bill b in config.Bills) 
				{
					string payee = b.Payee;
					if (!this.cboPayee.Items.Contains(payee))
						this.cboPayee.Items.Add(payee);
				}

			}
		}

		#endregion

		#region "Properties"
		
		public Bill GetBill 
		{
			get { return this.m_Bill;}
			set { this.m_Bill = value;}
		}
		
		
		#endregion
		
	}
}

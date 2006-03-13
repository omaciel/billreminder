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
	/// Summary description for NewBill.
	/// </summary>
	public class NewBill : System.Windows.Forms.Form
	{
		private Configuration config;
		private Bill m_Bill;
		
		private System.Windows.Forms.Panel panel1;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.TextBox txtAmount;
		private System.Windows.Forms.Label label4;
		private System.Windows.Forms.TextBox txtNotes;
		private System.Windows.Forms.Button btnAdd;
		private System.Windows.Forms.Button btnClear;
		private System.Windows.Forms.Button btnCancel;
		private System.Windows.Forms.ComboBox cboPayee;
		private System.Windows.Forms.DateTimePicker dtpDueDate;
		private System.Windows.Forms.Panel panel2;
		
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.Container components = null;

		#region "Constructors"

		/// <summary>
		/// Default constructor.
		/// </summary>
		public NewBill()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			this.config = Configuration.Instance();
			this.PopulatePayee();
		}

		#endregion

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
			this.dtpDueDate = new System.Windows.Forms.DateTimePicker();
			this.cboPayee = new System.Windows.Forms.ComboBox();
			this.txtNotes = new System.Windows.Forms.TextBox();
			this.label4 = new System.Windows.Forms.Label();
			this.txtAmount = new System.Windows.Forms.TextBox();
			this.label3 = new System.Windows.Forms.Label();
			this.label2 = new System.Windows.Forms.Label();
			this.label1 = new System.Windows.Forms.Label();
			this.btnCancel = new System.Windows.Forms.Button();
			this.btnClear = new System.Windows.Forms.Button();
			this.btnAdd = new System.Windows.Forms.Button();
			this.panel2 = new System.Windows.Forms.Panel();
			this.panel1.SuspendLayout();
			this.panel2.SuspendLayout();
			this.SuspendLayout();
			// 
			// panel1
			// 
			this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.panel1.Controls.Add(this.dtpDueDate);
			this.panel1.Controls.Add(this.cboPayee);
			this.panel1.Controls.Add(this.txtNotes);
			this.panel1.Controls.Add(this.label4);
			this.panel1.Controls.Add(this.txtAmount);
			this.panel1.Controls.Add(this.label3);
			this.panel1.Controls.Add(this.label2);
			this.panel1.Controls.Add(this.label1);
			this.panel1.Location = new System.Drawing.Point(10, 10);
			this.panel1.Name = "panel1";
			this.panel1.Size = new System.Drawing.Size(254, 220);
			this.panel1.TabIndex = 0;
			// 
			// dtpDueDate
			// 
			this.dtpDueDate.Format = System.Windows.Forms.DateTimePickerFormat.Short;
			this.dtpDueDate.Location = new System.Drawing.Point(88, 56);
			this.dtpDueDate.Name = "dtpDueDate";
			this.dtpDueDate.Size = new System.Drawing.Size(152, 22);
			this.dtpDueDate.TabIndex = 1;
			// 
			// cboPayee
			// 
			this.cboPayee.Location = new System.Drawing.Point(88, 16);
			this.cboPayee.Name = "cboPayee";
			this.cboPayee.Size = new System.Drawing.Size(152, 24);
			this.cboPayee.TabIndex = 0;
			// 
			// txtNotes
			// 
			this.txtNotes.Location = new System.Drawing.Point(88, 136);
			this.txtNotes.Multiline = true;
			this.txtNotes.Name = "txtNotes";
			this.txtNotes.Size = new System.Drawing.Size(152, 72);
			this.txtNotes.TabIndex = 3;
			this.txtNotes.Text = "";
			// 
			// label4
			// 
			this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label4.Location = new System.Drawing.Point(16, 135);
			this.label4.Name = "label4";
			this.label4.Size = new System.Drawing.Size(88, 24);
			this.label4.TabIndex = 6;
			this.label4.Text = "Notes:";
			// 
			// txtAmount
			// 
			this.txtAmount.Location = new System.Drawing.Point(88, 96);
			this.txtAmount.Name = "txtAmount";
			this.txtAmount.Size = new System.Drawing.Size(152, 22);
			this.txtAmount.TabIndex = 2;
			this.txtAmount.Text = "";
			// 
			// label3
			// 
			this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label3.Location = new System.Drawing.Point(16, 96);
			this.label3.Name = "label3";
			this.label3.Size = new System.Drawing.Size(96, 24);
			this.label3.TabIndex = 4;
			this.label3.Text = "Amount:";
			// 
			// label2
			// 
			this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label2.Location = new System.Drawing.Point(16, 57);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(88, 24);
			this.label2.TabIndex = 2;
			this.label2.Text = "Due Date:";
			// 
			// label1
			// 
			this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label1.Location = new System.Drawing.Point(16, 16);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(80, 24);
			this.label1.TabIndex = 0;
			this.label1.Text = "Payee:";
			// 
			// btnCancel
			// 
			this.btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
			this.btnCancel.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.btnCancel.ForeColor = System.Drawing.Color.Black;
			this.btnCancel.Location = new System.Drawing.Point(8, 176);
			this.btnCancel.Name = "btnCancel";
			this.btnCancel.Size = new System.Drawing.Size(72, 24);
			this.btnCancel.TabIndex = 2;
			this.btnCancel.Text = "Cancel";
			this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);
			// 
			// btnClear
			// 
			this.btnClear.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.btnClear.ForeColor = System.Drawing.Color.Black;
			this.btnClear.Location = new System.Drawing.Point(8, 48);
			this.btnClear.Name = "btnClear";
			this.btnClear.Size = new System.Drawing.Size(72, 24);
			this.btnClear.TabIndex = 1;
			this.btnClear.Text = "Clear";
			this.btnClear.Click += new System.EventHandler(this.btnClear_Click);
			// 
			// btnAdd
			// 
			this.btnAdd.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.btnAdd.ForeColor = System.Drawing.Color.Black;
			this.btnAdd.Location = new System.Drawing.Point(8, 16);
			this.btnAdd.Name = "btnAdd";
			this.btnAdd.Size = new System.Drawing.Size(72, 24);
			this.btnAdd.TabIndex = 0;
			this.btnAdd.Text = "Save";
			this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);
			// 
			// panel2
			// 
			this.panel2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.panel2.Controls.Add(this.btnClear);
			this.panel2.Controls.Add(this.btnAdd);
			this.panel2.Controls.Add(this.btnCancel);
			this.panel2.Location = new System.Drawing.Point(272, 10);
			this.panel2.Name = "panel2";
			this.panel2.Size = new System.Drawing.Size(96, 220);
			this.panel2.TabIndex = 11;
			// 
			// NewBill
			// 
			this.AutoScaleBaseSize = new System.Drawing.Size(6, 15);
			this.ClientSize = new System.Drawing.Size(376, 240);
			this.Controls.Add(this.panel2);
			this.Controls.Add(this.panel1);
			this.DockPadding.All = 10;
			this.MaximizeBox = false;
			this.Name = "NewBill";
			this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
			this.Text = "Add Bill";
			this.Load += new System.EventHandler(this.NewBill_Load);
			this.Closed += new EventHandler(this.NewBill_Closed);
			this.panel1.ResumeLayout(false);
			this.panel2.ResumeLayout(false);
			this.ResumeLayout(false);

		}
		#endregion

		#region "Events"

		private void btnAdd_Click(object sender, System.EventArgs e)
		{
			// TODO: Call validating routine

			this.CreateBill();

			this.Close();
		}

		private void btnCancel_Click(object sender, System.EventArgs e)
		{
			this.m_Bill = null;
			this.Close();
		}

		private void btnClear_Click(object sender, System.EventArgs e)
		{
			this.PopulateForm();
		}

		private void NewBill_Load(object sender, System.EventArgs e)
		{
			this.PopulateForm();
		}

		private void NewBill_Closed(object sender, System.EventArgs e)
		{
			if (this.m_Bill == null)
				this.DialogResult = DialogResult.Cancel;
			else
				this.DialogResult = DialogResult.OK;
		}

		#endregion

		#region "Methods"

		private void PopulateForm() 
		{
			if (this.m_Bill != null) 
			{
				//Populate Bill object
				this.cboPayee.Text = this.m_Bill.Payee;
				this.txtAmount.Text = this.m_Bill.AmountDue.ToString("c");
				this.dtpDueDate.Value = this.m_Bill.DueDate;
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
			this.dtpDueDate.Value = System.DateTime.Today;
			this.txtAmount.Text = string.Empty;
			this.txtNotes.Text = string.Empty;
		}

		private void CreateBill() 
		{
			this.m_Bill = new Bill();
			this.m_Bill.Payee = this.cboPayee.Text;
			this.m_Bill.DueDate = this.dtpDueDate.Value;
			this.m_Bill.AmountDue = Convert.ToDouble(this.txtAmount.Text.Remove(0,1));
			this.m_Bill.Notes = this.txtNotes.Text;
		}

		private void PopulatePayee() 
		{
			if (config.UnpaidBills.Count > 0) 
			{
				foreach (Bill b in config.UnpaidBills) 
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

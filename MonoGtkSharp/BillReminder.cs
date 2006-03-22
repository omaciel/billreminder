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
using System.IO;
using System.Xml;
using Gtk;
using Glade;

namespace BillReminder
{
class MainWindow {
	[Glade.Widget] Window frmMain;
	[Glade.Widget] Window frmAbout;
	[Glade.Widget] TreeView tvBills;

	TreeSelection selection;

	[Glade.Widget] Button btnAdd;
	[Glade.Widget] Button btnEdit;
	[Glade.Widget] Button btnRemove;
	[Glade.Widget] Button btnPaid;
	[Glade.Widget] Button btnQuit;
	[Glade.Widget] MenuItem mnuAbout;

	ListStore list;
	Configuration config;
	

	enum Columns {
		Payee,
		AmountDue,
		DueDate,
		Status
	}

	public MainWindow()
	{
		Glade.XML xml;

		/* Load our user interface */
		xml = new Glade.XML ("billreminder.glade", null, null);
		xml.Autoconnect (this);

		//Singleton
                this.config = Configuration.Instance();

                //FormatTreeView();

		
		
		/* Our on_selection_changed method will get called when the user
		 * clicks on a row in the list.
		 */
		selection = tvBills.Selection;
		selection.Changed += new EventHandler (on_selection_changed);

		/* Start with everything disabled */
		set_sensitivity (false);

		/* Set up everything */
		create_columns ();
		create_list ();
		
		PopulateListView();
		//load_phonebook ();
	}

	private void PopulateListView() 
        {
 
                if (this.config.Bills.Count > 0) 
		{
                	foreach (Bill b in this.config.Bills) 
			{
				list.AppendValues (b.Payee, b.AmountDue.ToString("c"), b.DueDate.ToShortDateString(),"*");
			}
 
			set_sensitivity(true);
		}
                
	}
	
	public void Show ()
	{
		frmMain.Show();
	}

	void create_columns ()
	{
		tvBills.AppendColumn ("Payee", new CellRendererText (), 
					"text", (int) Columns.Payee);

		tvBills.AppendColumn ("Amount Due", new CellRendererText (), 
					"text", (int) Columns.AmountDue);

		tvBills.AppendColumn ("Due Date", new CellRendererText (), 
					"text", (int) Columns.DueDate);

		tvBills.AppendColumn ("Status", new CellRendererText (), 
					"text", (int) Columns.Status);

	}

	void create_list ()
	{
		list = new ListStore (typeof (string), typeof (string), typeof (string), typeof (string));
		tvBills.Model = list;
	}

	void on_selection_changed (object o, EventArgs args)
	{
		bool has_selection;
		TreeModel model;
		TreeIter iter;

		// Get an iterator for the selected row, if any
		has_selection = selection.GetSelected (out model, out iter);

		// If nothing is selected, disable the other controls.  Otherwise, enable them.
		set_sensitivity (has_selection);

		/*
		if (has_selection) {
			// Use GetValue() and our iterator to get the values from the list
			name_entry.Text  = (string) list.GetValue (iter, (int) Columns.Name);
			phone_entry.Text = (string) list.GetValue (iter, (int) Columns.Phone);
			mail_entry.Text  = (string) list.GetValue (iter, (int) Columns.Mail);
		} else {
			name_entry.Text  = "";
			phone_entry.Text = "";
			mail_entry.Text  = "";
		}
		*/
	}
	
	void terminate()
	{
		Application.Quit();
	}

	void set_sensitivity (bool sensitive)
	{
		tvBills.Sensitive = sensitive;
		btnEdit.Sensitive = sensitive;
		btnRemove.Sensitive = sensitive;
		btnPaid.Sensitive = sensitive;
	}

	void on_frmMain_delete_event (object o, DeleteEventArgs args)
	{
		terminate();
		args.RetVal = true;
	}
	
	public void on_btnQuit_clicked (System.Object obj, EventArgs e) 
	{
                terminate(); 		
	}

	public void on_mnuAbout_activate (System.Object obj, EventArgs e) 
	{
                Console.WriteLine("About");
                frmAbout.Visible = true;
                
	}
}

class BillReminder {
	public static void Main ()
	{
		MainWindow br;

		Application.Init ();

		br = new MainWindow ();
		br.Show ();

		Application.Run ();
	}
}
}

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
using System.Xml.Serialization;


	/// <summary>
	/// Used to represent an instance of a Bill object.
	/// </summary>
[Serializable()]
public class Bill : IComparable
{
	#region "Class Variables"

	[XmlAttribute("m_Payee")] private string m_Payee;
	[XmlAttribute("m_DueDate")] private DateTime m_DueDate;
	[XmlAttribute("m_AmountDue")] private double m_AmountDue;
	[XmlAttribute("m_Notes")] private string m_Notes;
	[XmlAttribute("m_Paid")] private bool m_Paid = false;
	[XmlAttribute("m_Status")] private int m_Status;

	#endregion

	#region "Constructors"

	/// <summary>
	/// Default Bill constructor.
	/// </summary>
	public Bill(){}

	/// <summary>
	/// Bill Constructor.
	/// </summary>
	/// <param name="payee"></param>
	/// <param name="dueDate"></param>
	/// <param name="amountDue"></param>
	/// <param name="notes"></param>
	public Bill(string payee, DateTime dueDate, double amountDue, string notes) : this() 
	{
		this.m_Payee = payee;
		this.m_DueDate = dueDate;
		this.m_AmountDue = amountDue;
		this.m_Notes = notes;

//		this.GetStatus();
	}

	/// <summary>
	/// Bill Constructor.
	/// </summary>
	/// <param name="payee"></param>
	/// <param name="dueDate"></param>
	/// <param name="amountDue"></param>
	public Bill(string payee, DateTime dueDate, double amountDue) : this() 
	{
		this.m_Payee = payee;
		this.m_DueDate = dueDate;
		this.m_AmountDue = amountDue;
		this.m_Notes = string.Empty;
	}


	#endregion

	#region "Properties"

	/// <summary>
	/// Name for payee.
	/// </summary>
	public string Payee 
	{
		get { return this.m_Payee;}
		set { this.m_Payee = value;}
	}

	/// <summary>
	/// Due date for Bill.
	/// </summary>
	public DateTime DueDate 
	{
		get { return this.m_DueDate;}
		set 
		{ 
			this.m_DueDate = value;
			this.SetStatus();
		}
	}

	/// <summary>
	/// Amount due for Bill.
	/// </summary>
	public double AmountDue 
	{
		get { return this.m_AmountDue;}
		set { this.m_AmountDue = value;}
	}

	/// <summary>
	/// Notes associated to Bill.
	/// </summary>
	public string Notes 
	{
		get { return this.m_Notes;}
		set { this.m_Notes = value;}
	}

	/// <summary>
	/// Status of Bill.
	/// </summary>
	public bool Paid 
	{
		get { return this.m_Paid;}
		set { this.m_Paid = value;}
	}

	/// <summary>
	/// Status of Bill.
	/// </summary>
	public int Status
	{
		get { return this.m_Status;}
	}

	#endregion

	#region "Methods"

	/// <summary>
	/// String representation of Bill.
	/// </summary>
	/// <returns>Payee (AmountDue) - DueDate</returns>
	public override string ToString()
	{
		return this.m_Payee;
	}

	/// <summary>
	/// Used to properly compare Bill objects to one another.
	/// </summary>
	/// <param name="obj"></param>
	/// <returns>True or False</returns>
	public override bool Equals(Object obj) 
	{
		Bill b = (Bill)obj;
		return (this.Payee == b.Payee && this.DueDate  == b.DueDate && this.AmountDue == b.AmountDue );

	}

	public override int GetHashCode() 
	{
		return this.m_Payee.GetHashCode();
	}

	/// <summary>
	/// Returns Bill's current status:
	/// Overdue, Due, or Current.
	/// </summary>
	/// <returns>-1, 0, 1</returns>
	private int SetStatus()
	{
		DateTime today = DateTime.Today;

		if (this.m_DueDate < today)
			this.m_Status = -1;
		else if (this.m_DueDate == today)
			this.m_Status = 0;
		else
			this.m_Status = 1;

		return this.m_Status;
	}

	public bool Match(string payee)
	{
		return (this.Payee == payee);
	}

	public bool Match(DateTime dueDate)
	{
		return (this.DueDate == dueDate);
	}

	public bool Match(double amountDue)
	{
		return (this.AmountDue == amountDue );
	}

	public bool Match(Bill criteria)
	{
		bool retVal = true;

		if ((criteria.Payee != null) && (criteria.Payee != string.Empty))
			retVal = this.Match(criteria.Payee);
		else
			retVal = false;

		if (retVal)
		{
			if (criteria.DueDate != DateTime.MinValue)
				retVal = this.Match(criteria.DueDate);

			if (retVal)
			{
				if(criteria.AmountDue > 0)
					retVal = this.Match(criteria.AmountDue );
			}
		}

		return retVal;
	}


	#endregion

	#region IComparable Members

	public int CompareTo(object obj)
	{
		int isEqual = 0;

		isEqual = this.DueDate.CompareTo(((Bill)obj).DueDate);
		
		return isEqual * -1;
	}

	#endregion
}

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
using System.Collections;
using System.Xml;
using System.Xml.Serialization;

/// <summary>
/// A simple collection of Bills.
/// </summary>
[Serializable()]
public class BillCollection : CollectionBase
{
	/// <summary>
	/// Default constructor
	/// </summary>
	public BillCollection()
	{
	}

	/// <summary>
	/// Allows for selection by index
	/// </summary>
	[XmlElement("bill")]
	public Bill this[int index]  
	{
		get { return((Bill)List[index] );}
		set { List[index] = value;}
	}

	/// <summary>
	/// Adds new Bill to collection
	/// </summary>
	/// <param name="value"></param>
	/// <returns></returns>
	public int Add(Bill value)  
	{
		if (!List.Contains(value))
			return List.Add(value);
		else
			throw new ArgumentException("Item exists");
	}

	/// <summary>
	/// Returns index of passed Bill within collection
	/// </summary>
	/// <param name="value"></param>
	/// <returns></returns>
	public int IndexOf(Bill value)  
	{
		return List.IndexOf(value);
	}

	/// <summary>
	/// Inserts Bill into specific location (index) of collection
	/// </summary>
	/// <param name="index"></param>
	/// <param name="value"></param>
	public void Insert(int index, Bill value)  
	{
		List.Insert(index, value);
	}

	/// <summary>
	/// Removed passed Bill from collection
	/// </summary>
	/// <param name="value"></param>
	public void Remove(Bill value)  
	{
		if (!List.Contains(value))
			List.Remove(value);
		else
			throw new ArgumentException("No match found");
	}

	/// <summary>
	/// Simple routine to check existance of given Bill in collection
	/// </summary>
	/// <param name="value"></param>
	/// <returns></returns>
	public bool Contains(Bill value)  
	{
		return List.Contains(value);
	}
	
	/// <summary>
	/// Simple routine to search with the collection
	/// </summary>
	/// <param name="payee"></param>
	/// <param name="dueDate"></param>
	/// <param name="amountDue"></param>
	/// <returns></returns>
	public BillCollection Search(string payee, DateTime dueDate, double amountDue )
	{
		// Multiples results could be returned, therefore a 
		// collection gets returned
		BillCollection result = new BillCollection();
		Bill searchCriteria = new Bill(payee,dueDate,amountDue);

		foreach(Bill bill in this.InnerList )
		{
			if (bill.Match(searchCriteria))
				result.Add(bill);
		}

		if (result.Count > 0 )
			return result;
		else
			return null;
	}
}
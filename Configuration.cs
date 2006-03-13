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
using System.Xml.Serialization;

namespace BillReminder
{
	/// <summary>
	/// Singleton used to hold all pertinent information for the bills
	/// being used by users as well as serving as a mechanism to 
	/// make sure the records are available throughout the application.
	/// </summary>
	public class Configuration
	{
		/// <summary>
		/// Used to determine if Bill has been paid or not.
		/// </summary>
		public enum BillType 
		{
			Paid,
			Unpaid
		}

		// This is the singleton
		private static Configuration configuration;
		
		// Three individual collections used
		private static BillCollection unpaidBills;
		private static BillCollection paidBills;
		private static BillCollection searchedBills;

		// File location for serializable objects
		//
		// TODO: make the file location for serializable objects
		//       more flexible and leave it up to the end user
		//       to choose the location.
		private static string UNPAIDFILE = "./unpaid.xml";
		private static string PAIDFILE = "./paid.xml";
		

		#region "Constructors"

		/// <summary>
		/// Default constructor
		/// </summary>
		protected Configuration()
		{
			//bills = new BillContainer();
			// Initialization of collections
			unpaidBills = new BillCollection();
			paidBills = new BillCollection();

			// Deserializes any serializable object into proper
			// collection.
			LoadBills();
		}

		#endregion

		#region "Methods"

		// This is how we make sure only one single instance of this
		// class gets instantiated/created throughout the application.
		public static Configuration Instance()
		{
			// Use 'Lazy initialization'
			if (configuration == null)
			{
				configuration = new Configuration();
			}

			return configuration;
		}

		/// <summary>
		/// Loads any serializable objects found into proper collection.
		/// If none are found, create an empty one.
		/// </summary>
		private static void LoadBills()
		{
			// Check to see if serializable unpaidBills objects exist
			if (File.Exists(UNPAIDFILE)) 
				DeserializeBills(UNPAIDFILE, ref unpaidBills);
			else
				// Create empty collection
				SerializeBills(UNPAIDFILE, unpaidBills);

			// Check to see if serializable paidBills objects exist
			if (File.Exists(PAIDFILE)) 
				DeserializeBills(PAIDFILE, ref paidBills);
			else
				// Create empty collection
				SerializeBills(PAIDFILE, paidBills);	
		}

		/// <summary>
		/// Responsible for XML deserialization of collections
		/// </summary>
		/// <param name="filename"></param>
		/// <param name="billCollection"></param>
		public static void DeserializeBills(string filename, ref BillCollection billCollection) 
		{
			XmlSerializer s = new XmlSerializer( typeof( BillCollection ) );
			TextReader r = new StreamReader( filename );
			billCollection = (BillCollection)s.Deserialize( r );

			r.Close();
		}

		/// <summary>
		/// Responsible for XML serialization of collections.
		/// </summary>
		/// <param name="filename"></param>
		/// <param name="billCollection"></param>
		private static void SerializeBills(string filename, BillCollection billCollection) 
		{
			try 
			{
				XmlSerializer s = new XmlSerializer( typeof( BillCollection ) );
				TextWriter w = new StreamWriter( filename );
				s.Serialize( w, billCollection );
				w.Close();}
			catch ( Exception ex ){ Console.WriteLine(ex.ToString());}
		}

		/// <summary>
		/// Public method that allows "manual" calls to serialization
		/// method.
		/// </summary>
		/// <param name="type"></param>
		public static void Write(BillType type) 
		{
			if (type == BillType.Paid)
				SerializeBills(PAIDFILE, paidBills);
			else
				SerializeBills(UNPAIDFILE, unpaidBills);
		}

		#endregion

		#region "Properties"

		/// <summary>
		/// Direct access to unpaidBills collection.
		/// </summary>
		public BillCollection UnpaidBills 
		{
			get { return unpaidBills;}
			set { unpaidBills = value;}
		}

		/// <summary>
		/// Direct access to paidBills collection.
		/// </summary>
		public BillCollection PaidBills 
		{
			get { return paidBills;}
			set { paidBills = value;}
		}
		
		/// <summary>
		/// Direct access to searchedBills collection.
		/// </summary>
		public BillCollection SearchedBills
		{
			get {return searchedBills;}
			set { searchedBills = value;}
		}

		#endregion


	}
}

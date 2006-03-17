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
		private static BillCollection bills;

		// File location for serializable objects
		//
		// TODO: make the file location for serializable objects
		//       more flexible and leave it up to the end user
		//       to choose the location.		
		private static string homeDir = Environment.GetFolderPath(Environment.SpecialFolder.Personal);
		private static string confDir = "/.config/billreminder/";
		private static string dataFile = "bills.xml";
		private static string filePath = homeDir + confDir + dataFile;
		private static string dirPath = homeDir + confDir;
		
		#region "Constructors"

		/// <summary>
		/// Default constructor
		/// </summary>
		protected Configuration()
		{
			//bills = new BillContainer();
			// Initialization of collections
			bills = new BillCollection();

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
			// Check to see if serializable Bills objects exist
			if ((InitializeConfigurationDirectory()) && (InitializeDataFiles())) 
				DeserializeBills();
			else
				// Create empty collection
				Console.WriteLine("There were some errors and this application will shutdown!");
		}

		private static bool InitializeDataFiles() 
		{
			bool created = true;
			
			if (!(File.Exists(filePath)))
				try 
				{
				    // Create empty collection
					SerializeBills();
					}
				catch (IOException io) 
				{
					Console.WriteLine("some other problem");
					Console.WriteLine(io.ToString());
					created = false;
				}
				catch(UnauthorizedAccessException uae) 
				{
					Console.WriteLine("You don't have the permission to create directories!");
					Console.WriteLine(uae.ToString());
					created = false;
				}

			return created;
		}

		private static bool InitializeConfigurationDirectory() 
		{
			bool created = true;
			
			if (!(Directory.Exists(dirPath)))
				try 
				{
					Directory.CreateDirectory(homeDir + confDir); 
					Console.WriteLine(homeDir + confDir + " created!");
				}
				catch (IOException io) 
				{
					Console.WriteLine("some other problem");
					Console.WriteLine(io.ToString());
					created = false;
				}
				catch(UnauthorizedAccessException uae) 
				{
					Console.WriteLine("You don't have the permission to create directories!");
					Console.WriteLine(uae.ToString());
					created = false;
				}

			return created;
		}

		
		/// <summary>
		/// Responsible for XML deserialization of collections
		/// </summary>
		/// <param name="filename"></param>
		/// <param name="billCollection"></param>
		public static void DeserializeBills() 
		{
			XmlSerializer s = new XmlSerializer( typeof( BillCollection ) );
			TextReader r = new StreamReader( filePath );
			bills = (BillCollection)s.Deserialize( r );

			r.Close();
		}

		/// <summary>
		/// Responsible for XML serialization of collections.
		/// </summary>
		/// <param name="filename"></param>
		/// <param name="billCollection"></param>
		private static void SerializeBills() 
		{
			try 
			{
				XmlSerializer s = new XmlSerializer( typeof( BillCollection ) );
				TextWriter w = new StreamWriter( filePath );
				s.Serialize( w, bills );
				w.Close();}
			catch ( Exception ex ){ Console.WriteLine(ex.ToString());}
		}

		/// <summary>
		/// Public method that allows "manual" calls to serialization
		/// method.
		/// </summary>
		/// <param name="type"></param>
		public static void Write() 
		{
			SerializeBills();
		}

		#endregion

		#region "Properties"

		/// <summary>
		/// Direct access to unpaidBills collection.
		/// </summary>
		public BillCollection Bills 
		{
			get { return bills;}
			set { bills = value;}
		}

		#endregion


	}
}

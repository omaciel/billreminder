.. contents::

=====
PyCha
=====

Pycha is a very simple Python package for drawing charts using the great
`Cairo <http://www.cairographics.org/>`_ library. Its goals are:

 * Lightweight

 * Simple to use
 
 * Nice looking with default values
 
 * Customization 

It won't try to draw any possible chart on earth but draw the most common ones
nicely. There are some other options you may want to look at like
`pyCairoChart <http://bettercom.de/de/pycairochart>`_.

Pycha is based on `Plotr <http://solutoire.com/plotr/>`_ which is based on
`PlotKit <http://www.liquidx.net/plotkit/>`_. Both libraries are written in
JavaScript and are great for client web programming. I needed the same for the
server side so that's the reason I ported Plotr to Python. Now we can deliver
charts to people with JavaScript disabled or embed them in PDF reports.

Pycha is distributed under the terms of the `GNU Lesser General Public License
<http://www.gnu.org/licenses/lgpl.html>`_.

Documentation
=============

Installation
------------

Pycha needs PyCairo to works since it uses the Cairo graphics library. If you
use Linux you will probably already have it installed so you don't have to do
anything. If you use Windows these are the recommended steps for installing
PyCairo:

   1. Grab the latest PyCairo Windows installer from
      http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/ You need to use the
      one that matches your Python version so take the one ending in -py2.4.exe
      for Python 2.4 or the one ending in -py2.5.exe for Python 2.5
   2. Install it in your Python environment (just follow the installation
      program instructions)
   3. Put the Cairo dlls inside the pycairo directory inside your site-packages
      directory or anywhere in your path. You can find the dlls at
      http://www.gimp.org/%7Etml/gimp/win32/downloads.html Go there and download
      the following packages:

         1. cairo.zip. You just need the libcairo-2.dll file inside that zip
         2. libpng.zip. You just need the libpng13.dll file inside that zip
         3. zlib.zip. You just need the zlib1.dll file inside that zip 

Pycha is distributed as a Python Egg so is quite easy to install. You just need
to type the following command:

easy_install pycha

And Easy Install will go to the Cheeseshop and grab the last pycha for you. If
will also install it for you at no extra cost :-)

Tutorial
--------

Using pycha is quite simple. You always follow the same 5 simple steps:

   1. Create a Cairo surface to draw the chart on
   2. Build a list of data sets from which your chart will be created
   3. Customize the chart options.
   4. Create the chart, add the datasets and render it
   5. Save the results into a file or do whatever you want with the Cairo
      surface 

To create the Cairo surface you just need to say the type of surface and its
dimensions::

   import cairo
   width, height = (500, 400)
   surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

Then you should create your data set querying a database or any other data
source::

   dataSet = (
     ('dataSet 1', ((0, 1), (1, 3), (2, 2.5))),
     ('dataSet 2', ((0, 2), (1, 4), (2, 3))),
     ('dataSet 3', ((0, 5), (1, 1), (2, 0.5))),     
   )

As you can see, each data set is a tuple where the first element is the name of
the data set and the second is another tuple composed by points. Each point is a
two-elements tuple, the first one is the x value and the second the y value.

Not every chart uses all the information of a data set. For example, the Pie
chart only uses the first point of each dataset and it only uses the y value of
the point.

Now you may want to specify some options so the chart can be customize changing
its defaults values. To see the defaults you can check the
pycha.chart.Chart.__init__ method in the source code. You can use regular
dictionaries to define your options. For example, imagine you want to hide the
legend and use a different color for the background::

   options = {
       'legend': {'hide': True},
       'background': {'color': '#f0f0f0'},
   }

Now we are ready to instantiate the chart, add the data set and render it::

   import pycha.bar
   chart = pycha.bar.VerticalBarChart(surface, options)
   chart.addDataset(dataSet)
   chart.render()


Right now you can choose among 4 different kind of charts:

    * Pie Charts (pycha.pie.PieChart)
    * Vertical Bar Charts (pycha.bar.VerticalBarChart)
    * Horizontal Bar Charts (pycha.bar.HorizontalBarChart)
    * Line Charts (pycha.bar.LineChart)
    * Scatterplot Charts (pycha.scatter.ScatterplotChart)

Finally you can write the surface to a graphic file or anything you want using
the cairo library::

   surface.write_to_png('output.png')

That's it! You can see more examples in the examples directory of the source
code.

Documentation
-------------

Adam Przywecki has done a fantastic work writing documentation for Pycha.
Check it out at http://pycha.yourwei.com/


Development
-----------

You can get the last bleeding edge version of pycha by getting a checkout of
the subversion repository::

   svn co http://www.lorenzogil.com/svn/pycha/trunk pycha

Don't forget to check the 
`Release Notes <http://www.lorenzogil.com/projects/pycha/wiki/ReleaseNotes/>`_ 
for each version to learn the new features and incompatible changes. 

Contact
-------

There is a mailing list about PyCha at http://groups.google.com/group/pycha 
You can join it to ask questions about its use or simply to talk about its
development. Your ideas and feedback are greatly appreciated! 

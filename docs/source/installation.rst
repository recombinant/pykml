.. include:: <isonum.txt>
Installing pyKML
================

Installation
~~~~~~~~~~~~

Existing installation?
----------------------

To verify an existing installation of pyKML, open up a Python shell and type:

>>> import pykml
>>>

If you don't get back an error message, pykml has already been installed.


Installing the Dependencies
---------------------------

You will need to `install pip`_ if your Python installation does already have
it.

pyKML depends on a several Python modules.  With one exception these are pure
Python modules and install automatically without problem when
`installing the pyKML package`_ using pip.  The exception of the lxml_ Python
module which can cause problems…

.. _install pip: https://pip.pypa.io/en/latest/installing.html

Installing the lxml Dependency
------------------------------

pyKML depends on the lxml_ Python module, which in turn depends on two
C libraries: libxml2_ and libxslt_.  Given this, the first step to installing
pyKML is to get lxml running on your system.  Refer to the `lxml` website for
`instructions on how to install lxml`_.

To verify that the lxml module has been installed correctly,
open up a Python shell and type:

>>> import lxml
>>>

If you don't get back an error message, lxml has been installed and you are 
ready to proceed.

.. note::
    For Windows users the simplest method of installing lxml is to use
    the `unofficial Windows binaries`_ mentioned in
    the `lxml MS Windows install documentation`_.  Download the appropriate
    wheel file and install using **pip install -U** *appropriate_wheel.whl*.
    (wheels_ are the official preferred method for Python module distribution,
    *.exe* and *.msi* files are reconciled to history for general Python
    module distribution on Windows.)

.. _unofficial Windows binaries: http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
.. _lxml MS Windows install documentation: http://lxml.de/installation.html#source-builds-on-ms-windows
.. _lxml: http://lxml.de
.. _instructions on how to install lxml: http://lxml.de/installation.html
.. _libxml2: http://xmlsoft.org/
.. _libxslt: http://xmlsoft.org/XSLT/
.. _wheels: http://pythonwheels.com/


Installing the pyKML package
----------------------------

pyKML itself can be installed from the Python Package Index, 
using pip_.

From a console in Linux or any UNIX\ |copy|\ -like system::

    $ pip install pykml

Or similarly from a command prompt in Microsoft\ |reg| Windows\ |reg|::

    C:>pip install pykml

To verify that the pyKML module has been installed correctly,
open up a Python shell and type:

>>> import pykml
>>>

Once again, if you don't get back an error, pyKML has been installed correctly. 
To learn how to start using pyKML, head on over to the :doc:`tutorial`.

.. note::
    The `Python website`_ contains further information on `installing python modules`_

.. _pip: http://pypi.python.org/pypi/pip
.. _installing python modules: https://docs.python.org/3/installing/
.. _Python website: https://www.python.org/

Building pyKML documentation
----------------------------

The pyKML documentation is built using Sphinx_ and uses the 
`ipython_directive`_ extension provided by the ipython_ project.
Because of this, building the documentation requires that 
Sphinx_, and ipython_ be installed on your system.

.. note::
    Note that there appears to be a bug that prevents building documentation
    when using the Ubuntu 10.04's default versions of the libraries.  The
    documentation has been successfully built using the default libraries of
    Ubuntu 11.04.

.. note::
    The `ipython_directive`_ extension was originally part of the matplotlib_
    project but has since been moved to ipython_ project.

.. _Sphinx: http://sphinx.pocoo.org/
.. _ipython: http://ipython.org/
.. _ipython_directive: https://github.com/ipython/ipython/blob/master/IPython/sphinxext/ipython_directive.py
.. _matplotlib: http://matplotlib.sourceforge.net/


Installed version
~~~~~~~~~~~~~~~~~


lxml version
------------

*Assuming that lxml is installed.* To determine the lxml version, open up a
Python shell and type:

>>> from lxml import etree
>>> etree.LXML_VERSION

This will report the lxml version.


pyKML version
-------------

*Assuming that pyKML and its dependencies are installed.* To determine the
pyKML version, open up a Python shell and type:

>>> import pykml
>>> pykml.version

If you get back an error message then the version is prior to 0.2.0 otherwise
the version will be reported.

If the version is prior to 0.2.0 then after the previous step type the
following:

>>> from pykml.util import format_xml_with_cdata

If this does not report an error then the version is 0.1.1 otherwise the pyKML
version is 0.1.0 or earlier.

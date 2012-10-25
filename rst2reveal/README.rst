=========
rst2reval
=========

Introcution
===========

rst2reveal is just a thin layer on top of standard html4css writer
that produces a reveal_ presentation.


.. _reveal: http://lab.hakim.se/reveal-js/


Usage
=====

::

   python rst2reveal.py [options] input_file.rst > output_file.html


``rst2reveal`` generates ``<section>`` tags for each slide, letting
reveal_ do the real hard job.



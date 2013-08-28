interstitial
=============

Tool to detect interstitial errors in digitization workflows

Introduction
------------

interstitial is designed to detect dropped samples in audio digitization processes.  These are caused by fleeting interruptions in the hardware/software pipeline on a digital audio workstation, causing a small number of samples to be dropped from the transfer.

More information on interstitial errors can be found in [this FADGI report](http://www.digitizationguidelines.gov/audio-visual/documents/Interstitial_Error_Report_2013-04-08.pdf)

Usage
-----

This tool requires two sets of audio files: one generated as normal on a DAW, and one generated on a reference device.  Typically, a device such as a standalone recorder is used as the reference device.  This device should receive the same digital output that the DAW receives and record it to disk.

Once the two sets are generated, interstitial-errors can be pointed at the reference and DAW directories and run.  It will automatically match WAV files between the directories, find errors in the DAW-generated files, and report results.

Sample audio files can be found here:

[DAW](http://www.avpreserve.com/interstitialerrorsamples/201206081082_DAW.wav)

[Ref](http://www.avpreserve.com/interstitialerrorsamples/201206081082_DDR.wav)

Note that, due to the nature of the tests performed by the tool, it may also highlight other issues in a digitization chain (e.g. timing problems).

Requires
--------

* audiolab
* numpy
* PySide

Precompiled Binaries
--------------------

* [Windows](http://www.avpreserve.com/wp-content/uploads/2013/07/interstitial-win.zip)
* [OSX](http://www.avpreserve.com/wp-content/uploads/2013/07/interstitial-osx.zip)

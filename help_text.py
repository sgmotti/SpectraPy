helpstr ="""Funtionalities included so far:

Load spectrum files
	From SpectraSuite or any other .txt file.
	Takes wl from first column and spectrum from the 2nd column.

Overlay a reference with the live data:
	Snapshot taken in live mode or a spectrum loaded from file.
	(currently only one overlay plot is available)

Free run:
	Live spectra from OceanOptics spectrometers (tested with 3 different models: Maya, Usb2000 and IRQuest).
	Allows averaging of spectra in live mode.

Time plot:
	You'll be asked for a basename and spectra will be saved as basename_N.txt (where N is the sequence number).
	Will save every spectrum with the same interval as they show on screen, depending on integration time and averages.
	When finished, it will create a basename_timeplot.txt file with the integrated signal (in the WL range defined) over time.



    """

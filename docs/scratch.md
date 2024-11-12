We believe in late binding, meaning TDAP will faithfully represent the data as it was collected and stored in EMR.


 > Patient A is on a nasal cannual and decompensates and get placed on mechanical ventilation.  1 day later the patient is weened off the vent and placed back on the nasal cannula.  Capturing these shifts is several flowsheet items (only 2 mentioned for this simple example):  O2 devive and Vent Mode.  Vent mode is only ever populated when the patient is on a vent.  This means is the data is simply fed forward the last known vent mode will still be in the matrix even AFTER the patient got better and returned to the nasal cannula.  This is a reality violation.  Cleanups are intended to help correct this type of wrongdoing.

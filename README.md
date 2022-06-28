# yachts_dataset

**Scrapes Used Sailboat Listings From https://www.sailboatlistings.com**

Dataset should appear after running `dvc repro`
requires 'dvc' CLI https://dvc.org/doc/install


Features include.

    * Length
    * Beam
    * Draft
    * Year Manufactured
    * Hull Type
    * Material Type
    * No. Engines
    * Date Posted
    * Adjusted Asking Price

The adjusted asking price uses the cpi library to reflect the asking price
in current day dollars. The earliest listings observed are from 2010.

Once the data is scraped and saved it undergoes a cleaning and processing step.

The cleaning.py file attempts to standardize numerical features to '00.0f' format.
It also encodes categorical features into binary or ordinal columns.
Lastly, it drops records for which there are null values for any of the features.

The remove_outliers.py script determines, for each continuous variable, the
interquartile range and removes records outside of the range multiplied by a
factor of 1.5.

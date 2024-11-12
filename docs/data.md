# TAPESTRY Data

TAPESTRY is fundamentally a data management platform.  As described on the [home page](index.md), core to TAPESTRY is a simple universal clinical data key:

patient :: time :: clinical data

It is important to think of clinical data as concepts, a few reasons why:

- The same clinical data collected in the same way over time will frequently get re-coded either due to versioning data coding standards OR from changing proprietary code sets within modern EMR's
- Data collected through different pathways may, in fact, be semantically synonymous and a mechanism to interleave them is advantageous

Working on a specific TAPESTRY instance means choosing a set of clinical concepts that are meaningful to the disease process you wish to study and using the TAPESTRY toolkit to bring them together.  The complete toolkit helps you manage clinical concepts from ingestion to use in 4 steps:

1. Concept Ingestion from known clinical databases - see [data sources below](#data-sources)
1. Concept Ingestion from unknown data sources - see [extensions below](#extensions)
1. Data Cleanup - the process of cleaning and normalizing data for the intended use-case - see [cleanups below](#cleanups)
1. Data Derivation - the process of combining data into new information - see [derivation below](#derivations)


In sum, the key to successfully using TAPESTRY comes down to defining a population of patients you wish to model a set of clinical concepts for.  The toolkit approach used in TAPESTRY provides a lot of boilerplate, paramaterized code, as well as three interfaces that allow you to configure it and/or bring your own code to meet the specific goals of your project.  The rest of this document describes the motivations to break this into this 4 step process to complete a TAPESTRY project.  The sibling document about [running TAPESTRY](run.md) will describe the technical details about how to do this.

The easy way to think about how TAPESTRY operates:

For each patient in your desired population, The config file guides TAPESTRY tools through the steps of data ingestion (core or extension interface), cleanups, derivations.  We implement peformance optimizations in the form of [parallelism](run.md#script-performance-and-parallelization) to keep things fast, but this is the core logical framing.

For each patient, we build a simple 2 dimensional data representation which we call the matrix.  This is best described by example.  Please see the following visual overview of how the patient :: time :: clinical data concept paradigm operates as TAPESTRY executes.

![](img/tapestry_overview.png)

#### TAPESTRY matrix

The matrix itself is simple.  It has a 2 column primary key of a patient identifier and a timestamp.  Then we start appending clinical concepts, which will be represented by a set of columns that, collectively, fully describe a concept within the TAPESTRY framework.  Given the simplicity of this data model, we rely heavily on naming conventions to provide some organization.  All columns specific to a concept will share the same prefix.  So in the case of a matrix that contains a single concept of blood pressure, it would contain at a minimum something like this:

|patient_id|timestamp          |bp_value|bp_transaction_id|bp_raw_timestamp   |
|----------|-------------------|--------|-----------------|-------------------|
|123456    |2024-01-01 16:00:00| 120/80 |3477654321       |2024-01-01 16:00:42|

To consider additional data in the matrix, simply add an additional set of columns for the next concept.

---
## Data sources

TDAP has paramaterized adapters for the following known clinical transactional databases or clinical data sources.  To get specific, an adapter is pre-written code that will obtain data directly from that source on your behalf, saving you time writing code.  Using OMOP as an example, for each data domain in OMOP, TAPESTRY has a pre-written SQL query with placeholders.  These placeholders are replaced with values from the configuration file which you fill out to obtain for your project.

1. <span style='color:green'>OMOP</span>
1. <span style='color:green'>Epic Clarity</span>
1. <span style='color:red'>Epic Caboodle*</span>
1. <span style='color:red'>HL7 FHIR Resources*</span>

<span style='color:green'>Green indicates the adaptor is available</sapn>

<span style='color:red'>Red indicates the adaptor is in development</span>

None of these data adapters has complete coverage of the entirety of these sources.  Instead, they cover the data that is most frequently used in temporal data resoning studies.  Keep in mind that you can always employ the Extensions interface to add additional data from these sources.

### OMOP Data Adapter

The OMOP adapter includes the following domains, which follow logically with the dimensional modeling of the OMOP CDM.  Please see the [OHDSI foundations CDM documentation](https://ohdsi.github.io/CommonDataModel/) for more information about each one:

1. measurement
1. condition_occurrence
1. drug_exposure
1. procedure_occurrence
1. observation
1. device_exposure

### Epic Clarity Data Adapter

> NOTE:  We do not release this adapter as fully open source due to Epic's IP constraints.  However, we are willing to share this adapter with sites that have an Epic EMR.

The Epic Clarity data apater includes the following data domains.  It is worth noting that these domains are conceptual in Epic Clarity since this database is not dimensionally modeled.

1. flowsheet - obtains flowsheet values, typically numeric
1. mar - obtains information about medication administrations - typically inpatient
1. labrslt - obtains information about lab results - typically numeric; some string data
1. ordproc - obtains fact of occurrence information about ordered procedures
1. adt - obtains census information about transfers and locations in inpatient settings
1. enc_dx - obtains encounter diagnosis information
1. ord_med - obtains information about ordered medications

---
## TAPESTRY Concepts

The 'clinical concept' is key to understanding how TAPESTRY works.  Here, we describe exactly what defines a concept to the TAPESTRY toolkit. Concept defintions are just one component of a TAPESTRY configuration file - [see tapestry configuration](run.md#managing-the-tapestry-config-file).


Here is the schema for a single TAPESTRY concept - thie example demonstrates what it requires to instruct TAPESTRY how to extract blood pressure from the flowsheets in an Epic Clarity database:

```json
"bp": {
        "conceptproperties": {
            "originid": "'5'",
            "origindatatype": "string",
            "origintype": "flowsheet",
            "desttable": "pytdap_matrix",
            "fillmethod": "forwardfill",
            "fillwithnormalmode" : "n",
            "filltimetonormal" : "0",
            "fillnormalvalue" : "unk",
            "cleanvals":"n",
            "minval":0,
            "maxval":0
        }
```

Concept Property definitions:
* origintype - Tells us what type of data this concept represents.  For each data type, there is a templated SQL query to extract this data type within TAPESTRY.
* originid - uniquely identifies this type of data from other data.  Specifically this list of values is injected into the SQL query to extract the data
* origindatatype - Tells tdap how to process the data, numerically or as text - This directly impacts the type of [aggregations applied during down sampling](#data-types-and-associated-aggregations-during-down-sampling).
* desttable - After tdap processes these data, they will be saved in a database table with this name
* fillmethod - tells tdap how to extrapolate the data forward in time.  Currenlty only the last known value approach is supported but interpolation is on the way
* fillwithnormalmode - 'y' or 'n' - If yes, we only fill data for a specified number of data periods (aka rows in the matrix), specified by the next few properties
* filltimetonormal - The number of time periods to propagate the value
* fillnormalvalue - The 'normal' value to populate in this column after the specified number of time periods
* cleanvals - 'y' or 'n' - If yes, alter values less than minval to the minval value in this config and alter values greater than maxval to the maxval value in this config


### Data types and associated aggregations during down sampling

TAPESTRY treats the down sampling of data differently for string and numeric data.  During downsampling we are reducing the sampling frequency and therefore must aggregate, with the goal to reduce data loss to the extent possible.  Therefore, TAPESTRY performs the following aggregations based on whether or not the data is string or numeric:

**String Data Aggregations**

  - First
  - Last
  - Most frequent
  - List

**Numeric Data Aggregations**

  - First
  - Last
  - Min
  - Max
  - Mean
  - Mode - NOTE if multimodal, only one mode is stored
  - Standard Deviation


---

## Extensions, Cleanups, and Derivations

These modular paradigms were included to make TAPESTRY extensible and configurable.  You, the user, are empowered to write one or more of these modules and the TDAP framework will take care of the execution as long as you respect the interface, defined [here](run.md#adding-your-own-extensionscleanupsderivations)


### Extensions

Extensions are the paradigm by which any 3rd party data can be integrated into the matrix.  In this paradigm, TAPESTRY is little more than a set of functions that simplify the process of adding data to the matrix, but it is YOUR resposibility to write the code that connects to the data repository and extracts the data.  Extensions were born out of the necessity to combine data from non-standard or non-ubiquitous clinical data repositores.

### Cleanups and Derivations

Cleanups and Derivations are just fancy names for python code that should be executed AFTER the matrix is created but begore the matrix is returned to the user.  There is a distinction between cleanups and derivations:

1. Cleanups should primarily focus on data cleaning and normalization
2. Derivations should be focused on deriving new information by combining multiple concepts together


### Cleanups

A good example of a cleanup is unit normalization.  This is frequently required for research since differences in local system configuration result in a variety of stored units, and this can change over time. There are also changing requirements in research data for different use-cases.  Lets take the example of converting 

 mcg/min to mcg/kg/min  

In this case you would need to divide the mcg/min value by the appropriate KG measurement (last known, nearest, etc...) to obtain mcg/kg/min.  In this instance the temporal nature of TAPESTRY will simplify the conversion but, it is important you have control over this conversion to ensure the semantics are correct for your use-case.


### Derivations

A good example of a derivation is computing a digital phenotype.  Lets use the Seqentional Organ Failure Assessment score as an example, which will highlight both the idea of derivations as well as a key TAPESTRY advantage.  SOFA is made up 6 system specific subscores:

- Respiratory
- Coagulation
- Liver
- Cardiovascular
- Central Nervous System
- Renal

Lets focus on a single subscore to keep things simple - the respiratory score.  This score is calculated as the P to F ratio, which is PaO2 or partial pressure of oxygen dissovled in the blood normalized over the FiO2 or the Fractional inspired oxygen concentraion.  This means we are integrating two variables, measured independetly of one another into a new value with unique clinical meaning.  This is the essence of what a derivation is all about but, this example seems too simple.  It is.  While PaO2 is a value measured directly by a lab, FiO2 is not so simple a thing.  To obtain an FiO2, we must integrate information about Oxygen delivery device, if applicable, otherwise we assume 0.21 for room air.  If there is an oxygen device in use, then we must ascertain how invasive of a device and how each one uniquely alters the FiO2 value.  I will not inlude all of the details here but, this can easily involve upwards of 10 variables and the mix of these variables will change over time.
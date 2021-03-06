##Connector Overview

The Socrata Connectors produce a Socrata dataset with a row for each feature. New tables can be created for each specified feature type or, alternatively, rows can be written to existing datasets that match the feature type names. The feature type may also be treated as a dataset ID, if it matches Socrata�s alphanumeric 4-4 ID pattern. The Socrata Writer enforces uniqueness for dataset names owned by the user. 

Note that when a dataset has been newly created, it may not be immediately reflected in the Socrata web interface, and the Socrata Writer may not detect the new dataset if the same translation is run shortly afterwards. To prevent the creation of duplicate datasets, or if running a data sync job allow a few minutes for the original dataset to appear in the Socrata web interface before re-running.


Only 2D point geometry is supported by the Socrata Writer. The point coordinates are stored in �Location� column type on the Socrata dataset. When you Visualize or map the dataset you will this new "Location" column. 

Note: __The Socrata Writer will coerce geometries to a point whenever possible.__ Each location column supports only a single point. Multiple geometry columns may be specified, in which case the Socrata Writer will expect the input to be named geometry or named multiple geometry with names that map to the geometry column names.

Features are written to a temporary CSV file, which is then uploaded and converted to a Socrata dataset using Socrata�s Import API. If the FME_DEBUG environment variable is set, the CSV file generated by the Socrata Writer will not be deleted from the system�s temporary directory.

The Socrata Writer only supports operations available in the Socrata Import API, and does not support row-level operations. The Import API supports creating, appending, and replacing datasets. For append operations, the user is responsible for defining user attributes that match the destination dataset.

A user login, password, and app token are required in order to access the SODA API. An app token can be generated by logging into your Socrata account and creating a new application under the App Tokens page.

The Socrata Writer will only access Socrata using HTTPS and basic authentication. If you are connecting via a proxy server, ensure that it supports HTTPS.


###Syncronizing Data
Syncronizing data with FME is simple. In the writer under Format Parameters set the Write Mode to Upsert. This will invoke the the Socrata Syncronizer installed with FME and update changes.


###Publishing A Dataset
It is possible to write data into Socrata as a working copy but also as a public, published dataset. In the writer under Format Parameters just set the Publish or Public properties to Yes/No depending on the requirents.


###Assumptions
These connectors assume FME 2014 SP4 or higher. If you are running a different version you can download the latest here: http://www.safe.com/support/support-resources/fme-downloads/

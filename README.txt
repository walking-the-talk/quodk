This plugin works alongside an ODK Central Server (not Kobo / Ona etc). It allows you to load geo-located data gathered in ODK Collect forms as QGIS temporary layers, as well as download associated attachments. It is designed to allow you to incrementally download submissions (by selecting a date range of when data was sent from ODK Collect to the server. You can, with caution, opt to load all records - bear in mind this could take some time for large datasets with lots of attachments.

Prerequisites / dependencies

QuODK requires PANDAS package to be installed in order to function: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html
You could use "pip install pandas" 
WINDOWS: open OSGEO4W command line to ensure it is installed in the correct version
LINUX / MACOS: you may need to set up a virtual environment to install the pandas package - and avoid conflict

Set up

Ask the person responsible for managing your ODK Central server to provide you with log-in details (hint: it may be useful to set up a separate web-user on Central with restricted access - e.g. Project Viewer). You can choose to save the password (stored in plain-text on your computer in the plug-in folder).

Loading data

Once you connect to your server you will get a list of ODK projects if appropriate, and then you can select the form you would like to download. If your form has repeat groups with location data you can select the repeat as well as the main form. You can load any form or repeat as a simple table if there is no location data (in case you want to link data in QGIS).

You can select a different Projection for the layer to fit with your project / location (e.g. OSGB grid). You can also download data as CSV.

NOTE: By default QuODK only loads features with spatial data (point / line / polygon) so that they can be displayed in QGIS, but if you have some records that have no location data you can choose to include them and manual add relevant spatial data [once the layer is loaded, select the feature in the attribute table and then choose Add part in QGIS digitising toolbar] 

Attachments
After you have selected the data you can download related attachments to a folder on your computer. This plugin also creates a project variable called @ODK_image_path so that you can view the attachments in the attribute form by setting the default path to this variable. Be aware that the plugin might freeze for a while when it loads the attachments form if you have lots of submissions. If you choose to download all the attachments listed it can take a while, needing high bandwidth - use with caution. 

Entities
As of version 1.2 QuODK supports downloading entity lists from Central and indirectly managing Entity lists. Upload of new entities or modification of existing entities requires additional privileges in Central and could potentially affect data collection. For this reason (and because it is hard to anticipate every scenario for adapting entity lists), you can convert a QGIS vector layer to CSV but cannot update Central directly from QuODK.

You can export QGIS layers (point, line or polygon, or even those without geometry) to the CSV format required by Central - it will include a UUID field or you can choose an existing UUID. QuODK will generate the basis for a pyODK script for you to copy and paste (e.g. into Jupyter Lab).


Credits

This plugin was inspired by FooODK which written in Swahili for WWF Tanzania by Cuthbert-Langen Mushi. Code refactoring, additional features and translations were implemented by Chris York at Walking-the-Talk. The plugin uses the ODK Central API to access the server and more functionality is planned (e.g. working with entities, and potentially deleting submissions)...

Find out more about ODK

ODK is an ecosystem of open source mobile data collection supported by a core development team and an active community.
ODK website: https://getodk.org

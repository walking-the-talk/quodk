![QuODK](/quodk.png)

This plugin for QGIS works alongside an ODK Central Server (**not Kobo / Ona etc**). It allows you to load geo-located data gathered in ODK Collect / Webforms or Enketo forms as QGIS temporary layers, as well as downloading associated attachments. It is designed to allow you to incrementally download submissions (by selecting a date range of when data was sent from ODK Collect to the server. You can, with caution, opt to load all records - bear in mind this could take some time for large datasets with lots of attachments.

![QuODK main screen](help/screenshot1.png)

# Contents
**[Getting Started](#getting-started)**

+[Prerequisites](#prerequisites)
+[Set Up](set-up)

**[Using QuODK](#using-quodk)**

+[Downloading submissions](#downloading-submissions)
+[Media attachments](#media-attachments)
+[Downloading Enitities](#downloading-entities)

**[Entity Management](#entity-management)**

**[Credits](#credits)**

**[More about ODK](#find-out-more-about-odk)**


# Getting Started

## Prerequisites / dependencies

QuODK requires PANDAS package to be installed in order to function:

 https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html



**WINDOWS**: open OSGEO4W command line to ensure it is installed in the correct version / location. You could use: 
>pip install pandas

**LINUX / MACOS**: you may need to set up a virtual environment to install the pandas package - and avoid conflict. The following can be used in Linux:
>sudo apt install python3-pandas

## Set up

Ask the person responsible for managing your ODK Central server to provide you with log-in details.

**Hint**: it may be useful to set up a separate web-user on Central with restricted access - e.g. Project Viewer. You can choose whether or not to save the ODK Central password. **NOTE**: the set up data is stored in plain-text on your computer in the QGIS plug-in folder.

# Using QuODK
Within this plugin there is an underlying assumption that you are vaguely familiar with ODK Collect / Webforms / Enketo and the outputs from ODK Central (QuODK works with the API and oData outputs) - please see the documentation if you are in doubt https://docs.getodk.org - please make sure you understand the concept of forms, repeat groups, submissions, media attachments and entities before setting sail with QuODK.

The plugin is built around drop-down combo-boxes, check-boxes and push-buttons to reduce the amount of 'prior knowledge' required about the data. This necessarily means that all entities, forms and submissions available to the Central User will be listed when you connect to your Server. Discuss any data protection or privacy issues with your Data Manager (it's beyond scope of QuODK to manage privileges and data privacy!). Where possible there is a 'logic' to which options can be selected as you progress through the plugin... So, for example you can't activate the 'Load to canvas' if you haven't selected which geometry column to use - where your data only has one available option, QuODK will use this as the default value to reduce the frustration of clickerty-boo... Sometimes if you have done too much *Blakery* (ref: clicking every permutation of option and button) you may get unexpected behaviour - please report an issue and restart QuODK - then try working from top to bottom on the user interface!

## Downloading submissions

Once you connect to your server you will get a list of ODK projects that you are authorised to view and then you can select the form you would like to download submissions. If your form has repeat groups with location data you can select the repeat as well as the main form - each Repeat Group will be a separate layer in QGIS and QuODK retains the relationships between the main form and repeat using the KEY and PARENT_KEY fields. You can load any form or repeat as a simple table if there is no location data (in case you want to link data in QGIS).

![screen-shot of Form selection](help/screenshot2.png, "Select a form from a project")

Use the date filters to restrict the scope of the download from the server (particularly useful if you have a slow connection or large dataset). You can optionally ignore dates - but be aware that this downloads ALL submissions for the given form or repeat. **NOTE** ODK Central stores submissions in UTC time (equivalent to GMT). QuODK has a simple internationalisation feature to account for your time zone if required - due to Python / Windows inconsistencies, the method used might fail around the time of clocks changing - please be aware of this if you are trying to download submissions on a daily basis around this time of year. In all other situations it would probably be cumbersome to include an hourly option for the date filter. 

![screen-shot of date filters](help/screenshot3.png, "Use date filters to access a sub-set of submissions") ![screen-shot of all submissions](screenshot4.png, "Check ignore dates to load all submissions")

You can further filter your data according to one of the attributes within the form to include or exclude one value - e.g. if you have a question for Surveyor Name, you can filter on this to download a single surveyor's data.

![screen-shot of attribute filters](help/screenshot4.png, "Use attribute filters to refine the list of submissions")

By default, data is loaded as lat/long (EPSG:4326 Projection) but you can select a different Projection for the layer to fit with your location (e.g. OSGB grid). You can also download data as CSV. All geometry data are saved in XYZM format with the M variable denoting the accuracy of each point or vertex.

![screen-shot of temporary layer](help/screenshot5.png, "submissions / repeats are loaded as temporary vector layers")

**NOTE**: By default, QuODK only includes features with spatial data (point / line / polygon) so that they can be displayed in QGIS, but if you have some records that are missing or have no location data you can choose to include them (check box) and manually add relevant spatial data. 

*HINT: for features that have no geometry, once the layer is loaded, select the feature in the attribute table and then choose "Add part" in QGIS digitising toolbar - you can then digitise the geometry and save the record* 

## Media Attachments
After you have selected the data you can download related media attachments to a folder on your computer. This plugin also creates a project variable called **@ODK_image_path** so that you can view image attachments in the attribute form by setting the default path to this variable. Be aware that the plugin might freeze for a while when it downloads the attachments if you have chosen lots of submissions - and also that it could take considerable bandwidth / consume data.  

**Note**: if you use the same QGIS project to download attachments from multiple forms to different folders on your computer you may need to manually adapt the project variables to include different locations.

## Downloading Entities
If the selected project includes any Entity Lists you have the option to download New or Updated entities (within your date range or all).

![screen-shot of entities](help/screenshot6.png, "Download of new or updated entities")

# Entity Management
If you need to generate an Entity List from a QGIS layer, or edit existing Entities in QGIS (e.g. adjust the geometry or other attributes), QuODK can be used to prepare a CSV file that can be uploaded to ODK Central Server. This is a relatively complex concept and you are well advised to become familiar with Entities before using QuODK for this purpose - for example: https://docs.getodk.org/entities-quick-reference/

![screen-shot of creating entity list](help/screenshot7.png, "Preparing an Entity List with QuODK")

You can export QGIS layers (point, line or polygon, or even those without geometry) with any attributes within that layer. **NOTE**: make sure your geometry is 'single part' - each entity needs to have its own geometry and multipart geometries cannot be handled.


QuODK will generate a UUID field or you can choose an existing UUID (useful if you want to update existing entities or keep a clear link between QGIS data and Entity lists or if you are updating entities). This also means you could include additional fields that control the format of the entity on the map widgets (e.g. colour, marker or line width)

![screen-shot of entity list preview](help/screenshot10.png, "Preview Entity List")

However, upload of new entities or modification of existing entities requires additional privileges in Central and could potentially affect data collection / data integrity. For this reason (and because it is hard to anticipate every scenario for adapting entity lists), you cannot update Entities directly from QuODK. There is an intermediary step that needs to be done with pyODK (please see https://getodk.github.io/pyodk) - so you need to know how to drive pyODK!

![screen-shot of pyODK recipe](help/screenshot11.png, "a simple pyODK recipe")

 QuODK will also generate the basis of a pyODK script for you to copy and paste (e.g. into Jupyter Lab). You can adapt it to create, update, merge or delete entities. The CSV file includes the **\__id** column to identify the UUID on ODK Central


# Credits

This plugin was inspired by FooODK which written in Swahili for WWF Tanzania by Cuthbert-Langen Mushi. Code refactoring, additional features and translations were implemented by Chris York at Walking-the-Talk. The plugin uses the ODK Central API to access the server and more functionality is planned ...

# Find out more about ODK

ODK is an ecosystem of open source mobile data collection supported by a core development team and an active community.
ODK website: https://getodk.org

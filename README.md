# Quick start
This plugin works alongside an ODK Central Server (not Kobo / Ona etc). It allows you to load geo-located data gathered in ODK Collect forms as QGIS temporary layers, as well as download associated attachments. It is designed to allow you to incrementally download submissions (by selecting a date range of when data was sent from ODK Collect to the server. You can use an automated method or download each set of repeats manually

## Auto Pilot
This is a simple form to allow you to download the records within a given form and associated Entity List (if relevant) as well as the attachments. You can choose a date range and filter the submissions (but all Entities created and update in that date range are included). The Auto Pilot works from an encrypted configuration file (username and password are kept encrypted with a Fernet key stored on the local machine) - this file provides QuODK with the Project, Form, Repeats and Entities, with the associated geometry type(s).

## Manual download
You can select a form or Entity List and download submissions / entities within a given date range, and filter. Each repeat group is downloaded as a separate layer (or non-spatial table if there is no geometry field).

Once you connect to your server you will get a list of ODK projects, if appropriate to your permissions, and then you can select the form you would like to download. If your form has repeat groups with location data you can select the repeat as well as the main form. You can load any form or repeat as a simple table if there is no location data (in case you want to link data in QGIS).

You can select a different Projection for each layer to fit with your project / location (e.g. OSGB grid). You can also download data as CSV (which is loaded as a delimited text file in WGS84 projection in QGIS).

*NOTE*: By default QuODK only loads features with spatial data (point / line / polygon) so that they can be displayed in QGIS, but if you have some records that have no location data you can choose to include them and manual add relevant spatial data. [Once the layer is loaded, select the feature in the attribute table and then choose Add part in QGIS digitising toolbar] 

### For Entities and forms that use 'geometry' field
A special function is needed because ODK Collect and ODK Central are 'agnostic' to geometry type when plotting spatial data (an entity list could have a combination of any geometry type) - QGIS uses a separate layer for each geometry type so you could find multiple layers loaded (each is named with the type!). If you use a field called 'geometry' to combine different questions from Collect, QuODK will detect and separate the geometry types. [You might use this so that ODK Central can plot the geometry in it's map preview]


### Attachments
After you have selected the data (in Manual or Auto-pilot mode) you can download related attachments to a folder on your computer. QuODK creates a project variable called @ODK_image_path so that you can view the attachments in the attribute form by setting the default path to this variable. Be aware that the plugin might freeze for a while when it loads the attachments form if you have lots of submissions. If you choose to download all the attachments listed it can take a while, needing high bandwidth - use with caution.

# Set up

Ask the person responsible for managing your ODK Central server to provide you with an Auto-pilot file (and the QuODKey to unlock it) for each form's submissions you need to download. 

Alternatively, if you are dealing with multiple forms, you can get log-in details (hint: it may be useful to set up a separate web-user on Central with restricted access - e.g. Project Viewer). These details are stored in QGIS settings and you can choose to use the QGIS Authentication system for storing the username and password.

# Advanced operations

## Create and Share Auto-pilot
You can create Auto Pilot files - either your own use or, with caveats, for sharing. Select the Form and geometry for each repeat, and whether to include Entities. You can create a filter to restrict the submissions available (e.g. __system.submitterName corresponds to the App user) or Entities (separate filter to account for the different structure).
*Data Protection Note*: It is not currently possible to filter data via the API (i.e. at source), so the unfiltered values are retrieved and filtered by QuODK. Although the full data is not available to the QGIS user, it may be technically possible to intercept the full dataset, so this function needs to be used with awareness of potential data protection issues (e.g. sharing submissions that contain sensitive data).

If you want to share the Auto Pilot file you need to generate a QuODKey so that the other user(s) can unlock the file (and it will be re-encrypted on their PC) - take care when sharing these elements, as it is not possible to prevent the password being exposed to a serious hacker if both the QuODKey and locked Auto-pilot file are stored in the same place or transmitted insecurely. However, once locally unlocked the QuODKey is redundant and the Auto-pilot file cannot be used on another PC.

## Manage Entities
You can create new Entity Lists from QGIS layers, update existing lists and combine geometry types. You can also delete one or more Entities. Select a QGIS layer with single-part geometry for this to work (ODK Collect does not handle Multi-part geometry). Select the field to be used for the entity label (does not need to be unique) and an entity id (you can create one in QGIS or leave blank and one will be added to the output).  You can also select which fields to include in the entity properties. QuODK will save the layer as a CSV for upload to ODK Central (new entity lists) or via the API (for all other operations). You can choose the type of Entity List operation and QuODK will adapt the script accordingly...

You will need to install pyODK to access the API - doing this directly with QuODK could lead to loss of data, so the QuODK simply provides you with a script to use with pyODK - the Central User needs the appropriate permissions.

# Credits

This plugin was inspired by FooODK written in Swahili for WWF Tanzania by Cuthbert-Langen Mushi. Code refactoring, additional features and translations were implemented by Chris York at Walking-the-Talk. Version 2 employed AI to help with refactoring code and implementing the QGIS Authentication. The plugin uses the ODK Central API to access the server.

## Find out more about ODK

ODK is an ecosystem of open source mobile data collection supported by a core development team and an active community.
ODK website: https://getodk.org


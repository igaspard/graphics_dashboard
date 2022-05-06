# Graphics Dashboards
## This repos demostrate how to use Plotly to read the report from 3DMark and build a Dashboard Web app.
### Most of the part is reference from the this [tutorial](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cvscode-deploy%2Cterminal-bash%2Cdeploy-instructions-azportal%2Cdeploy-instructions-zip-azcli) from Microsoft Docs. Plus the Plotly [Dash DataTable](https://dash.plotly.com/datatable).

### Before deploy this app to Azure, we already prepare a fake random genrize dataset on the Azure Blob storage. And I already mount it into my Azure Web App's docker located in /data. That can help me easily access the data just like in the locate drive.

### Here are simple steps the `app.py` do.
1. list all the sub folder in the root directory
2. create the file list contain the test items we expect & create dataframe
3. append data into each dataframes from the rest of subfolders
4. append the create time of each folder into the dataframe
5. Shorten the cloumns by removing the test name
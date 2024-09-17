# Filebeat

When you add filebeat to a project,
You must give the following variables in the `.env` file:

``` ini
ELASTICSEARCH_HOST=your-elastic-host
ELASTICSEARCH_USERNAME=your-elastic-username
ELASTICSEARCH_PASSWORD=your-elastic-password
ELASTICSEARCH_INDEX=your-index-name
LOG_FILE_PATH=path-to-log-file
```

The path to the log file should look like this:
"C:/Users/Drones/Desktop/app.log"

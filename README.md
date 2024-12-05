# Drone Routing Project

Welcome to the project! Follow these steps to set up and run the project in your local environment.

## Set up the environment

1. Locate the `.env.sample` file in the project directory.

2. Create a new file named `.env` in the same directory.
3. Copy the contents of `.env.sample` to the newly created `.env` file.

4. Fill in the required values ​​in the `.env` file based on your environment.

5. Be sure to fill in the values ​​as appropriate for how you are running the project.

## Run options

## Option 1: Run the project for development

To start the project in development mode, use the following command:

```bash
docker compose up
```

This command will start all the required services as defined in the `docker-compose.yml` file.

## Option 2: Build the Docker Image for use

To build the Docker container, use the following command, replacing `container_name` with the desired name for the container:

```Bash
docker build -t image_name .

docker run --name container_name -it -p 8000:8000 -v /path/to/your/app:/app -v /path/to/your/map.tif:/app/map.tif  image_name
```

This command will build the Docker image based on the `Dockerfile` in the project directory.

Running the project this way will only be possible with Redis and S3 deployed and connected to their endpoints

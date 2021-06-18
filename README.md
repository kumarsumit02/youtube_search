## Youtube Video Search

This project helps to get the details of most recently published youtube videos for a given tag/search query. Also, matching title and description can be found by using the search functionality.


## Technology used

* Django (with Django Rest Framework)
* Celery (with Redis)
* Postgres


## Setup Details

After installing docker, the one & only command you need to start the project is:

     $ docker-compose up -d

The build process might take couple of minutes and after that data should automatically start showing up on the dashboard - `http://localhost`

<img width="1680" alt="dashboard" src="https://user-images.githubusercontent.com/47178820/122505058-33fe5d80-d019-11eb-8b3f-ef3fa93d3eff.png">


## API Details

* Videos Listing APIs

      1. Get all videos - `http://localhost/api/v1/videos`
            - returns the stored video data in a paginated response sorted in descending order of published time.

      2. Search videos - `http://localhost/api/v1/videos/?search=bitcoin`
            - returns the video data for which the title or description contains the searched data
      
      3. Change the order - `http://localhost/api/v1/videos/?ordering=-published_at`
            - results ordering can be set using parameter `published_at` or `-published_at`

* API Key Details

      1. Get all API Keys - `http://localhost/api/v1/api_key`
            - returns all the stored API keys (not secure, just implemented to test functionality)
      
      2. Post API Key - `http://localhost/api/v1/api_key`
            - Post request can be made with body `{"key": your_api_key}`



## A Few Project Details

      1. The default API key to be used is stored in the variable `DEFAULT_API_KEY` path - server/youtube_project/config.py
      The default API key is used until a new key is stored in the table - `ApiKey`

      2. To minimize the rate limit issue, each time the API call is made using Least Recently Used API Key.

      3. The background task picks up the latest published time for the `Videos` table and use it to fetch youtube videos details for which the published time is greater than the stored video's latest time. This helps in 3 ways:
            - Less data is fetched from Youtube API on every call
            - Ensures no duplicate rows in the table
            - If the background job fails for sometime, the data is restored whenever the job starts again.

      4. The configurations like background job time interval, pagination row size, youtube search word, etc. are stored in a single place - server/youtube_project/config.py
      A new Build may be necessary after changing the configurations


## To check logs - 

      Django Server : docker-compose logs -f app
      Celery Tasks  :  docker-compose logs -f celery


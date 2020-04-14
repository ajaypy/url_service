Service Definition:

URL lookup service is a web appliation that maintains a database which tells if a particular URL has malware or not.

Service Design Goals/TBDs:
1. Quick response time
2. Manage a large database that will grow with time
3. Deployment Options
4. Security
5. HA/Resiliency ? (TBD depends on deployment options)
6. Scalability ? (TBD depends on deployment options)
7. URL purge ?
8. When the service comes up, how does it ask for the current URL database?
   Is there a URL database sync protocol between the URL service and the service sending the updates?

Assumptions:
1. The URL updates are a push from another service
2. The Service assumes any URL not in its database is not a malware
3. The PROXY server is known and currently only one server will make queries


1.   Possible reasons for delay in handling the GET requests:
     HTTP processing time: 
          Too many requests are coming in too fast consuming all resources
     Database access time: 
          lookup takes long time as database grows
          the database is busy in an update and query waits, (the query should reply with the updated information)
     

Design Options:
1. Language: Python
2. Web framework : TBD 
3. In Memory  Data structures:
   As URLs are unique, and currently our service will reply (Bad) if the  URL is found or Good if not,
   the suitable data structure for in memory storage will be any constant access  data structure.
   Python provides multiple such structures and I will use set()
   As currently not storing any values for each URL, so using another constant access data structure like python 
   dictionary will consume  extra  space (one byte per URL)
   
4. External databases:
   With need for quick response time , in memory database like Redis will be a good choice.
   Redis is open source and seems it have better options compared to Memcached which will help in future expansions
   Using a SQL data base like MySQL will add to response time and the data is very simple to use RDBMS
   
5. Processing HTTP:
   depends on web framework TBD





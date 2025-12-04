# Tech Stack and Components

This section outlines the recommended technologies for building a **URL shortener** that can scale to 10M MAU (Monthly active users).  


## 🌐 API Gateway

The gateway should perform both redirects to the appropriate microservice and JWT authentication for protected endpoints, the API gateway also needs to handle a large amount of traffic

Considering these Kong seems to be a popular open source option that seems to fit this use case, it offers the following features that make it an appropriate pick

- JWT authentication
- 50K+ transactions per second per node it's deployed in
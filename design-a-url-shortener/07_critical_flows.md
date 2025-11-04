# ⚙️ Critical Flows (URL shortener system)

This section documents the core end-to-end flows in URL-Shortener system. It emphasizes **session-based authentication**, converting URLs to short URLs and redirecting to the original URLs when a short URL is hit


## 🔑 0. User Login (Note: User doesn't have to login to create short URLs, this is only for additional features where the User can view all the short URLs they've created in their dashboard)

**Goal:** Authenticate the user and issue a token for subsequent requests.  

| Step | Component                             | Action                                            |
| ---- | ------------------------------------- | ------------------------------------------------- |
| 1    | **User → API Gateway → Auth Service** | POST `/login` with email/password                 |
| 2    | **Auth Service**                      | Validates credentials, generates JWT              |
| 3    | **API Gateway → User**                | Returns JWT                                       |
| 4    | **User → API Gateway → URL Service**  | Sends requests with `Authorization: Bearer <jwt>` |
| 5    | **API Gateway**                       | Validates token (signature + expiry)              |
| 6    | **URL Service**                       | Uses `user_id` claim to fetch URLs                |

**Note:** Look into JWT tokens

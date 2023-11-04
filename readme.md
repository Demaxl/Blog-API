# Blog API with DJANGO REST FRAMEWORK

I am learning django rest framework, This is my second project

## Available Endpoints:

Note: All endpoints are nested with **api/**

```
/articles # List all articles
/articles/<pk> # single article
/articles/<pk>/like # Authenticated. Likes an article
/articles/<pk>/comments # Get article comments
/articles/<pk>/comments/<pk> # Single comment
/articles/<pk>/comments/<pk>/like # Authenticated, Likes a comment
/articles/<pk>/comments/<pk>/replies # Get comment replies
/articles/<pk>/comments/<pk>/replies/<pk> # Single reply
/articles/<pk>/comments/<pk>/replies/<pk>/like # Like a reply
/articles/me # Authenticated. Gets users articles
/author/<username> # Get user information
/author/me/liked-articles # Authenticated. Gets users liked articles
```


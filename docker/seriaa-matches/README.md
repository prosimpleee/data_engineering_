# How to run Serie A api:
1. Create Docker Image: 
```
docker build -t serie-matches
```
2. Run Docker Image   : 
```
docker run -e MY_API_KEY=token(Serie A API Documentation)
           -e MY_AWS_KEY=aws_key 
           -e MY_AWS_SECRET_KEY=aws_sercet_key [ImageName or ImageId]
```

3. Result             :

![MatchDay 34](https://user-images.githubusercontent.com/55916170/167618349-c71d9d56-009e-4ddf-8964-035a26407802.png)


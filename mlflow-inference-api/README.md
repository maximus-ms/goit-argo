
```bash
docker build -t inference-api .
docker tag inference-api:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest

aws ecr get-login-password --region us-east-1 --profile <your-profile>   | docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com

docker push <acconut_id>.dkr.ecr.us-east-1.amazonaws.com/inference-api:latest
```

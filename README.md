# NBT E-Paper Handler

Get today's newspaper at this URL

https://fomknjverbo2erq7grhcgubxyi0rsxhq.lambda-url.ap-south-1.on.aws/

## Steps to deploy using ZIP

1. Clone the repository in your local
2. Follow the given commands to create a deployment package, to be uploaded to Lambda. Refer [this](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) for reference.

```sh
cd NBT-Epaper
mkdir package

pip3 install -r requirements.txt --target ./package
cd package
zip -r ../deployment.zip package

cd ..
zip -r deployment.zip -j handler/
```

3. Now create a Lambda function in AWS Lambda console, and upload this zip named `deployment.zip`


## Steps to deploy using AWS SAM

1. Make sure to install [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
2. Clone the repository in your local, then go inside the NBT-Epaper repository
3. If you have `python3.12` installed in your system, run `sam build; sam deploy`
4. If you don't have `python3.12` installed, you'll need Docker to create the deployment build inside a container. Install docker, and then change user to sudo via `sudo -i`. Then finally run `sam build --use-container; sam deploy`

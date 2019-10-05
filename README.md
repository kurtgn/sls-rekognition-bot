# Installation

## 0. Create AWS account, authorize your computer

- If you don't have an AWS Account - create it (you will need to enter your credit card, sorry)
- Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- Configure CLI by running `aws configure` and enter your credentials ([manual here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration))



## 1. Install dependencies
```
pip install -r requirements.txt
```

or:

```
poetry install
```


## 2. Deploy code to Lambda

After that, open `zappa_settings.json` and change `s3_bucket` variable to something else:

```
{
    "dev": {
        ...
        "s3_bucket": "some-other-unique-name",
        ...
    }
}
```

And then run:

```
zappa deploy dev
```

You will get some console output. Most important two lines are: 

```
Uploading serverless-reko-dev-1570307440.zip (6.0MiB)..
...
Your updated Zappa deployment is live!: https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev
```

From the first line, remember the function name: `serverless-reko-dev`
From the last line, remember the endpoint: `https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev`

Create `.env` file in project folder and add these two variables:

```
LAMBDA_FUNCTION_NAME=serverless-reko-dev
LAMBDA_ENDPOINT=https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev
```



## 3. Set other variables



Add three more lines to `.env` file.

```
...

TELEGRAM_TOKEN=your-telegram-token
BUCKET_NAME=some-bucket-name
DB_NAME=some-db-name
```

Run commands:
```
flask setup
flask post-setup
```

## 4. Have fun!

Now send some pictures to your chatbot. It should be able to reply.



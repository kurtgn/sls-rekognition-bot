# Intro

This is a telegram bot that uses AWS Rekognition to detect emotions on selfies.

<img src="tg_picture.jpg" height="400">


# Installation

## ☁️ 0. Create AWS account, authorize your computer

- If you don't have an AWS Account - create it (you will need to enter your credit card, sorry)
- Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- Configure CLI by running `aws configure` and enter your credentials ([manual here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration))



## 🔌 1. Install dependencies

This works for Python>=3.7.

```
pip install -r requirements.txt
```

or:

```
poetry install
```


## 🏹 2. Deploy code to Lambda

After that, open `zappa_settings.json` and change `s3_bucket` variable to something unique (these buckets need to have globally unique names):

```
{
    "dev": {
        ...
        "s3_bucket": "some-unique-name",
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

- From the first line, remember the function name: `serverless-reko-dev`
- From the last line, remember the endpoint: `https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev`

Create the `.env` file in the project folder and add two variables from above: 

```
LAMBDA_FUNCTION_NAME=serverless-reko-dev
LAMBDA_ENDPOINT=https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev
```

Okay, you have deployed your code but, there is a bit more to configure.

## 🛠️ 3. Set other variables



Add three more lines to `.env` file.

```
...

TELEGRAM_TOKEN=your-telegram-token
BUCKET_NAME=some-bucket-name
DB_NAME=some-db-name
```

- `TELEGRAM_TOKEN` is the token of your Telegram bot. Obtain it [here](https://core.telegram.org/bots#6-botfather)
- `BUCKET_NAME` is the S3 bucket to store uploaded photos.
- `DB_NAME` is the DynamoDB table name where the app will store data.

Run commands:
```
flask setup
flask post-setup
```

## 🔥 4. Have fun!

Now send some selfies to your chatbot. It should be able to reply.


## ☠️ 5. Teardown

If you want to delete everything, you need to do two things:

- To undeploy your app, run: `zappa undeploy dev`
- To delete saved pictures and data, run `flask teardown`.

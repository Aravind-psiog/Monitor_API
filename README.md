# AWS lambda

## _Github action pipeline_

![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

The purpose of this project is to build a API with a reallife usecase.

- FastAPI, Mangum
- Auto pep8
- documenting

## Installation

clone the repo and install requirements by

```
pip install -r requirements.txt
```

### FastAPI

To run the FastAPI

```
cd app
uvicorn main:app --reload
```

Default hostname is ```http://localhost:8000``` and as it has inbuild documentation, ```http://localhost:8000/docs``` can be used to view/test the API's.
```main.py``` is the main app which has API functionalities.

### AWS deployment

For deploying it on AWS lambda, create a repo in Github and add the aws secret,access and region in the secrets environment. Create S3 bucket and lambda function and API endpoint and configure the endpoint to created lambda function. edit the main.yml file and input it with your bucket name. This is a one time setup.

After completing the setup. Deploy it to the git repo. It created a action pipeline which does the rest of the work.

## Troubleshooting

The psycopg2 library which was installed doesnot work on aws lambda engine. reference >> <https://github.com/jkehler/awslambda-psycopg2/issues/47>

I have downloaded the custom build and placed it in ```psycop2-fix``` folder. The pipeline automatically adds this build to the S3 bucket.

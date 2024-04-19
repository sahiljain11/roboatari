# RoboAtari Repository

## Installation

```bash
conda create -n javatari python=3.9.19
conda activate javatari
pip install -r requirements.txt
```

### S3
In order to save the game data, you will need a S3 bucket for the server to upload game and audio data. You'll also need to create an IAM account on AWS. This IAM account will give you access codes (`AMAZON_CLIENT_KEY` and `AMAZON_SECRET_CLIENT_KEY` and `AMAZON_REGION`) for your application to connect to your S3 bucket. After creating the S3 bucket and IAM credentials, you'll need to modify the Permissions to fit the needs of your security policy. If you would like the easiest (and least secure) solution that simply works, add the following to the Bucket Policy and CORS Policy respectively:

#### Bucket Policy
```
{
    "Version": "2012-10-17",
    "Id": "<id_automatically_added>",
    "Statement": [
        {
            "Sid": "<sid_automatically_added>",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::<bucket_name>"
        }
    ]
}
```
#### CORS Policy
```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "POST",
            "PUT",
            "DELETE",
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```

### To run the code locally

```bash
export ROM=<rom_name (spaceinvaders, mspacman, revenge, enduro, seaquest)>
export S3_BUCKET=<s3_bucket_name>
export AMAZON_CLIENT_KEY=<insert_client_key>
export AMAZON_SECRET_CLIENT_KEY=<insert_secret_client_key>
export AMAZON_REGION=<insert_region>
python new_server.py
```

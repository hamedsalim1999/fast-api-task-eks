from fastapi import FastAPI
from fastapi.responses import HTMLResponse , RedirectResponse
from pydantic import BaseModel
from decouple import config  
import boto3

app = FastAPI()

aws_access_key_id = config('AWS_ACCESS_KEY_ID')
aws_secret_access_key = config('AWS_SECRET_ACCESS_KEY')
s3_bucket_name = config('S3_BUCKET_NAME')
s3_object_key = 'view_count.txt'

s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def get_view_count():
    try:
        response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
        count = int(response['Body'].read())
    except s3_client.exceptions.NoSuchKey:
        count = 0
    return count

def store_view_count(count):
    s3_client.put_object(Bucket=s3_bucket_name, Key=s3_object_key, Body=str(count))

class ViewCountResponse(BaseModel):
    count: int

@app.get("/", response_class=HTMLResponse)
async def get_and_increment_view_count():
    view_count = get_view_count()
    view_count += 1
    store_view_count(view_count)
    html_content = f'''
    <html>
    <head>
        <title>View Count</title>
    </head>
    <body>
        <h1>View Count: {view_count}</h1>
        <a href="/restart">Restart Counter</a>
    </body>
    </html>
    '''

    return HTMLResponse(content=html_content)

@app.get("/restart")
async def restart_view_count():
    store_view_count(0)
    return RedirectResponse(url="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
<br>

## **What is S3UpDownLoader**

<br>

- `S3UpDownLoader` helps you upload/download a file or a folder to/from S3 Storage.
- You can upload/download file or folder in the environment of Object Storage (S3 Storage).
- It has good peformance to upload/download files, especially **large size of files.** But it has not good performance to do these with too many small size of files.
- I hope you to use thie code for making your job automation.

<br>

## **Install**

<br>

- If you don't have packages below, those automatically will be installed when you import `S3UpDownLoader`.
    - Requirements : `boto3`, `tqdm`
    - Install packages with `pip install boto3 tqdm`

<br>

## **How to use**

<br>

- There are 4 main method to use.
- ① download file : `.download_file(src_path, dest_path)`
    - Download a file from S3 storage.
        - src_path : a file path including file name in S3 storage to be downloaded. (except bucket name.)
        - dest_path : path in local to be saved.
    - Example : file_example.zip is saved in local_example.
        - src_path : path/.../.../s3_storage/file_example.zip
        - dest_path : C://.../.../local_example

<br>

- ② download folder : `.download_folder(src_path, dest_path)`
    - Download a folder from S3 storage.
        - src_path : folder path (prefix in S3 storage) in S3 storage to be downloaded. (except bucket name.)
        - dest_path : path in local to be saved.
    - Example : s3_storage_example folder is saved in local_example.
        - src_path : path/.../.../s3_storage_example
        - dest_path : C://.../.../local_example

<br>

- ③ uplaod file : `.upload_file(src_path, dest_path)`
    - Upload a file from local to S3 storage.
        - src_path : file path in local to be uploaded. (except bucket name.)
        - dest_path : path in S3 storage
    - Example : file_example.zip is saved in s3_storage_example.
        - src_path : C://.../.../local/file_example.zip
        - dest_path : path/.../.../s3_storage_example

<br>

- ④ upload folder : `.upload_folder(src_path, dest_path)`
    - Upload a folder from local to S3 storage.
        - src_path : folder path in local to be uploaded. (except bucket name.)
        - dest_path : path in S3 storage
    - Example : local_example folder is saved in s3_storage_example.
        - src_path : C://.../.../local_example
        - dest_path : path/.../.../s3_storage_example

<br>

- ⑤ check_path_exists : `.check_path_exists(path)`
    - chech whether input path (directory or file) exists or not.
        - path : directory path or directory + file path
    - Example : return True/False according to the result of path existence.
        - ex1) path : path/.../.../s3_storage_example
        - ex2) path : path/.../.../s3_storage_example/file_example.zip

<br>

## **Example**

<br>

```python
BUCKET_NAME = "USE_REAL_BUCKET_NAME"
ACCESS_KEY = "USE_REAL_ACCESS_KEY"
SECRET_KEY = "USE_REAL_SECRET_KEY"
ENDPOINT_URL = "USE_REAL_ENDPOINT_URL_IF_NECESSARY"

s3_updownloader = S3UpDownLoader(
        bucket_name = BUCKET_NAME,
        access_key = ACCESS_KEY,
        secret_key = SECRET_KEY,
        endpoint_url  = ENDPOINT_URL,
        verbose = False
    )

# ① download a file from S3 storage to local.
src_path="path/.../.../s3_storage/file_example.zip"
dest_path="C://.../.../local_example"
s3_updownloader.download_file(src_path, dest_path)

# ② download a folder from S3 storage to local.
src_path="path/.../.../s3_storage_example"
dest_path="C://.../.../local_example"
s3_updownloader.download_folder(src_path, dest_path)

# ③ upload a file from local storage to S3 storage
src_path="C://.../.../local/file_example.zip"
dest_path="path/.../.../s3_storage_example"
s3_updownloader.upload_file(src_path, dest_path)

# ④ upload a folder from local storage to S3 storage
src_path="C://.../.../local_example"
dest_path="path/.../.../s3_storage_example"
s3_updownloader.upload_folder(src_path, dest_path)

# ⑤ chech whether input path (directory or file) exists or not.
path1 = "path/.../.../s3_storage_example"
path2 = "path/.../.../s3_storage_example/file_example.zip"

if s3_updownloader.check_path_exists(path1):
    print("s3_storage_example folder exists.")
else:
    print("s3_storage_example folder dosen't exist.")

if s3_updownloader.check_path_exists(path2):
    print("file_example.zip file exists.")
else:
    print("file_example.zip file dosen't exist.")
```

<br>

## **How to use run_updownload.py**

<br>

```python

python3 run_updownload.py \
    --updown=up \                                       # (Required) enter 'up' for upload or 'down' for download.
    --filefolder=file \                                 # (Required) enter 'file' for a file or 'folder' for a folder.
    --src_path=C://.../.../local/file_example.zip \     # (Required) enter the path to the file or folder to be up/downloaded.
    --dest_path=path/.../.../s3_storage_example \       # (Required) enter the path to the file or folder to be up/downloaded.
    --bucket_name=USE_REAL_BUCKET_NAME \                # (Optional) bucket name.
    --access_key=USE_REAL_ACCESS_KEY \                  # (Optional) access key.
    --secret_key=USE_REAL_SECRET_KEY \                  # (Optional) secret key.
    --endpoint_url=USE_REAL_ENDPOINT_URL_IF_NECESSARY \ # (Optional) endpoint url for S3 Compatible Storage.
    --verbose=False                                   \ # (Optional) verbose
```

<br>
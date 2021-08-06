import os
import sys
import subprocess
import time
import boto3
from tqdm import tqdm

# install boto3 if not installed.
try:
    import boto3
except ModuleNotFoundError:
    print("Install boto3 in python3")
    subprocess.call([sys.executable, "-m", "pip", "install", 'boto3'])
finally:
    import boto3

# install tqdm if not installed.
try:
    import tqdm
except ModuleNotFoundError:
    print("Install tqdm in python3")
    subprocess.call([sys.executable, "-m", "pip", "install", 'tqdm'])
finally:
    from tqdm import tqdm

class S3UpDownLoader():

    def __init__(self, bucket_name=None, access_key=None, secret_key=None, 
                    endpoint_url=None, multipart_threshold=50, max_concurrency=50, verbose=False):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url
        self.verbose = verbose

        print("s3 resource is being accessed..")
        self.s3 = boto3.resource(
            's3', 
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key, 
            endpoint_url=endpoint_url
        )

        print("s3 client is being accessed..") 
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
        )

        print("s3 bucket is being accessed..") 
        self.bucket = self.s3.Bucket(bucket_name)
        print(">>> Done.")

        self.MB = 1024 ** 2
        self.config = boto3.s3.transfer.TransferConfig(
            multipart_threshold=multipart_threshold * self.MB,
            max_concurrency=max_concurrency
        )

    def get_bytes(self, t):
        '''
        utility function for tqdm progress bar.
        '''
        def inner(bytes_amount):
            t.update(bytes_amount)
        return inner
    
    def remove_last_seperator(self, path):
        '''
        utility function for removing "/" or "\" seperator at the end of path not to create unnecessary path.        
        '''
        if path == "":
            pass
        elif path[-1] == "/" or path[-1] == "\\":
            path = path[:-1:]
        return path

    def check_path_exists(self, path):        
        result = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=path, MaxKeys=1)
        return 'Contents' in result

    def download_folder(self, src_path, dest_path):
        '''
        - Download a folder from S3 storage.
            1. src_path : folder path (prefix in S3 storage) in S3 storage to be downloaded. (except bucket name.)
            2. dest_path : path in local to be saved.
        
        - Example : s3_storage_example folder is saved in local_example.
            1. src_path : path/.../.../s3_storage_example
            2. dest_path : C://.../.../local_example
        '''

        src_path = self.remove_last_seperator(src_path)        
        for obj in self.bucket.objects.filter(Prefix = src_path):        
            src_file_path = obj.key
            destination_path = os.path.abspath(dest_path + "/" + src_file_path)
            
            if not os.path.exists(os.path.dirname(destination_path)):
                os.makedirs(os.path.dirname(destination_path))
                    
            file_size = self.s3.Object(self.bucket_name, src_file_path).content_length
            
            if file_size > 0:
                if self.verbose == True:
                    print(">>> download file : (S3 storage) " + src_file_path + " -> (Local) " + destination_path)
                    time.sleep(0.3)
                    with tqdm(total=file_size, unit='B', unit_scale=True, desc=src_file_path, ascii=True) as t:
                        self.bucket.download_file(src_file_path, destination_path, Config=self.config, Callback=self.get_bytes(t)) 
                else:
                    print(">>> download file : (S3 storage) " + src_file_path + " -> (Local) " + destination_path)
                    self.bucket.download_file(src_file_path, destination_path, Config=self.config) 
                    print(">>> Done.")

    
    def download_file(self, src_path, dest_path):
        '''
        - Download a file from S3 storage.
            1. src_path : a file path including file name in S3 storage to be downloaded. (except bucket name.)
            2. dest_path : path in local to be saved.
            
        - Example : file_example.zip is saved in local_example.
            1. src_path : path/.../.../s3_storage/file_example.zip
            2. dest_path : C://.../.../local_example
        '''

        file_size = self.s3.Object(self.bucket_name, src_path).content_length
        file_name = os.path.basename(src_path)
        destination_path = os.path.abspath(dest_path + "/" + file_name)

        if self.verbose == True:
            print(">>> download file : (S3 storage) " + src_path + " -> (Local) " + destination_path)
            time.sleep(0.3)
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=src_path, ascii=True) as t:
                self.bucket.download_file(src_path, destination_path, Config=self.config, Callback=self.get_bytes(t))
        else:
            print(">>> download file : (S3 storage) " + src_path + " -> (Local) " + destination_path)
            self.bucket.download_file(src_path, destination_path, Config=self.config)
            print("Done.")


    def upload_folder(self, src_path, dest_path):
        
        '''
        - Upload a folder from local to S3 storage.
            1. src_path : folder path in local to be uploaded. (except bucket name.)
            2. dest_path : path in S3 storage
            
        - Example : local_example folder is saved in s3_storage_example.
            1. src_path : C://.../.../local_example
            2. dest_path : path/.../.../s3_storage_example
        '''
        
        src_file_paths = []
        src_path = os.path.abspath(src_path).replace("\\", "/")
        for root, folders, files in os.walk(src_path):
            for file in files:
                src_file_paths.append(os.path.join(root, file).replace("\\", "/"))                
        base_folder = os.path.basename(os.path.normpath(src_path))
        base_file_paths = [base_folder + "/" + src_file_path.replace(src_path + "/", "") for src_file_path in src_file_paths]
        
        for src_file_path, base_file_path in zip(src_file_paths, base_file_paths):            
            file_size = os.path.getsize(src_file_path)
            file_name = os.path.basename(src_file_path)
            
            dest_path = self.remove_last_seperator(dest_path)
            if dest_path == "":
                destination_path = base_file_path
            else:
                destination_path = dest_path + "/" + base_file_path
        
            if self.verbose == True:
                print(">>> upload file : (Local) " + src_file_path + " -> (S3 Storage) " + destination_path)
                time.sleep(0.3)
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name, ascii=True) as t:
                    self.s3.meta.client.upload_file(src_file_path, self.bucket_name, destination_path, Config=self.config, Callback=self.get_bytes(t)) 
            else:
                print(">>> upload file : (Local) " + src_file_path + " -> (S3 Storage) " + destination_path)
                self.s3.meta.client.upload_file(src_file_path, self.bucket_name, destination_path, Config=self.config) 
                print("Done.")
        
        
    def upload_file(self, src_path, dest_path):
        
        '''
        - Upload a file from local to S3 storage.
            1. src_path : file path in local to be uploaded. (except bucket name.)
            2. dest_path : path in S3 storage
            
        - Example : file_example.zip is saved in s3_storage_example.
            1. src_path : C://.../.../local/file_example.zip
            2. dest_path : path/.../.../s3_storage_example
        '''

        src_path = os.path.abspath(src_path)
        file_size = os.path.getsize(src_path)
        file_name = os.path.basename(src_path)
        
        dest_path = self.remove_last_seperator(dest_path)
        if dest_path == "":
            destination_path = file_name
        else:
            destination_path = dest_path + "/" + file_name

        if self.verbose == True:
            print(">>> upload file : (Local) " + src_path + " -> (S3 Storage) " + destination_path)
            time.sleep(0.3)
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name, ascii=True) as t:
                self.s3.meta.client.upload_file(src_path, self.bucket_name, destination_path, Config=self.config, Callback=self.get_bytes(t)) 
        else:
            print(">>> upload file : (Local) " + src_path + " -> (S3 Storage) " + destination_path)
            self.s3.meta.client.upload_file(src_path, self.bucket_name, destination_path, Config=self.config) 
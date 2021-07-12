import os
import argparse
from S3UpDownLoader import S3UpDownLoader

#############################################################
BUCKET_NAME = "######################"
ACCESS_KEY = "#######################"
SECRET_KEY = "#######################"
ENDPOINT_URL = None
#############################################################

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--updown', required=True, help="(Required) enter 'up' for upload or 'down' for download.")
    parser.add_argument('--filefolder', required=True, help="(Required) enter 'file' for a file or 'folder' for a folder.")
    parser.add_argument('--src_path', required=True, help='(Required) enter the path to the file or folder to be up/downloaded.')
    parser.add_argument('--dest_path', required=True, help='(Required) enter the path to the file or folder to be up/downloaded.')

    parser.add_argument('--bucket_name', default=None, help='(Optional) bucket name.')
    parser.add_argument('--access_key', default=None, help='(Optional) access key.')
    parser.add_argument('--secret_key', default=None, help='(Optional) secret key.')
    parser.add_argument('--endpoint_url', default=None, help='(Optional) endpoint url for S3 Compatible Storage.')
    parser.add_argument('--multipart_threshold', type=int, default=50, help='(Optional) size of eachpart. default is 50 (Mega Byte).')
    parser.add_argument('--max_concurrency', type=int, default=50, help='(Optional) the number of maximum concurrent multipart. default is 50.')
    parser.add_argument('--verbose', type=bool, default=False, help='(Optional) verbose. default is False.')


    args = parser.parse_args()
    return args

def set_credentials(args):

    if args.bucket_name == None:
        args.bucket_name = BUCKET_NAME
    
    if args.access_key == None:
        args.access_key = ACCESS_KEY

    if args.secret_key == None:
        args.secret_key = SECRET_KEY

    if args.endpoint_url == None:
        args.endpoint_url = ENDPOINT_URL
    
    return args



if __name__ == "__main__":
    
    args = get_args()
    args = set_credentials(args)
    s3_updownloader = S3UpDownLoader(
        bucket_name = args.bucket_name,
        access_key = args.access_key,
        secret_key = args.secret_key ,
        endpoint_url  = args.endpoint_url,
        verbose = args.verbose
    )
    
    if args.updown == "up":
        if args.filefolder == "file":
            s3_updownloader.upload_file(args.src_path, args.dest_path)
        elif args.filefolder == "folder":
            s3_updownloader.upload_folder(args.src_path, args.dest_path)
        else:
            print("filefolder must be 'file' or 'folder'.")
    elif args.updown == "down":
        if args.filefolder == "file":
            s3_updownloader.download_file(args.src_path, args.dest_path)
        elif args.filefolder == "folder":
            s3_updownloader.download_folder(args.src_path, args.dest_path)
        else:
            print("filefolder must be 'file' or 'folder'.")
    else:
        print("updown must be 'up' or 'down'.")

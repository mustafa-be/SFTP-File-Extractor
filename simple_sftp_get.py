import pysftp
from pysftp import CnOpts
import stat
import sys
from datetime import datetime
import json
from os import path
import os

def get_json(path):
    with open(path) as f:
        try:
            json_file=json.load(f)
            return json_file
        except Exception as e:
            print(path)
            print("Invalid JSON, exiting",e)
            return {}



def sftp_get_n_store_files(host,port,username,password,input_path,output_path,output_backup_path):
    # If output_path and backup_path (local) are directories Skip
    if not path.isdir(output_path) or not path.isdir(output_backup_path):
        print("Skipping: Wrong outputs paths \n1.Output:",output_path,"\n2:OutputBackup",output_backup_path)
        return
    try:
        output_backup_path=output_backup_path
        output_path=output_path
        #cnopts = pysftp.CnOpts()
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        # Establish connection to host using function parameters
        print("hahahaworiking")
        # , private_key=".ppk", cnopts=cnopts
        # , username=username, private_key="./p.pem"
        with pysftp.Connection(host=host,port=int(port), username=username, password=password, cnopts=cnopts) as sftp:
#        with pysftp.Connection(host=host,port=int(port),username=username,password=password, cnopts=cnopts) as sftp:
            # Change the working directory at sftp server, Skips if
            try:
                sftp.cwd(input_path)
            except Exception as e:
                print("Skipping: Wrong SFTP Input Path CWD ",e)
                return
            
            try:
                print(input_path,output_path)
                sftp.get_r(input_path,output_path, preserve_mtime=False)
                os.rename(output_path+"/root",output_path+"/root"+datetime.now().strftime("%d-%m-%Y %H-%M-%S"))
                pass
            except Exception as e:
                print("Skipping: Wrong SFTP Input Path GET_Rs ",e)
                return
            
#            sftp.get_r('public', './output', preserve_mtime=True)


    except Exception as e:

        print("Skipping : Error while connecting to SFTP host",e)
        return



# https://stackoverflow.com/questions/38939454/verify-host-key-with-pysftp
# https://pysftp.readthedocs.io/en/release_0.2.9/cookbook.html#pysftp-connection
# https://stackoverflow.com/questions/53864260/no-hostkey-for-host-found-when-connecting-to-sftp-server-with-pysftp-usi
# https://stackoverflow.com/questions/34097068/pysftp-authenticationexception-while-connecting-to-server-with-private-key
# https://stackoverflow.com/questions/50118919/python-pysftp-get-r-from-linux-works-fine-on-linux-but-not-on-windows
# https://aws.amazon.com/premiumsupport/knowledge-center/convert-pem-file-into-ppk/
#
#


if __name__ == "__main__":
    if len(sys.argv)==2:
        hosts=get_json(sys.argv[1])
        k=list(hosts.keys())[0]
        print(hosts)
        host=hosts[k]
        ip=hosts[k]['ip']
        port=hosts[k]['port']
        username=hosts[k]['username']
        password=hosts[k]['password']
        input_path=hosts[k]['input_path']
        output_path=hosts[k]['output_path']
        output_backup_path=hosts[k]['output_path']
        sftp_get_n_store_files(ip,port,username,password,input_path,output_path, output_backup_path)
    
    else:
        print("Invalid Arguement\n python simple_sftp_get.py /path/to/data.json")
from zipfile import ZipFile, ZIP_DEFLATED
import os
import subprocess

def make_zip_from_file_list( zip_path, file_list ):
    error_code = 0
    zip_binary = None
    import platform
    platform_type = platform.system()
    if platform_type == 'Linux':
        args = ['zip', '-j9q', zip_path] + file_list
        error_code = subprocess.call( args )
    else:
        file_obj = ZipFile( file = zip_path, compression = ZIP_DEFLATED, mode = 'w' )
        for file_to_zip in file_list:
            file_zip_name = os.path.split( file_to_zip )[-1]
            file_obj.write( file_to_zip, file_zip_name )
        file_obj.close()
    
    if error_code == 0:
        zipped_file = open(zip_path, 'rb')
        zip_binary = zipped_file.read()
        zipped_file.close()
        
    if zip_path != None and os.path.exists( zip_path ) and os.path.isfile( zip_path ):
        try: os.remove( zip_path )
        except: pass
    return zip_binary
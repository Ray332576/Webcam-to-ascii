
import zipfile
import os
from datetime import datetime

def create_zip():
    zip_filename = "ascii_project.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            # Skip hidden directories and files
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.') and f != zip_filename]
            
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, ".")
                
                # Create ZipInfo with current timestamp to avoid pre-1980 error
                info = zipfile.ZipInfo(arc_name)
                info.date_time = datetime.now().timetuple()[:6]
                
                with open(file_path, 'rb') as src:
                    zipf.writestr(info, src.read())

create_zip()
print("✅ Project zipped as ascii_project.zip!")

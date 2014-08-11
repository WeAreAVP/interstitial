import os

def setImportBaseBath():
    base_path = os.getcwd()
    base_path = base_path.replace(r'\tests', '')
    base_path = base_path.replace(r'\Fixtures', '')
    base_path = base_path.replace(r'/tests', '')
    base_path = base_path.replace(r'/Fixtures', '')
    return os.path.join(base_path,'')
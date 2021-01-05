from xml.etree.ElementTree import parse, Element
import os

path = r'G:\数据\q3\motorhelpet'

def iter_files(rootDir):
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file.endswith('xml'):
                file_name = os.path.join(root, file)
                print(file_name)
                deal_xml(file_name)
        for dir in dirs:
            iter_files(dir)



def deal_xml(file):
    try:
        doc = parse(file)
    except:
        print(file)
        return
    root = doc.getroot()
    tf = root.find('folder')
    fn = root.find('filename')
    tp = root.find('path')
    if tf is not None:
        root.remove(tf)
    if fn is not None:
        root.remove(fn)
    if tp is not None:
        root.remove(tp)
    doc.write(file, xml_declaration=True)

iter_files(path)
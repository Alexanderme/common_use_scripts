from collections import defaultdict
import os
from xml.etree.ElementTree import parse


def iter_files(rootDir):
    """
    根据文件路径 返回文件名称 以及文件路径名称
    :param rootDir:
    :return:
    """
    filenames = defaultdict(list)
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file = os.path.join(root, file)
            if file.lower().endswith("xml"):
                filenames["xml_dir"].append(file)
            else:
                filenames["error_file"].append(file)
        for dir in dirs:
            iter_files(dir)

    return filenames


filenames = iter_files(
    r"C:\Users\Administrator\Desktop\WHGKhelmet20200518done_helmettestdataset_v2\WHGKhelmet20200518done_helmettestdataset_v2")

xmlfiles = filenames["xml_dir"]
for xml in xmlfiles:
    file = xml.split("/")[-1]
    doc = parse(xml)
    root = doc.getroot()
    res_kinds = doc.iterfind('object/name')
    res_coordinates = doc.iterfind('object/bndbox')
    for res_kind in res_kinds:
        print(res_kind.text)
        if res_kind.text == "hat":
            res_kind.text = "helemt"
            doc.write(xml, xml_declaration=True)

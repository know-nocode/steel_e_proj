import logging
import requests
import untangle
import zipfile
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import fsspec
from io import StringIO

# write logs to a file
logging.basicConfig(
    filename='C:\\Users\\DELL\\Desktop\\SteelProject\\steel.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

download_links = [] #Global Variable list for storing download links

def downXML(URL, f_loc):
    """
    Download XML from a specified URL and save it to a local file.

    Args:
        URL (str): URL from where XML will be downloaded.
        f_loc (str): The local file path where the downloaded XML will be saved.

    Returns:
        None
    """
    logging.info(f"Starting download from URL: {URL}")
    response = requests.get(URL)
    
    try:
        with open(f_loc, 'wb') as file:
            file.write(response.content)
            logging.info(f"Successfully downloaded and saved to: {f_loc}")
    except Exception as e:
        logging.error(f"Error writing to file {f_loc}: {e}")

def parXML(file_path):
    """
    Parse an XML file to extract download links.

    Args:
        file_path (str): The path to the XML file for retrieving download links.

    Returns:
        list: A list of download links extracted from the XML.
    """
    logging.info(f"Parsing XML file: {file_path}")
    parsed_xml = untangle.parse(file_path)
    
    if hasattr(parsed_xml, 'response') and hasattr(parsed_xml.response, 'result'):
        for doc in parsed_xml.response.result.doc:
            file_type = None
            download_link = None
            
            for x in doc.str:
                if x['name'] == 'file_type':
                    file_type = x.cdata  
                elif x['name'] == 'download_link':
                    download_link = x.cdata 

            if file_type == 'DLTINS' and download_link:
                download_links.append(download_link)
    
    if len(download_links) > 1:
        logging.info(f"Found second download link: {download_links[1]}")
    else:
        logging.warning("Less than two download links found.")
    
    return download_links

def extract_xml_from_zip(zip_file_path):
    """
    Extract XML files from a ZIP archive.

    Args:
        zip_file_path (str): The path to the ZIP file.

    Returns:
        list: A list of XML file contents extracted from the ZIP.
    """
    xml_contents = []
    logging.info(f"Extracting XML from zip file: {zip_file_path}")
    
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            for file_name in zip_file.namelist():
                if file_name.endswith('.xml'):
                    with zip_file.open(file_name) as xml_file:
                        xml_contents.append(xml_file.read())
                        logging.info(f"Found XML file in zip: {file_name}")
    except Exception as e:
        logging.error(f"Error extracting XML from ZIP: {e}")
    
    return xml_contents

def xml_to_csv(xml_strings, csv_file_path):
    """
    Convert XML strings to a CSV file.

    Args:
        xml_strings (list): A list of XML string contents.
        csv_file_path (str): The path where the CSV file will be saved.

    Returns:
        None
    """
    headers = [
        "FinInstrmGnlAttrbts.Id",
        "FinInstrmGnlAttrbts.FullNm",
        "FinInstrmGnlAttrbts.ClssfctnTp",
        "FinInstrmGnlAttrbts.CmmdtyDerivInd",
        "FinInstrmGnlAttrbts.NtnlCcy",
        "Issr"
    ]

    csv_rows = []

    for xml_data in xml_strings:
        try:
            root = ET.fromstring(xml_data)
            logging.info(f"Processing XML string with {len(root)} xml elements")
            
            for x in root.iter():
                if x.tag.endswith('FinInstrmGnlAttrbts'):
                    row = []
                    for child in x:
                        row.append(child.text if child.text is not None else '')
                    csv_rows.append(row)
                elif x.tag.endswith('Issr'):
                    row = [x.text if x.text is not None else '']
                    csv_rows.append(row)
        except Exception as e:
            logging.error(f"Error processing XML string: {e}")
    
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
            writer.writerows(csv_rows)
            logging.info(f"Successfully wrote CSV to {csv_file_path}")
    except Exception as e:
        logging.error(f"Error writing to CSV file: {e}")

def modify_and_upload_csv_cloud(file_path, cloud_path):
    """
    Modify a CSV file and upload it to the cloud.

    Args:
        file_path (str): The path to the CSV file to be modified.
        cloud_path (str): The cloud path where the modified CSV will be uploaded.

    Returns:
        None
    """
    logging.info(f"Modifying CSV file: {file_path}")
    df = pd.read_csv(file_path, encoding='ISO-8859-1')

    df['a_count'] = df['FinInstrmGnlAttrbts.FullNm'].str.count('a').fillna(0).astype(int)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, lineterminator='\n')
    logging.info(f"Uploading modified CSV to cloud at: {cloud_path}")
    
    try:
        with fsspec.open(cloud_path, 'w') as f:
            f.write(csv_buffer.getvalue())
            logging.info(f"Successfully uploaded CSV to cloud at {cloud_path}")
    except Exception as e:
        logging.error(f"Error uploading CSV to cloud: {e}")

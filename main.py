import steelProject

def main():
    """
    Main function to orchestrate the workflow of downloading, parsing,
    and converting XML data into CSV format.

    This function performs the following steps:
    1. Downloads XML data from a specified URL and saves it to a local file.
    2. Parse the downloaded XML file to extract relevant download links.
    3. Downloads a ZIP file from one of the extracted download links.
    4. Extracts XML contents from the downloaded ZIP file.
    5. Converts the extracted XML contents into a CSV file.

    Note:
        Uncomment the desired option from the last three lines to upload the generated CSV file
        to a cloud storage service (AWS, Azure or to local disk).

    Returns:
        None
    """
    steelProject.downXML('https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100',
                            'C:\\Users\\DELL\\Desktop\\SteelProject\\Steelnew.xml')
    steelProject.parXML('C:\\Users\\DELL\\Desktop\\SteelProject\\Steelnew.xml')
    steelProject.downXML(steelProject.download_links[1],'C:\\Users\\DELL\\Desktop\\SteelProject\\aa.zip')
    xml_contents=steelProject.extract_xml_from_zip('C:\\Users\\DELL\\Desktop\\SteelProject\\aa.zip')
    steelProject.xml_to_csv(xml_contents, 'C:\\Users\\DELL\\Desktop\\SteelProject\\teststeel.csv')
    
    steelProject.modify_and_upload_csv_cloud('C:\\Users\\DELL\\Desktop\\SteelProject\\teststeel.csv','C:\\Users\\DELL\\Desktop\\SteelProject\\testnewSteel.csv') #local disk
    #steelProject.modify_and_upload_csv_cloud('C:\\Users\\DELL\\Desktop\\SteelProject\\teststeel.csv', 's3://csvbypy/up-csv/newSteel.csv') #AWS
    #steelProject.modify_and_upload_csv_cloud('C:\\Users\\DELL\\Downloads\\SE\\BP\\aa\\output.csv', 'az://azurecontainer/newSteel.csv') #AZURE

if __name__ == "__main__":
    main()

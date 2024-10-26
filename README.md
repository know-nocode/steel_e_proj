# Steel Project

This project is designed to download XML data from a specified URL, parse the XML to extract relevant download links, download a ZIP file containing XML files, extract the XML contents, and convert them into a CSV format. The CSV file can then be modified and uploaded to a cloud storage service or saved locally.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Logging](#logging)
- [Functions](#functions)
- [Contributing](#contributing)

## Features

- Download XML data from a specified URL.
- Parse XML files to extract download links.
- Download and extract XML files from ZIP archives.
- Convert extracted XML data into a CSV format.
- Modify the CSV file by adding a new column based on specific criteria.
- Upload the modified CSV file to cloud storage (AWS, Azure) or save it locally.

## Installation

To run this project, you need to have Python installed on your machine. You also need to install the required libraries. You can do this using pip:

cmd:
>python pip install requests untangle pandas fsspec
Make sure you have access to the cloud storage libraries and have proper credentials like IAM keys, if you plan to upload files to AWS or Azure.

Usage
Clone the repository or download the source code.
Navigate to the project directory.
Update the file paths in the main() function to match your local environment.

Note:
Uncomment the desired option in the main() function to upload the generated CSV file to a cloud storage service (AWS, Azure) or to save it to a local disk.

Logging
Logs are written to a file named steel.log located in the project directory. The logging level is set to INFO, which records important events in the workflow.

Functions
downXML(URL, f_loc)
Downloads XML data from a specified URL and saves it to a local file.

parXML(file_path)
Parses an XML file to extract download links.

extract_xml_from_zip(zip_file_path)
Extracts XML files from a ZIP archive.

xml_to_csv(xml_strings, csv_file_path)
Converts XML to a CSV file.

modify_and_upload_csv_cloud(file_path, cloud_path)
Modifies a CSV file and uploads it to the cloud.

Contributing
Contributions are welcome! If you have suggestions for improvements or would like to add features, please create a pull request or open an issue.
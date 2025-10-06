from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential
import requests
import json
import os
import csv
import io
from datetime import datetime
import argparse

marker_map = {"U": 4, "I": 4, "D": 2}

class OpenMirroringClient:
    """
    Licensed under the MIT License.
    """

    def __init__(self, client_id: str, client_secret: str, client_tenant: str, host: str, table_metadata: dict = None, target_table_name: str = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_tenant = client_tenant
        self.host = self._normalize_path(host)
        self.service_client = self._create_service_client()
        self.table_metadata = table_metadata
        self.target_table_name = target_table_name

    def _normalize_path(self, path: str) -> str:
        """
        Normalizes the given path by removing the 'LandingZone' segment if it ends with it.

        :param path: The original path.
        :return: The normalized path.
        """
        if path.endswith("LandingZone"):
            return path[:path.rfind("/LandingZone")]
        elif path.endswith("LandingZone/"):
            return path[:path.rfind("/LandingZone/")]
        return path

    def _create_service_client(self):
        """Creates and returns a DataLakeServiceClient."""
        try:
            credential = ClientSecretCredential(self.client_tenant, self.client_id, self.client_secret)
            return DataLakeServiceClient(account_url=self.host, credential=credential)
        except Exception as e:
            raise Exception(f"Failed to create DataLakeServiceClient: {e}")

    def create_table(self, schema_name: str = None, table_name: str = "", key_cols: list = []):
        """
        Creates a folder in OneLake storage and a _metadata.json file inside it.

        :param schema_name: Optional schema name.
        :param table_name: Name of the table.
        :param key_cols: List of key column names.
        """
        if not table_name:
            raise ValueError("table_name cannot be empty.")

        # Construct the folder path
        folder_path = f"{schema_name}.schema/{table_name}" if schema_name else f"{table_name}"

        try:
            # Create the folder
            file_system_client = self.service_client.get_file_system_client(file_system="LandingZone")  # Replace with your file system name
            directory_client = file_system_client.get_directory_client(folder_path)
            directory_client.create_directory()

            # Create the _metadata.json file
            metadata_content = {"keyColumns": [f'{col}' for col in key_cols]}
            metadata_file_path = os.path.join(folder_path, "_metadata.json")
            file_client = directory_client.create_file("_metadata.json")
            file_client.append_data(data=json.dumps(metadata_content), offset=0, length=len(json.dumps(metadata_content)))
            file_client.flush_data(len(json.dumps(metadata_content)))

            print(f"Folder and _metadata.json created successfully at: {folder_path}")
        except Exception as e:
            raise Exception(f"Failed to create table: {e}")

    def remove_table(self, schema_name: str = None, table_name: str = "", remove_schema_folder: bool = False):
        """
        Deletes a folder in the OneLake storage.

        :param schema_name: Optional schema name.
        :param table_name: Name of the table.
        :param remove_schema_folder: If True, removes the schema folder as well.
        """
        if not table_name:
            table_name = self.target_table_name

        # Construct the folder path
        folder_path = f"{schema_name}.schema/{table_name}" if schema_name else f"{table_name}"

        try:
            # Get the directory client
            file_system_client = self.service_client.get_file_system_client(file_system="LandingZone")  # Replace with your file system name
            directory_client = file_system_client.get_directory_client(folder_path)

            # Check if the folder exists
            if not directory_client.exists():
                print(f"Warning: Folder '{folder_path}' not found.")
                return

            # Delete the folder
            directory_client.delete_directory()
            print(f"Folder '{folder_path}' deleted successfully.")

            # Check if schema folder exists
            if remove_schema_folder and schema_name:
                schema_folder_path = f"{schema_name}.schema"
                schema_directory_client = file_system_client.get_directory_client(schema_folder_path)
                if schema_directory_client.exists():
                    schema_directory_client.delete_directory()
                    print(f"Schema folder '{schema_folder_path}' deleted successfully.")
                else:
                    print(f"Warning: Schema folder '{schema_folder_path}' not found.")
        except Exception as e:
            raise Exception(f"Failed to delete table: {e}")

    def get_next_file_name(self, schema_name: str = None, table_name: str = "") -> str:
        """
        Finds the next file name for a folder in OneLake storage.

        :param schema_name: Optional schema name.
        :param table_name: Name of the table.
        :return: The next file name padded to 20 digits.
        """
        if not table_name:
            raise ValueError("table_name cannot be empty.")

        # Construct the folder path
        folder_path = f"LandingZone/{schema_name}.schema/{table_name}" if schema_name else f"LandingZone/{table_name}"

        try:
            # Get the system client
            file_system_client = self.service_client.get_file_system_client(file_system=folder_path)

            # List all files in the folder
            file_list = file_system_client.get_paths(recursive=False)
            parquet_files = []

            for file in file_list:
                file_name = os.path.basename(file.name)
                if not file.is_directory and file_name.endswith(".csv") and not file_name.startswith("_"):
                    # Validate the file name pattern
                    print(f"file_name: {file_name}")
                    print(f"file_name[:-4]: {file_name[:-4]}")
                    if not file_name[:-4].isdigit() or len(file_name[:-4]) != 20:  # Exclude ".csv"
                        raise ValueError(f"Invalid file name pattern: {file_name}")
                    parquet_files.append(int(file_name[:-4]))

            # Determine the next file name
            if parquet_files:
                next_file_number = max(parquet_files) + 1
            else:
                next_file_number = 1

            # Return the next file name padded to 20 digits
            return f"{next_file_number:020}.csv"

        except Exception as e:
            raise Exception(f"Failed to get next file name: {e}")

    def upload_data_file(self, schema_name: str = None, table_name: str = "", local_file_path: str = ""):
        """
        Uploads a file to OneLake storage.

        :param schema_name: Optional schema name.
        :param table_name: Name of the table.
        :param local_file_path: Path to the local file to be uploaded.
        """
        if not table_name:
            table_name = self.target_table_name
        if not local_file_path or not os.path.isfile(local_file_path):
            raise ValueError("Invalid local file path.")

        # Construct the folder path
        folder_path = f"{schema_name}.schema/{table_name}" if schema_name else f"{table_name}"

        try:
            # Get the directory client
            file_system_client = self.service_client.get_file_system_client(file_system="LandingZone")  # Replace with your file system name
            directory_client = file_system_client.get_directory_client(folder_path)

            # Check if the folder exists
            if not directory_client.exists():
                raise FileNotFoundError(f"Folder '{folder_path}' not found.")

            # Get the next file name
            next_file_name = self.get_next_file_name(schema_name, table_name)

            # Add an underscore to the file name for temporary upload
            temp_file_name = f"_{next_file_name}"

            # Upload the file
            file_client = directory_client.create_file(temp_file_name)
            with open(local_file_path, "rb") as file_data:
                file_contents = file_data.read()
                file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
                file_client.flush_data(len(file_contents))

            print(f"File uploaded successfully as '{temp_file_name}'.")

            # Python SDK doesn't handle rename properly for onelake, using REST API to rename the file instead
            self.rename_file_via_rest_api(f"LandingZone/{folder_path}", temp_file_name, next_file_name)
            print(f"File renamed successfully to '{next_file_name}'.")

        except Exception as e:
            raise Exception(f"Failed to upload data file: {e}")

    def rename_file_via_rest_api(self, folder_path: str, old_file_name: str, new_file_name: str):
        # Create a ClientSecretCredential
        credential = ClientSecretCredential(self.client_tenant, self.client_id, self.client_secret)
        # Get a token
        token = credential.get_token("https://storage.azure.com/.default").token

        # Construct the rename URL
        rename_url = f"{self.host}/{folder_path}/{new_file_name}"

        # Construct the source path
        source_path = f"{self.host}/{folder_path}/{old_file_name}"

        # Set the headers
        headers = {
            "Authorization": f"Bearer {token}",
            "x-ms-rename-source": source_path,
            "x-ms-version": "2020-06-12"
        }

        # Send the rename request
        response = requests.put(rename_url, headers=headers)

        if response.status_code in [200, 201]:
            print(f"File renamed from {old_file_name} to {new_file_name} successfully.")
        else:
            print(f"Failed to rename file. Status code: {response.status_code}, Error: {response.text}")

    def get_mirrored_database_status(self):
        """
        Retrieves and displays the status of the mirrored database from Monitoring/replicator.json.

        :raises Exception: If the status file or path does not exist.
        """
        file_system_client = self.service_client.get_file_system_client(file_system="Monitoring")
        try:
            file_client = file_system_client.get_file_client("replicator.json")
            if not file_client.exists():
                raise Exception("No status of mirrored database has been found. Please check whether the mirrored database has been started properly.")

            download = file_client.download_file()
            content = download.readall()
            status_json = json.loads(content)
            print(json.dumps(status_json, indent=4))
        except Exception:
            raise Exception("No status of mirrored database has been found. Please check whether the mirrored database has been started properly.")

    def get_table_status(self, schema_name: str = None, table_name: str = None):
        """
        Retrieves and displays the status of tables from Monitoring/table.json.

        :param schema_name: Optional schema name to filter.
        :param table_name: Optional table name to filter.
        :raises Exception: If the status file or path does not exist.
        """
        file_system_client = self.service_client.get_file_system_client(file_system="Monitoring")
        try:
            file_client = file_system_client.get_file_client("tables.json")
            if not file_client.exists():
                raise Exception("No status of mirrored database has been found. Please check whether the mirrored database has been started properly.")

            download = file_client.download_file()
            content = download.readall()
            status_json = json.loads(content)

            # Treat None as empty string for filtering
            schema_name = schema_name or ""
            table_name = table_name or ""

            if not schema_name and not table_name:
                # Show the whole JSON content
                print(json.dumps(status_json, indent=4))
            else:
                # Filter tables array
                filtered_tables = [
                    t for t in status_json.get("tables", [])
                    if t.get("sourceSchemaName", "") == schema_name and t.get("sourceTableName", "") == table_name
                ]
                print(json.dumps({"tables": filtered_tables}, indent=4))
        except Exception:
            raise Exception("No status of mirrored database has been found. Please check whether the mirrored database has been started properly.")

    def create_table_with_metadata(self, schema_name: str = None, table_name: str = "", metadata_file_path: str = ""):
        """
        PingCAP SA. OpenMirroring.
        Creates a folder in OneLake storage and read a provided _metadata.json file.

        :param schema_name: Optional schema name.
        :param table_name: Name of the table.
        :param metadata_file_path: Path to the _metadata.json file.
        """
        if not table_name:
            raise ValueError("table_name cannot be empty.")

        # Construct the folder path
        folder_path = f"{schema_name}.schema/{table_name}" if schema_name else f"{table_name}"

        try:
            # Create the folder
            file_system_client = self.service_client.get_file_system_client(file_system="LandingZone")  # Replace with your file system name
            directory_client = file_system_client.get_directory_client(folder_path)
            directory_client.create_directory()

            # Create the _metadata.json file
            with open(metadata_file_path, "r", encoding="utf-8") as f:
                metadata_content = json.load(f)
            metadata_file_path = os.path.join(folder_path, "_metadata.json")
            file_client = directory_client.create_file("_metadata.json")
            file_client.append_data(data=json.dumps(metadata_content), offset=0, length=len(json.dumps(metadata_content)))
            file_client.flush_data(len(json.dumps(metadata_content)))

            print(f"Folder and _metadata.json created successfully at: {folder_path}")
        except Exception as e:
            raise Exception(f"Failed to create table: {e}")

    def create_table_with_class_metadata(self, schema_name: str = None, table_name: str = ""):
        """
        PingCAP SA. OpenMirroring.
        Creates a folder in OneLake storage and read a provided _metadata.json file.

        :param schema_name: Optional schema name.
        :param table_name: Name of the table.
        """

        metadata_file_path = "./_metadata.json"
        with open(metadata_file_path, "w", encoding="utf-8") as f:
            json.dump(self.table_metadata, f, ensure_ascii=False, indent=4)

        if not table_name:
            raise ValueError("table_name cannot be empty.")

        # Construct the folder path
        folder_path = f"{schema_name}.schema/{table_name}" if schema_name else f"{table_name}"

        try:
            # Create the folder
            file_system_client = self.service_client.get_file_system_client(file_system="LandingZone")  # Replace with your file system name
            directory_client = file_system_client.get_directory_client(folder_path)
            directory_client.create_directory()

            # Create the _metadata.json file
            with open(metadata_file_path, "r", encoding="utf-8") as f:
                metadata_content = json.load(f)
            metadata_file_path = os.path.join(folder_path, "_metadata.json")
            file_client = directory_client.create_file("_metadata.json")
            file_client.append_data(data=json.dumps(metadata_content), offset=0, length=len(json.dumps(metadata_content)))
            file_client.flush_data(len(json.dumps(metadata_content)))

            print(f"Folder and _metadata.json created successfully at: {folder_path}")
        except Exception as e:
            raise Exception(f"Failed to create table: {e}")

    def convert_cdc_to_landingzone_file(self, cdc_file_content: str):
        columns = [col["Name"] for col in self.table_metadata["SchemaDefinition"]["Columns"]]
        header = columns + ["__rowMarker__"]

        # Write the header and all rows into a file
        output_filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(output_filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator="\r\n", quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            for line in cdc_file_content.splitlines():
                if not line.strip():
                    continue
                row = next(csv.reader(io.StringIO(line)))
                # Discard the second and third columns (index 1 and 2)
                row = [row[0]] + row[3:]
                row_marker = marker_map.get(row[0])
                # Remove the second and third columns from the original line for consistency
                # But since we already have the row as a list, just write it out
                final_row = row[1:] + [str(row_marker)]
                writer.writerow(final_row)

        return output_filename

    def upload_data_file_as(self, schema_name: str = None, table_name: str = "", local_file_path: str = "", as_file_name: str = ""):
        """
        Uploads a file to OneLake storage as a specific file name.
        """
        if not table_name:
            table_name = self.target_table_name
        if not local_file_path or not os.path.isfile(local_file_path):
            raise ValueError("Invalid local file path.")

        # Construct the folder path
        folder_path = f"{schema_name}.schema/{table_name}" if schema_name else f"{table_name}"

        try:
            # Get the directory client
            file_system_client = self.service_client.get_file_system_client(file_system="LandingZone")  # Replace with your file system name
            directory_client = file_system_client.get_directory_client(folder_path)

            # Check if the folder exists
            if not directory_client.exists():
                raise FileNotFoundError(f"Folder '{folder_path}' not found.")

            # Add an underscore to the file name for temporary upload
            temp_file_name = f"_{as_file_name}"

            # Upload the file
            file_client = directory_client.create_file(temp_file_name)
            with open(local_file_path, "rb") as file_data:
                file_contents = file_data.read()
                file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
                file_client.flush_data(len(file_contents))

            print(f"File uploaded successfully as '{temp_file_name}'.")

            # Python SDK doesn't handle rename properly for onelake, using REST API to rename the file instead
            self.rename_file_via_rest_api(f"LandingZone/{folder_path}", temp_file_name, as_file_name)
            print(f"File renamed successfully to '{as_file_name}'.")

        except Exception as e:
            raise Exception(f"Failed to upload data file: {e}")

if __name__ == "__main__":

    source_schema_name = "<source_schema_name>"
    source_table_name = "<source_table_name>"
    target_table_name = "<target_table_name>"
    fabric_app_client_id = "<fabric_app_client_id>"
    fabric_app_client_tenant = "<fabric_app_client_tenant>"
    fabric_app_client_secret = "<fabric_app_client_secret>"
    landing_zone_url = "<landing_zone_url>"
    target_table_metadata = {
        "KeyColumns": [
            # TODO
        ],
        "FirstRowAsHeader": True,
        "SchemaDefinition": {
            "Columns": [
                # TODO
            ]
        },
        "FileFormat": "CSV",
        "FileExtension": "csv",
        "FileFormatTypeProperties": {
            "FirstRowAsHeader": True,
            "RowSeparator": "\r\n",
            "ColumnSeparator": ",",
            "NullValue": "N/A",
            "Encoding": "UTF-8"
        }
    }

    client = OpenMirroringClient(
        client_id=fabric_app_client_id,
        client_secret=fabric_app_client_secret,
        client_tenant=fabric_app_client_tenant,
        host=landing_zone_url,
        table_metadata=target_table_metadata,
        target_table_name=target_table_name

    )

    parser = argparse.ArgumentParser(description="OpenMirroring Admin Operations")
    parser.add_argument("--get-table-status", action="store_true", help="Get the status of a table")
    parser.add_argument("--create-table", action="store_true", help="Create target table in mirrored database")
    parser.add_argument("--upload-data-file", action="store_true", help="Upload initial data to target table in mirrored database")
    parser.add_argument("--upload-data-file-as", action="store_true", help="Upload incremental data to target table in mirrored database as a specific file name")
    parser.add_argument("--remove-table", action="store_true", help="Drop table in mirrored database")

    parser.add_argument("--table-name", type=str, default=target_table_name, help="Name of the table")
    parser.add_argument("--local-file-path", type=str, default=None, help="Local file path for upload")
    parser.add_argument("--remove-schema-folder", action="store_true", help="Remove schema folder when dropping table")

    args = parser.parse_args()

    if args.get_table_status:
        client.get_table_status(table_name=args.table_name)

    if args.create_table:
        client.create_table_with_class_metadata(table_name=args.table_name)

    if args.upload_data_file:
        client.upload_data_file(local_file_path=args.local_file_path, table_name=args.table_name)

    if args.upload_data_file_as:
        client.upload_data_file_as(local_file_path=args.local_file_path, table_name=args.table_name, as_file_name=args.as_file_name)

    if args.remove_table:
        client.remove_table(table_name=args.table_name, remove_schema_folder=args.remove_schema_folder)
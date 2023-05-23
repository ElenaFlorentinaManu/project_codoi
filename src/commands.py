"""A module for the persistence layer"""

import sys
import typing as t
from src.database import DatabaseManager
from datetime import datetime
import json


db = DatabaseManager("forecasts_co2.db")

CommandInput = t.Optional[t.Union[t.Dict[str, str], int]]
CommandResult = t.Optional[t.Union[t.List[str], str]]

class Command(t.Protocol):
    """A protocol class that will be and example for implementing Commands"""

    def execute(self, data: CommandInput) -> CommandResult:
        """The actual execution of the command"""

        pass

class CreateForecastTableCommand:
    """A Command class that creates the SQL table of forecasts"""

    def execute(self):
        """The actual execution of the command"""

        db.create_table(
            table_name="forecasts",
            columns={
                "id": "integer primary key autoincrement",
                "number_of_container": "integer not null",
                "port_of_loading": "text not null",
                "port_of_destination": "text not null",
                "date_of_departure_port": "text not null",
                "due_date_plant": "text not null",
                "date_added": "text not null",
                },
        )

class CreatePortsTableCommand:
    """A Command class that creates the SQL table of forecasts"""

    def execute(self):
        """The actual execution of the command"""

        db.create_table(
            table_name="ports",
            columns={
                "id": "integer primary key autoincrement",
                "port": "text not null",
                "longitude": "text not null",
                "latitude": "text not null",
                },
        )

class AddForecastCommand:
    """A Command class that inserts into the SQL table forecasts"""

    def execute(self, data: t.Dict[str, str], timestamp: t.Optional[str] = None) -> str:
        """The actual execution of the command"""

        date_added = timestamp or datetime.utcnow().isoformat()
        data.setdefault("date_added", date_added)
        db.add(table_name="forecasts", data=data)
        return "Forecast added!"
    
class ListForecastCommand:
    """A Command class that will list all the forecast in the SQL table"""

    def __init__(self, order_by: str = "due_date_plant"):
        self.order_by = order_by

    def execute(self) -> t.List[str]:
        """The actual execution of the command"""

        cursor = db.select(table_name="forecasts", order_by=self.order_by)
        results = cursor.fetchall()
        return results
    
class DeleteForecastCommand:
    """A Command class that will delete a forecast from the SQL table"""

    def execute(self, data: int) -> str:
        db.delete(table_name="forecasts", criteria={"id": data})
        return "Forecast deleted!"
    
class InsertColumnsLocationPortsCommand: #add new columns
    """A Command class that creates in the SQL table "forecasts" new columns"""

    def execute(self):
        """The actual execution of the command"""
    
        # db.alter_table(
        #     table_name="forecasts",
        #     columns={
        #         "longitude_POL": "text",
        #         },
        #     )

        # db.alter_table(
        #     table_name="forecasts",
        #     columns={
        #         "latitude_POL": "text",
        #         },
        #     )
        
        # db.alter_table(
        #     table_name="forecasts",
        #     columns={
        #         "longitude_POL": "text",
        #         },
        #     )
        
        # db.alter_table(
        #     table_name="forecasts",
        #     columns={
        #         "latitude_POD": "text",
        #         },
        #     )
    
# class ImportGeolocationOfPortsCommand: 
#     """A command class that will take the geolocation from the json file and insert them in the table ""ports" the DB.
#     This command needs to be executed only on update of the source file."""

#     def execute(self) -> str:

#         with open("ports.json","rb") as file:
#             data = json.load(file)

#         curated_data = []
#         for port, port_data in data.items():
#             coordinates = port_data.get("coordinates", [0, 0])
#             longitude = coordinates[0]
#             latitude = coordinates[1]
#             current_entry = {
#                 "port": port,
#                 "longitude": longitude,
#                 "latitude": latitude
#             }
#             curated_data.append(current_entry)

#         for entry in curated_data:
#             db.add(table_name="ports", data=entry)

class GetPortLocationCommand:
    """A Command class that will add geolocation for ports in forecast"""

    def execute(self, data) -> t.List[str]:
        """The actual execution of the command"""

        cursor = db.select(table_name="ports", criteria={'port':data})
        result = cursor.fetchone()
        return result
    
class JoinTablesForecastsAndPorts:
    """A command Class that will join the 2 tables"""
    def execute(self, data):
        """The actual execution of the command"""

        results = db.join_tables(table_name_1 = "forecasts", column_1= {"port_of_loading":data}, table_name_2= "ports", column_2={"port":data})
        return results

class QuitCommand:
    """A Command class that will quit the application"""

    def execute(self):
        sys.exit()
from src import commands as c
from src import presentation as p

def loop():
    options = {
            "A": p.Option(
                name="Add a forecast",
                command=c.AddForecastCommand(),
                prep_call=p.get_new_forecasts
            ),
            "B": p.Option(name="List forecasts by date added", command=c.ListForecastCommand()),
            "T": p.Option(
                name="List forecasts by due date in plant",
                command=c.ListForecastCommand(order_by="due_date_plant"),
            ),
            "D": p.Option(
                name="Delete a forecast",
                command=c.DeleteForecastCommand(),
                prep_call=p.get_forecast_id
            ),
            "Q": p.Option(name="Quit", command=c.QuitCommand()),
        }

    p.clear_screen()
    p.print_options(options)
    chosen_option = p.get_option_choice(options)
    p.clear_screen()
    chosen_option.choose()

    _= input("Press ENTER to return to menu")

if __name__ == "__main__":
    c.CreateForecastTableCommand().execute()
    c.CreatePortsTableCommand().execute()
    

while True:
    loop()
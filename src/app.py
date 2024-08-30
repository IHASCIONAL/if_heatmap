from frontend import ExcelValidatorUI
from backend import ProcessDataController

controller = ProcessDataController()

def main():
    ui = ExcelValidatorUI()
    ui.display_header()

    upload_file = ui.upload_file()

    if upload_file:
        df, result, erros = controller.process_data(upload_file)
        ui.display_results(result, erros)

        if erros:
            ui.display_wrong_message()
            




if __name__ == "__main__":
    main()
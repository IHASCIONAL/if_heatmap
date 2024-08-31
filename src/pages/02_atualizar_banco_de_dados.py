from frontend.frontend import ExcelValidatorUI
from backend.backend import ProcessDataController, RefreshDataBase
import sentry_sdk

sentry_sdk.init(
    dsn="https://c1a0ce2c70a4f2376d6f2daefdcd21d2@o4507863466508288.ingest.us.sentry.io/4507863468670976",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

atualiza_banco = RefreshDataBase()
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
            sentry_sdk.capture_message("A planilha estava errada")

        elif ui.display_save_button():
            atualiza_banco.refresh_database(df)
            ui.display_success_message()

            sentry_sdk.capture_message("O banco SQL foi atualizado")
            




if __name__ == "__main__":
    main()

class Locators:
    # View
    SendFaxApplicationStackView = "#SendFaxAppApplicationStackView"
    CheckingForFaxSetupView = "#faxSetupViewMenuListListViewlist1"
    SendRecipientsView = "#faxSendRecipientsView"
    FaxNotConfiguredAlertView = "#faxNotConfiguredAlert"

    # Buttons
    FaxSetupSkipButton = "#faxSetupHomeViewSkipButton #ButtonControl"
    FaxSetupContinueButton = "#faxSetupHomeViewContinueButton #ButtonControl"
    FaxHomeButton = CheckingForFaxSetupView + "#BreadcrumbView #HomeButton #ButtonControl"
    FaxConfigureButton = "#faxConfigureButton #ButtonControl"
    FaxConfigureCancelButton = "#cancelButton #ButtonControl"
    FaxConfirmCancelButton = "#faxCancelSetupYesButton #ButtonControl"
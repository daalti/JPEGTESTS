class ProSelectUIObjectIds:
    # Utilities
    OobeCountryRegionPrefix = "#cCountryRegion"

    # Views
    homeScreenView = "#HomeScreenView"
    ToastMessageView = "#ToastSystemToastStackView"
    PrinterUserView = "#DeviceUserView"
    EnterUserNameView = "#EnterUserNameView"
    SignInView = '#AnaUiServiceServiceStackView'
    SignInDescriptionView = SignInView + " #DescriptiveButtonListLayout"
    TumblerView = "#Tumbler #KeyPathView"
    AdminPasswordRequiredView = "#adminPwReqView"
    OobeDeviceLanguageView = "#DeviceLanguageView"
    OobeMessageLayoutView = "#MessageLayout"
    OobeCountryRegionView = "#OobeCountryRegionView"
    OobeMoreLocationsView = "#MoreCountriesRegionsView"
    OobeNetworkSettingsView = "#OOBENetworkSettingsView"
    OobeProxySettingsView = "#ProxySettingsView"
    OobeSharePrinterAnalyticsView = "#OobeSharePrinterAnalytics"
    OobeFirmwareUpdateView = "#cfuInfo"
    OobeFirmwareUpdateErrorView = "#CriticalFwUpdate"
    OobeInstallDriversView = "#OobeInstallDriversView"
    reportsAppView = "#ReportAppApplicationStackView"

    # Text
    CurrentAppText = "#CurrentAppText"
    ToastMessageText = ToastMessageView + " #ToastInfoText"

    # Buttons
    PrinterUserNameButton = SignInDescriptionView + " #enterUsernameButtonUser #SpiceButton"
    PrinterUserPasswordButton = SignInDescriptionView + " #enterPasswordButtonUser #SpiceButton"
    KeyboardButton = "#spiceKeyboardView #MouseArea"
    HybridKeyboardBackspaceButton = "#SpiceKeyBoardbutton_ba"
    HybridKeyboardEnterButton = "#SpiceKeyBoardbutton_en"
    KeyboardBackspaceButton = "#ItemIconDelegatebackspace_xs"
    KeyboardEnterButton = "#ItemIconDelegatecheckmark_xs"
    SignInOkButton = "#signInOkButton"
    SignInCancelButton = "#signInCancelButton"
    HomeSignInButton = "#7db992ba-557a-461c-b941-6023aa8cfa34 MouseArea"
    invalidSignInView = "#AgentNotAuthenticatedView"
    invalidSignInOkButton = "#failedOkButton #SpiceButton"
    AdminPasswordRequiredOkButton = AdminPasswordRequiredView + " #adminPwReqOkButton #SpiceButton"
    OobeConfirmLanguageButton = "#confirmLanguageButton"
    OobeMoreLocationsButton = "#MoreCountryRegionSettingsButton"
    OobeNetworkContinueButton = "#NetworkContinueButton"
    OobeProxySettingsSkipButton = "#SkipProxyButton"
    OobeSharePrinterAnalyticsNoButton = "#NoButton"
    OobeSharePrinterAnalyticsYesButton = "#YesButton"
    OobeFirmwareUpdateOptionsView = "#AutoPrinterUpdateMessageScreen"
    OobeFirmwareUpdateOptionsAutoButton = "#AutoButton"
    OobeFirmwareUpdateContinueButton = "#continueButton"
    OobeFirmwareUpdateCancelButton = "#Cancel"
    OobeFirmwareUpdateErrorSkipButton = "#SkipButton"
    OobeInstallDriversContinueButton = "#DriversContinueButton"
    statusReportButton = "#reportStatusWithoutDependenciesMenuButton"
    usageReportButton = "#checkboxMenuEntry_report_usageReport"
    SigningInCancelButton = "#SigningInView #Cancel #SpiceButton"
    SignInBackButton = "#BackButton #SpiceButton"

    # Input Fields
    HybridKeyboardTextInputArea = "#hybridKeyboardTextInputArea"

    # Scroll Bars
    SignInPageScrollBar = "#baseViewScrollBar"

    # SignInApp
    SignInUsernameConfirmButton = "#ConfirmButton"
    SignInUsernameCancelButton = "#CancelButton"

    # Sign In Authentication Agents
    PrinterUser = "User"
    Windows = "Windows"
    Ldap = "Ldap"
    Admin = "Admin"

    # Tray Settings
    traySettingsSizeTypePromptDisplay = "#display"
    traySettingsSizeTypePromptDoNotDisplay = "#doNotDisplay"
    traySettingsPaperOutTimeoutNone = "#none"
    traySettingsPaperOutTimeoutImmediate = "#immediate"
    menu_button_settings_tray_Alternative_Letter_Head_Mode = "#alternativeLetterHeadModeMenuSwitch"
    menu_button_settings_tray_Alternative_Letter_Head_Mode_setting_switch = "#alternativeLetterHeadModeSettingsSwitch"
    menu_tray_settings_list = "#MenuListtraySettings"

    # Views
    PrinterUserNameView = "#SpiceView"
    AdminPasswordView = "#LocalUserPasswordView"
    ConfirmView = "#MessageLayout"
    WindowsView = "#WindowsView MouseArea"
    LDAPView = "#LdapView MouseArea"
    AdminView = "#LocalAdminView MouseArea"

    # Text
    SignInMethodText = SignInDescriptionView + " #Header #Version1Text"

    # Text Box
    UserNameTextInputBox = EnterUserNameView + " #TextInputArea #TextInputBox"
    PrinterUserNameTextInputBox = PrinterUserNameView + " #TextInputArea #TextInputBox"
    PrinterUserPasswordTextInputBox = AdminPasswordView + " #TextInputArea #TextInputBox"

    # Button
    WindowsUserNameButton = SignInDescriptionView + " #enterUsernameButtonWindows #SpiceButton"
    WindowsPasswordButton = SignInDescriptionView + " #enterPasswordButtonWindows #SpiceButton"
    LdapUserNameButton = SignInDescriptionView + " #enterUsernameButtonLdap #SpiceButton"
    LdapPasswordButton = SignInDescriptionView + " #enterPasswordButtonLdap #SpiceButton"
    LdapSignInOkButton = "#signInOkButtonLdap #SpiceButton"
    AdminPasswordButton = SignInDescriptionView + " #localAdminPasswordButton #SpiceButton"
    AdminSignInOkButton = "#localAdminOkButton #SpiceButton"
    PrinterUserNameButton = SignInDescriptionView + " #enterUsernameButtonUser #SpiceButton"
    PrinterUserPasswordButton = SignInDescriptionView + " #enterPasswordButtonUser #SpiceButton"
    PrinterUserSignInOkButton = "#signInOkButtonUser #SpiceButton"
    WindowsSignInOkButton = "#signInOkButtonWindows #SpiceButton"
    ConfrimOkButton = "#ConfirmButton #SpiceButton"
    ConfirmCancelButton = "#CancelButton #SpiceButton"
    SignInMethodButton = SignInDescriptionView + " #signinMethodButtonUser #SpiceButton"
    cancel_button = "#cancelButton"
    # Scroll Bar
    SignInScrollbar = "#baseViewScrollBar"

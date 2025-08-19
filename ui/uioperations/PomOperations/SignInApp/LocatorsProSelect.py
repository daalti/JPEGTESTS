class LocatorsProSelect:
    # Views
    HomeScreenView = "#HomeScreenView"
    SignInView = '#AnaUiServiceServiceStackView'
    SignInDescriptionView = SignInView + " #DescriptiveButtonListLayout"
    EnterUserNameView = "#EnterUserNameView"
    PrinterUserNameView = "#SpiceView"
    PasswordView = "#NetworkUserPasswordView"
    AdminPasswordView = "#LocalUserPasswordView"
    PrinterUserView = "#DeviceUserView MouseArea"
    SignInScrollArea = SignInView + " #DescriptiveButtonListLayout"
    TumblerView = "#Tumbler #KeyPathView"
    ConfirmView = "#MessageLayout"
    WindowsView = "#WindowsView MouseArea"
    LDAPView = "#LdapView MouseArea"
    AdminView = "#LocalAdminView MouseArea"

    # Text
    HomeScreenCurrentAppText = "#CurrentAppText"
    SignInMethodText = SignInDescriptionView + " #Header #Version1Text"
    ToastMessageText = "#ToastSystemToastStackView #ToastInfoText"

    # Text Box
    UserNameTextInputBox = EnterUserNameView + " #TextInputArea #TextInputBox"
    PrinterUserNameTextInputBox = PrinterUserNameView + " #TextInputArea #TextInputBox"
    PrinterUserPasswordTextInputBox = AdminPasswordView + " #TextInputArea #TextInputBox"

    # Button
    SignInButton = "#7db992ba-557a-461c-b941-6023aa8cfa34 MouseArea"
    WindowsUserNameButton = SignInDescriptionView + " #enterUsernameButtonWindows #SpiceButton"
    WindowsPasswordButton = SignInDescriptionView + " #enterPasswordButtonWindows #SpiceButton"
    LdapUserNameButton = SignInDescriptionView + " #enterUsernameButtonLdap #SpiceButton"
    LdapPasswordButton = SignInDescriptionView + " #enterPasswordButtonLdap #SpiceButton"
    LdapSignInOkButton = "#signInOkButtonLdap #SpiceButton"
    AdminPasswordButton = SignInDescriptionView + " #localAdminPasswordButton #SpiceButton"
    AdminSignInOkButton = "#localAdminOkButton #SpiceButton"
    PrinterUserNameButton = SignInDescriptionView + " #enterUsernameButtonUser #SpiceButton"
    PrinterUserPasswordButton = SignInDescriptionView + " #enterPasswordButtonUser #SpiceButton"
    KeyboardButton = "#spiceKeyboardView #MouseArea"
    PrinterUserSignInOkButton = "#signInOkButtonUser #SpiceButton"
    WindowsSignInOkButton = "#signInOkButtonWindows #SpiceButton"
    ConfrimOkButton = "#ConfirmButton #SpiceButton"
    ConfirmCancelButton = "#CancelButton #SpiceButton"
    SignInMethodButton = SignInDescriptionView + " #signinMethodButtonUser #SpiceButton"

    # Scroll Bar
    SignInScrollbar = "#baseViewScrollBar"
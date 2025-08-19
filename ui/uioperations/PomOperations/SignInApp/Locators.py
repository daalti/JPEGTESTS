class Locators:
    # Properties
    DisplayText = 'displayText'

    # Views
    SignInView = '#AnaUiServiceServiceStackView'
    SignInViewInvalid = '#notAuthetnicatedView'
    WelcomeUserView = "#welcomeUserView"
    
    WindowsSignInSingleDomainView = "#loginWindowsSingleDomainView"
    WindowsSignInMultipleDomainsView = "#loginWindowsMultipleDomainView"
    ServiceUserSignInView = "#loginServiceUserView"
    SmartcardSignInView = '#loginSmartCardView'
    PrinterUserSignInView = "#loginUserView"
    AdminSignInView = "#loginAdminView"
    LdapSignInView = "#loginLDAPView"
    IDCodeSignInView = "#loginIdentificationCodeView"

    AllSignInViews = [SmartcardSignInView, PrinterUserSignInView, AdminSignInView, ServiceUserSignInView,
     WindowsSignInSingleDomainView, WindowsSignInMultipleDomainsView, LdapSignInView]

    ToastMessageView = "#ToastWindowToastStackView"
    SmartcardProblemView = "#notRecognizedErrorView"
    ConstraintMessageErrorPageTextView = "#ConstraintMessage #constraintDescription SpiceText[visible=true]"
    SmartcardLockedView = "#pinLockedErrorView"
    KeyboardView = "#spiceKeyboardView"

    AdminSignInViewLayout = "#loginAdminView #bodyLayoutverticalLayout"
    IDCodeSignInViewLayout = "#loginIdentificationCodeView #bodyLayoutverticalLayout"
    LdapSignInViewLayout = "#loginLDAPView #bodyLayoutverticalLayout"
    PrinterUserSignInViewLayout = "#loginUserView #bodyLayoutverticalLayout"
    WindowsMultipleDomainViewLayout = "#loginWindowsMultipleDomainView #bodyLayoutverticalLayout"

    # Combo Boxes
    PopupListSuffix = "popupList"

    SmartcardSignInComboBox = '#smartCardSigninInComboBox'
    SmartcardDomainComboBox = '#smartCardDomainComboBox'
    SmartCardDomainTextField = "#smartCardDomainTextField"

    ServiceUserSignInComboBox = '#serviceUserSignInComboBox'
    PrinterUserSignInComboBox = '#userSignInComboBox'
    IDCodeSignInComboBox = '#identificationCodeSigninInComboBox'
    WindowsSignInComboBox = '#windowsSignInComboBox'
    WindowsDomainComboBox = 'NO OBJECT NAME'
    AdminSignInComboBox = '#adminSigninInComboBox'
    LdapSignInComboBox = '#ldapSignInComboBox'

    # Combo Box Items
    ServiceUserComboBoxItemSuffix = '_serviceTech'
    PrinterUserComboBoxItemSuffix = '_deviceUser'
    IDCodeComboBoxItemSuffix = '_identificationCode'
    SmartcardComboBoxItemSuffix = '_smartCard'
    WindowsComboBoxItemSuffix = '_windows'
    AdminComboBoxItemSuffix = '_admin'
    LdapComboBoxItemSuffix = '_ldap'

    ServiceUserSignInComboBoxItemPrefix = '#serviceUserSignInComboBoxItem'
    SmartcardSignInComboBoxItemPrefix = '#smartCardSignInComboBoxItem'
    PrinterUserSignInComboBoxItemPrefix = '#userSignInComboBoxItem'
    IDCodeSignInComboBoxItemPrefix = "#identificationCodeSignInComboBoxItem"
    WindowsSignInComboBoxItemPrefix = '#windowsSignInComboBoxItem'
    AdminSignInComboBoxItemPrefix = '#adminSignInComboBoxItem'
    LdapSignInComboBoxItemPrefix = '#ldapSignInComboBoxItem'

    # Scroll Bars
    ComboBoxScrollBar = "#comboBoxScrollBar"
    AdminSignInScrollBar = "#loginAdminView #bodyLayoutverticalLayout #bodyLayoutverticalLayoutScrollBar"
    IDCodeSignInScrollBar = "#loginIdentificationCodeView #bodyLayoutverticalLayout #bodyLayoutverticalLayoutScrollBar"
    LdapSignInScrollBar = "#loginLDAPView #bodyLayoutverticalLayout #bodyLayoutverticalLayoutScrollBar"
    PrinterUserSignInScrollBar = "#loginUserView #bodyLayoutverticalLayout #bodyLayoutverticalLayoutScrollBar"
    WindowsMultipleDomainSignInScrollBar = "#loginWindowsMultipleDomainView #bodyLayoutverticalLayout #bodyLayoutverticalLayoutScrollBar"

    # Footer
    FooterRectangle = "#footer #footerRectangle"

    # Fields
    SmartcardDomainTextField = '#smartCardDomainTextField'
    SmartcardPinInput = "#smartCardPinInputField"
    SmartcardPinInputField = '#smartCardPinInputField #TextInputBox'
    SmartcardPinInputFieldClickable = '#smartCardPinInputField #ButtonControl'
    SmartcardPinInputFieldContainer = '#smartCardPinInputField #textFieldContainer'
    WindowsUsernameInputField = '#windowsUsernameInputField #TextInputBox'
    WindowsPasswordInput = "#windowsPasswordInputField"
    WindowsPasswordInputField = '#windowsPasswordInputField #TextInputBox'
    AdminPasswordInput = "#adminPasswordInputField"
    AdminPasswordInputField = '#adminPasswordInputField #TextInputBox'
    SmartcardConstraintTextField = '#loginSmartCardView #smartCardConstraintTextField'
    LdapUsernameInputField = "#ldapUsernameInputField #TextInputBox"
    LdapPasswordInput = "#ldapPasswordInputField"
    LdapPasswordInputField = "#ldapPasswordInputField #TextInputBox"
    PrinterUserUsernameInputField = "#userUsernameInputField #TextInputBox"
    PrinterUserPasswordInput = "#userPasswordInputField"
    PrinterUserPasswordInputField = "#userPasswordInputField #TextInputBox"
    ServiceUserPasswordInputField = "#serviceUserPasswordInputField #TextInputBox"
    IDCodePasswordInput = "#identificationCodePinInputField"
    IDCodePasswordInputField = "#identificationCodePinInputField #TextInputBox"

    # Buttons
    InvalidSignInButton = '#notAuthenticatedSignInButton #ButtonControl'
    SmartcardSignInButton = '#smartCardSignInButton #ButtonControl'
    SmartcardCancelButton = '#smartCardCancelButton #ButtonControl'
    WindowsSignInButton = '#windowsSignInButton #ButtonControl'
    WindowsCancelButton = '#windowsCancelButton #ButtonControl'
    AdminSignInButton = '#adminSignInButton #ButtonControl'
    AdminCancelButton = '#adminCancelButton #ButtonControl'
    SigningInCancelButton = "#signingInCancelButton #ButtonControl"
    SmartcardProblemOkButton = SmartcardProblemView + " #notRecognizedErrorOkButton #ButtonControl"
    ConstraintMessageErrorPageOkButton = "#ConstraintMessage #FooterView #okButton #ButtonControl"
    MultipleReadersAttachedOkButton = "#multipleCardReaderErrorOkButton #ButtonControl"
    SmartcardLockedOkButton = "#pinLockedErrorOkButton #ButtonControl"
    LdapSignInButton = "#ldapSignInButton #ButtonControl"
    LdapCancelButton = "#ldapCancelButton #ButtonControl"
    PrinterUserSignInButton = "#userSignInButton #ButtonControl"
    PrinterUserCancelButton = "#userCancelButton #ButtonControl"
    ServiceUserSignInButton = "#serviceUserSignInButton #ButtonControl"
    ServiceUserCancelButton = "#serviceUserCancelButton #ButtonControl"
    ServiceUserInvalidSignInButton = '#OK #ButtonControl'
    IDCodeUserSignInButton = "#identificationCodeSignInButton #ButtonControl"
    IDCodeUserCancelButton = "#identificationCodeCancelButton #ButtonControl"
    RevealIcon = "#RevealIcon"
    RevealIconButton = "#RevealIcon #EyeMouseArea"
    SmartcardPinInputRevealIconButton = "#smartCardPinInputField " + RevealIconButton
    WindowsPasswordInputRevealIconButton = "#windowsPasswordInputField " + RevealIconButton
    LdapPasswordInputRevealIconButton = "#ldapPasswordInputField " + RevealIconButton
    AdminPasswordInputRevealIconButton = "#adminPasswordInputField " + RevealIconButton
    PrinterUserPasswordInputRevealIconButton = "#userPasswordInputField " + RevealIconButton
    IDCodePinInputRevealIconButton = "#identificationCodePinInputField " + RevealIconButton

    # Text
    ToastMessageText = ToastMessageView + " SpiceText[visible=true]"
    SmartcardConstraintTextFieldText = SmartcardConstraintTextField
    KeypadEnterTextView = KeyboardView + " #enterKeyPositiveIntegerKeypad SpiceText[visible=true]" # Clickable
    KeyboardEnterTextView = KeyboardView + " #enterKey1 SpiceText[visible=true]"        # Clickable
    
    # Numeric Keypad
    KeypadIntegerEnter = KeyboardView + " #enterKeyIntegerKeypad"
    KeypadInteger0 = KeyboardView + " #key0IntegerKeypad"
    KeypadInteger1 = KeyboardView + " #key1IntegerKeypad"
    KeypadInteger2 = KeyboardView + " #key2IntegerKeypad"
    KeypadInteger3 = KeyboardView + " #key3IntegerKeypad"
    KeypadInteger4 = KeyboardView + " #key4IntegerKeypad"
    KeypadInteger5 = KeyboardView + " #key5IntegerKeypad"
    KeypadInteger6 = KeyboardView + " #key6IntegerKeypad"
    KeypadInteger7 = KeyboardView + " #key7IntegerKeypad"
    KeypadInteger8 = KeyboardView + " #key8IntegerKeypad"
    KeypadInteger9 = KeyboardView + " #key9IntegerKeypad"
    

    SmartcardDetectedToastMessage = "SmartCard detected"
    SmartcardReaderDetectedToastMessage = "SmartCard reader detected"
    SmartcardConstraintNoReaderMessage = "Connect a SmartCard reader to the printer, and then insert the card."
    SmartcardConstraintNoCardInsertedMessage = "Please insert your SmartCard into the reader."
    SmartcardErrorPageNoReaderMessage = "No SmartCard reader detected. Connect a reader to the printer or contact the administrator."
    SmartcardErrorPageNoSmartcardMessage = "No SmartCard detected. Insert your SmartCard into the reader and retry signing in."
    SmartcardErrorPageMultipleReadersMessage = "Multiple SmartCard readers are connected to the printer."
    
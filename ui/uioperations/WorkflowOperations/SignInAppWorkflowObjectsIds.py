class SignInAppWorkflowObjectIds:

    comboBoxScrollBar = '#comboBoxScrollBar'

    # Views
    homeScreenView = '#HomeScreenView'
    home_swipe_view = '#homeScreenSwipeView'
    invalidSignInView = '#notAuthetnicatedView'
    signinView = '#signingInView'
    welcome_user_view = '#welcomeUserView'
    blank_creds_view = '#ConstraintMessage'
    confirm_sign_out_view = '#confirmSignOutView'
    signInStackView = '#AnaUiServiceServiceStackView'

    # Buttons
    sign_in = '#statusCenterServiceStackView #actionRow #StatusButtonSignIn #ButtonControl'
    sign_out = '#statusCenterServiceStackView #actionRow #StatusButtonSignOut #ButtonControl'
    confirmSignOutYesButton = '#confirmSignOutView #confirmSignOutFooter #confirmSignOutYesButton #ButtonControl'
    confirmSignOutNoButton = '#confirmSignOutView #confirmSignOutFooter #confirmSignOutNoButton #ButtonControl'
    menu_item_signinid = '#7db992ba-557a-461c-b941-6023aa8cfa34'
    sign_in_button = menu_item_signinid + ' #launcherButton'
    sign_in_label = menu_item_signinid + ' #labelText'
    cancel_button = '#cancelButton'
    invalidSignInButton = '#notAuthenticatedSignInButton'
    signingInCancelButton  = '#signingInCancelButton'
    blankCredsButton = '#okButton'
    confirm_sign_out_yes = '#confirmSignOutView #confirmSignOutYesButton'
    confirm_sign_out_no = '#confirmSignOutView #confirmSignOutNoButton'
    revealIcon = '#RevealIcon'
    revealIconButton = revealIcon + ' #EyeMouseArea #ButtonControl'

    # Suffixes and Prefixes for combo box and selections
    prefix_windows = '#windows'
    prefix_ldap = '#ldap'
    prefix_admin = '#admin'
    prefix_user = '#user'
    prefix_service = '#service'
    prefix_service_user = '#serviceUser'
    prefix_identification_code = '#identificationCode'
    prefix_smartcard = '#smartCard'

    suffix_signindropdown = 'SignInComboBox'
    suffix_windowsSelect = 'SignInComboBoxItem_windows'
    suffix_ldapSelect = 'SignInComboBoxItem_ldap'
    suffix_adminSelect = 'SignInComboBoxItem_admin'
    suffix_userSelect = 'SignInComboBoxItem_deviceUser'
    suffix_serviceSelect = 'SignInComboBoxItem_serviceTech'
    suffix_identificationCodeSelect = 'SignInComboBoxItem_identificationCode'
    suffix_smartcardSelect = 'SignInComboBoxItem_smartCard'

    suffix_usernameinputfield = 'UsernameInputField'
    suffix_passwordinputfield = 'PasswordInputField'
    suffix_pininputfield = 'PinInputField'
    suffix_signinbutton = 'SignInButton'
    suffix_domain_field = 'DomainTextField'
    suffix_domain_combo_box = 'DomainComboBox'

    suffix_cancelbutton = 'CancelButton'
    prefix_login_view = '#login'
    suffix_login_view = 'View'

    popup_list = "popupList"

    #Persistent Header
    userInfoView = '#userInfoView'
    userInfoInitial = userInfoView + ' #initials'
    userInfoUsername = userInfoView + ' #username'
    userInfoEmail = userInfoView + ' #email'
    userInfoSwitchAccountButton = userInfoView + ' #userInfoFooter #userInfoCancelButton #ButtonControl'
    userInfoCloseButton = userInfoView + ' #userInfoHeader #userInfoCloseButton #ButtonControl'
    userInfoSignOutButton = userInfoView + ' #userInfoFooter #userInfoSignInButton #ButtonControl'
    userInitials = '#userInitials'

    #Toast Messages
    toastMessageView = '#ToastWindowToastStackView'
    toastMessageText = toastMessageView + ' SpiceText[visible=true]'

    # Device Administrator
    adminLoginView = '#loginAdminView'
    adminLoginViewLayout = adminLoginView + ' #bodyLayoutverticalLayout'
    adminSignInComboBox = '#adminSigninInComboBox'
    adminPasswordInputField = '#adminPasswordInputField'
    adminPasswordInputFieldTextInputBox = adminPasswordInputField + ' #TextInputBox'
    adminSignInButtonControl = '#adminSignInButton #ButtonControl'
    adminPasswordInputRevealIconButton = '#adminPasswordInputField ' + revealIconButton
    adminCancelButtonControl = '#adminCancelButton #ButtonControl'
    adminPasswordRequiredView = '#adminPwReqView'
    adminPasswordRequiredOkButton = adminPasswordRequiredView + ' #FooterViewRight #adminPwReqOkButton #ButtonControl'
    adminSignInScrollBar = adminLoginViewLayout + ' #bodyLayoutverticalLayoutScrollBar'
    adminSignInFooter = adminLoginView + ' #adminFooter'

    # Printer User
    printerUserLoginView = '#loginUserView'
    printerUserLoginViewLayout = printerUserLoginView + ' #bodyLayoutverticalLayout'
    printerUserSignInComboBox = '#userSignInComboBox'
    printerUserUsernameInputField = '#userUsernameInputField'
    printerUserUsernameInputFieldTextInputBox = printerUserUsernameInputField + ' #TextInputBox'
    printerUserPasswordInputField = '#userPasswordInputField'
    printerUserPasswordInputFieldTextInputBox = printerUserPasswordInputField + ' #TextInputBox'
    printerUserSignInButtonControl = '#userSignInButton #ButtonControl'
    printerUserCancelButtonControl = '#userCancelButton #ButtonControl'
    printerUserPasswordInputRevealIconButton = '#userPasswordInputField ' + revealIconButton
    printerUserSignInScrollBar = printerUserLoginViewLayout + ' #bodyLayoutverticalLayoutScrollBar'
    serviceuserSelect = '#userSignInComboBoxItem_serviceTech'
    printerUserSignInFooter = printerUserLoginView + ' #userFooter'

    #IDCodes
    idCodeLoginView = '#loginIdentificationCodeView'
    idCodeLoginViewLayout = idCodeLoginView + ' #bodyLayoutverticalLayout'
    idCodeSignInComboBox = '#identificationCodeSignInComboBox'
    idCodePinInputField = '#identificationCodePinInputField'
    idCodePinInputFieldTextInputBox = idCodePinInputField + ' #TextInputBox'
    idCodePinInputRevealIconButton = idCodePinInputField + ' RevealIconButton'
    idCodeSignInScrollBar = idCodeLoginViewLayout + ' #bodyLayoutverticalLayoutScrollBar'
    idCodeSignInButtonControl = '#identificationCodeSignInButton #ButtonControl'
    idCodeCancelButtonControl = '#identificationCodeCancelButton #ButtonControl'
    idCodeSignInFooter = idCodeLoginView + ' #identificationCodeFooter'

    #Service User
    serviceUserLoginView = '#loginServiceUserView'
    serviceUserLoginViewLayout = serviceUserLoginView + ' #bodyLayoutverticalLayout'
    serviceUserSignInComboBox = '#serviceSignInComboBox'
    serviceUserPasswordInputFieldText = '#serviceUserPasswordInputField'
    serviceUserPasswordInputFieldTextInputBox = serviceUserPasswordInputFieldText + ' #TextInputBox'
    serviceUserPasswordInputRevealIconButton = '#windowsPasswordInputField ' + revealIconButton
    serviceUserSignInButtonControl = '#serviceUserSignInButton #ButtonControl'
    serviceUserCancelButtonControl = '#serviceUserCancelButton #ButtonControl'
    serviceUserMenuAccessItem = '#informationMenuMenuButton'
    serviceUserSignInFooter = serviceUserLoginView + ' #userFooter'

    #Windows Multi-Demensional Functionality:
    windowsLoginView_base = '#loginWindowsView'
    windowsSingleDomainView = '#loginWindowsSingleDomainView'
    windowsMultipleDomainView = '#loginWindowsMultipleDomainView'
    windowsUserSignInFooter_MultiDimensional = '{} #windowsFooter'
    windowsLoginViewLayout_MultiDimensional = '{} #bodyLayoutverticalLayout'
    windowsSignInScrollBar_MultiDimensional = '{} #bodyLayoutverticalLayout #bodyLayoutverticalLayoutScrollBar'
    #Windows remaining:
    windowsSignInComboBox = '#windowsSignInComboBox'
    windowsUsernameInputField = '#windowsUsernameInputField'
    windowsUsernameInputFieldTextInputBox = windowsUsernameInputField + ' #TextInputBox'
    windowsPasswordInputField = '#windowsPasswordInputField'
    windowsPasswordInputFieldTextInputBox = windowsPasswordInputField  + ' #TextInputBox'
    windowsSignInButtonControl = '#windowsSignInButton #ButtonControl'
    windowsCancelButtonControl = '#windowsCancelButton #ButtonControl'
    windowsPasswordInputRevealIconButton = '#windowsPasswordInputField ' + revealIconButton
    windowsDomainComboBox = prefix_windows + suffix_domain_combo_box
    windowsDomainField = prefix_windows + suffix_domain_field

    # LDAP
    ldapLoginView = '#loginLdapView'
    ldapLoginViewLayout = ldapLoginView + ' #bodyLayoutverticalLayout'
    ldapSignInComboBox = '#ldapSignInComboBox'
    ldapUsernameInputField = '#ldapUsernameInputField'
    ldapUsernameInputFieldInputTextBox = ldapUsernameInputField + ' #TextInputBox'
    ldapPasswordInputField = '#ldapPasswordInputField'
    ldapPasswordInputFieldTextInputBox = ldapPasswordInputField + ' #TextInputBox'
    ldapPasswordInputRevealIconButton = '#ldapPasswordInputField ' + revealIconButton
    ldapSignInScrollBar = ldapLoginViewLayout + ' #bodyLayoutverticalLayoutScrollBar'
    ldapSignInButtonControl = '#ldapSignInButton #ButtonControl'
    ldapCancelButtonControl = '#ldapCancelButton #ButtonControl'
    ldapUserSignInFooter = ldapLoginView + ' #ldapFooter'

    #SmartCard
    smartcardLoginView = '#loginSmartCardView'
    smartcardMultipleDomainView = '#loginSmartCardMultipleDomainView'
    smartcardLoginViewLayout = smartcardLoginView + ' #bodyLayoutverticalLayout'
    smartcardSignInComboBox = '#smartcardSignInComboBox'
    smartCardPinInputField = '#smartCardPinInputField'
    smartcardPinInputFieldTextInputBox = smartCardPinInputField + ' #TextInputBox'
    smartcardPinInputRevealIconButton = smartCardPinInputField + revealIconButton
    smartcardSignInScrollBar = smartcardLoginViewLayout + ' #bodyLayoutverticalLayoutScrollBar'
    smartcardConstraintTextField = '#loginSmartCardView #smartCardConstraintTextField'
    smartcardPinInputFieldClickable = smartCardPinInputField + ' #ButtonControl'
    smartcardPinInputFieldContainer = smartCardPinInputField + ' #textFieldContainer'
    smartcardDomainTextField = '#smartCardDomainTextField'
    smartcardDomainComboBox = prefix_smartcard + suffix_domain_combo_box
    smartcardSingleDomainText = smartcardDomainComboBox + ' #control #itemContainerTextImage #textColumn #contentItem'
    smartCardDomainField = prefix_smartcard + suffix_domain_field
    smartcardSignInButtonControl = prefix_smartcard + suffix_signinbutton + ' #ButtonControl'
    smartcardCancelButtonControl = smartcardLoginView + ' #smartCardCancelButton #ButtonControl'
    smartcardUserSignInFooter = smartcardLoginView + ' #smartCardFooter'

    AllSignInViews = [smartcardLoginView, printerUserLoginView, adminLoginView, serviceUserLoginView,
    windowsLoginView_base, ldapLoginView]

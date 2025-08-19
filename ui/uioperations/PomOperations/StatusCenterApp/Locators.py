from enum import Enum

class Locators:
    # States
    class StatusCenterState(str, Enum):
        Collapsed = "COLLAPSED"
        Expanded = "EXPANDED"

    # Views
    NotificationCenterView = "NotificationCenterView"
    ConfirmSignOutView = "#confirmSignOutView"

    ClickableStatusCenterBar = NotificationCenterView + " #footer"
    ClickableStatusCenterRectangleBar = ClickableStatusCenterBar + " #footerRectangle"

    # Buttons
    SignInButton = "#StatusButtonSignIn #ButtonControl"
    SignOutButton = "#StatusButtonSignOut #ButtonControl"
    ConfirmSignOutYesButton = "#confirmSignOutYesButton #ButtonControl"
    ConfirmSignOutNoButton = "#confirmSignOutNoButton #ButtonControl"

    # Text
    WantProceedText = "#wantProceedSpiceText"
    SignOutWarningText = "#signingOutSpiceText"
    SignInButtonText = "#StatusSignIn"
    SignOutButtonText = "#StatusSignOut"
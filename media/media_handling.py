# file: dunetuf/media/media_handling/media_handling.py

import logging
from typing import Any, Dict, Type, cast
from typing_extensions import Self  # type: ignore

from dunetuf.metadata import get_ip
from dunetuf.udw.udw import get_underware_instance
from dunetuf.cdm import get_cdm_instance
from dunetuf.control.targetdevice import TargetPlatform, device_instance

class MediaHandling:
    """
    Base class for Media Handling CDM operations.
    Dispatches to platform-specific subclasses based on the target device.
    """

    def __new__(cls: Type[Self], *args: Any, **kwargs: Any) -> Self:
        if cls is MediaHandling:
            cls.ip_address = get_ip()
            cls._udw = get_underware_instance(ip=cls.ip_address)
            cls._cdm = get_cdm_instance(addr=cls.ip_address, udw=cls._udw)
            cls._target_platform = device_instance().target_platform

            if cls._target_platform == TargetPlatform.DUNE:
                from dunetuf.media.dune.media_handing_dune import MediaHandlingDune
                return cast(Self, MediaHandlingDune(*args, **kwargs))
            elif cls._target_platform == TargetPlatform.ARES:
                from dunetuf.media.ares.media_handling_ares import MediaHandlingAres
                return cast(Self, MediaHandlingAres(*args, **kwargs))
            else:
                raise NotImplementedError(
                    "Platform {cls._target_platform} not supported for MediaHandling"
                )
        return cast(Self, super().__new__(cls))

    def get_alerts(self) -> Dict[str, Any]:
        """
        GET cdm/mediaHandling/v1/alerts
        Retrieve the list of current media handling alerts.
        """
        raise NotImplementedError("The method get_alerts() must be implemented in the subclass")

    def put_alert_action(self, alert_id: str, action: str) -> None:
        """
        PUT cdm/mediaHandling/v1/alerts/{alertId}/action
        Send a user action for a specific alert.

        Args:
            alert_id: Identifier of the alert to act upon.
            action: Action string (e.g., 'ok', 'cancel', 'modify').
        """
        raise NotImplementedError("The method put_alert_action() must be implemented in the subclass")

    def get_configuration(self) -> Dict[str, Any]:
        """
        GET cdm/mediaHandling/v1/configuration
        Retrieve the current media handling configuration.
        """
        raise NotImplementedError("The method get_configuration() must be implemented in the subclass")

    def update_configuration(self, payload: Dict[str, Any]) -> None:
        """
        PATCH cdm/mediaHandling/v1/configuration
        Apply a partial update to the media handling configuration.

        Args:
            payload: Dictionary of configuration fields to update.
        """
        raise NotImplementedError("The method update_configuration() must be implemented in the subclass")

    def get_capabilities(self) -> Dict[str, Any]:
        """
        GET cdm/mediaHandling/v1/capabilities
        Retrieve the media handling capabilities supported by the device.
        """
        raise NotImplementedError("The method get_capabilities() must be implemented in the subclass")
    
    def wait_for_alerts(self, category='any', timeout=15):
        """Wait until a specific category of media alert is observed."""
        
        raise NotImplementedError("The method wait_for_alerts() must be implemented in the subclass")

    def alert_action(self, category, response):
        """Check the Flow Category against the one returned by cdm."""

        raise NotImplementedError("The method alert_action() must be implemented in the subclass")

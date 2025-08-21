# file: dunetuf/media/media.py

import logging
import time
from typing import Any, Dict, Type, cast, Optional, List, Tuple, Union
from typing_extensions import Self  # type: ignore

from dunetuf.metadata import get_ip
from dunetuf.udw.udw import get_underware_instance
from dunetuf.cdm import get_cdm_instance
from dunetuf.control.targetdevice import TargetPlatform, device_instance
from dunetuf.media.enums.media_simulator_enums import MediaSize, MediaType, MediaInputIds, MediaOrientation
from dunetuf.udw import TclSocketClient

class Media:
    """
    Base class for media operations (capabilities / configuration).
    Instantiates the appropriate subclass depending on target platform.
    """
    MediaType = MediaType
    MediaSize = MediaSize
    MediaInputIds = MediaInputIds
    MediaOrientation = MediaOrientation

    def __new__(cls: Type[Self], *args: Any, **kwargs: Any) -> Self:
        if cls is Media:
            # Common initialization
            cls.ip_address = get_ip()
            cls._udw = get_underware_instance(ip=cls.ip_address)
            cls._cdm = get_cdm_instance(addr=cls.ip_address, udw=cls._udw)
            cls._target_platform = device_instance().target_platform

            # Delegate to concrete implementation
            if cls._target_platform == TargetPlatform.DUNE:
                from dunetuf.media.dune.media_dune import MediaDune
                return cast(Self, MediaDune(*args, **kwargs))
            elif cls._target_platform == TargetPlatform.ARES:
                from dunetuf.media.ares.media_ares import MediaAres
                return cast(Self, MediaAres(*args, **kwargs))
            else:
                raise NotImplementedError(
                    f"Media is not implemented for platform: {cls._target_platform}"
                )

        return cast(Self, super().__new__(cls))
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize Media instance."""

        self._tray: Optional[Media.Tray] = None

    
    @property
    def tray(self) -> "Media.Tray":
        if self._tray is None:
            self._tray = type(self).Tray(self)
        return self._tray

    def get_media_capabilities(self) -> Dict:
        """
        GET cdm/media/v1/capabilities
        Retrieves the device’s media capabilities, trays, and finishers.
        """
        logging.info("Fetching media capabilities")
        return self._cdm.get(self._cdm.CDM_MEDIA_CAPABILITIES)

    def get_media_configuration(self) -> Dict:
        """
        GET cdm/media/v1/configuration
        Retrieves the current media, tray, and finisher configuration.
        """
        logging.info("Fetching media configuration")
        return self._cdm.get(self._cdm.CDM_MEDIA_CONFIGURATION)

    def update_media_configuration(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/configuration
        Applies a partial update to the media configuration.
        
        Args:
            payload: dict of fields to update.
        """
        logging.info("Updating media configuration: %s", payload)
        self._cdm.patch(self._cdm.CDM_MEDIA_CONFIGURATION, payload)
        

    def create_media_configuration(self, payload: Dict) -> None:
        """
        POST cdm/media/v1/configuration
        Replaces the entire media configuration.
        
        Args:
            payload: dict representing the full configuration.
        """
        logging.info("Creating/replacing media configuration: %s", payload)
        self._cdm.post(self._cdm.CDM_MEDIA_CONFIGURATION, payload)

    # --- Media Source (Input) Configuration ---
    
    def get_media_source_configuration(self, media_source_id: str) -> Dict[str, Any]:
        """
        Retrieves the configuration for a specific media source (input) by its ID.

        Args:
            media_source_id (str): The mediaSourceId to look up.

        Returns:
            Dict[str, Any]: The input configuration dict for the given mediaSourceId.

        Raises:
            KeyError: If no input with the given mediaSourceId is found.
        """
        logging.info("Looking up media source configuration for ID: %s", media_source_id)
        config = self.get_media_configuration()
        for inp in config.get("inputs", []):
            if inp.get("mediaSourceId") == media_source_id:
                return inp
        raise KeyError(f"No input configuration found for mediaSourceId '{media_source_id}'")
    
    def get_media_source_capabilities(self, media_source_id: str) -> Dict[str, Any]:
        """
        Retrieves the capabilities for a specific media source (input) by its ID.

        Args:
            media_source_id (str): The mediaSourceId to look up.

        Returns:
            Dict[str, Any]: The input capabilities dict for the given mediaSourceId.

        Raises:
            KeyError: If no input with the given mediaSourceId is found.
        """
        logging.info("Looking up media source capabilities for ID: %s", media_source_id)
        capabilities = self.get_media_capabilities()
        for inp in capabilities.get("supportedInputs", []):
            if inp.get("mediaSourceId") == media_source_id:
                return inp
        raise KeyError(f"No input capabilities found for mediaSourceId '{media_source_id}'")
    

    def get_supported_sizes(self, media_source_id: str) -> List[str]:
        """Return a list of media sizes supported by the device/tray.

        Args:
            tray: Media source for which supported media size is required.(Optional)

        Return:
            media_size: Supported media size for device/tray
        """
        if not media_source_id:
            media_sizes = self.get_media_capabilities().get('supportedMediaSizes', [])
            logging.info('Supported Media Sizes (device): %s', media_sizes)
            return media_sizes

        for tray_config in self.get_media_capabilities().get('supportedInputs', []):
            if tray_config.get('mediaSourceId') == media_source_id:
                media_sizes = tray_config.get('supportedMediaSizes', [])
                logging.info('Supported Media Sizes (%s): %s', media_source_id, media_sizes)
                return media_sizes

        raise Exception(f"Media source '{media_source_id}' not found!")
    
    def get_supported_types(self, media_source_id: str) -> List[str]:
        """Return a list of media types supported by the device/tray.

        Args:
            media_source_id: Media source for which supported media type is required.

        Return:
            media_types: Supported media types for device/tray
        """
        if not media_source_id:
            media_types = self.get_media_capabilities().get('supportedMediaTypes', [])
            logging.info('Supported Media Types (device): %s', media_types)
            return media_types

        for tray_config in self.get_media_capabilities().get('supportedInputs', []):
            if tray_config.get('mediaSourceId') == media_source_id:
                media_types = tray_config.get('supportedMediaTypes', [])
                logging.info('Supported Media Types (%s): %s', media_source_id, media_types)
                return media_types

        raise Exception(f"Media source '{media_source_id}' not found!")
    
    def is_size_supported(self, media_source_id: str, size: str) -> bool:
        """Check if a specific media size is supported by the device/tray.

        Args:
            media_source_id: Media source to check.
            size: Media size to verify.

        Return:
            bool: True if the size is supported, False otherwise.
        """
        supported_sizes = self.get_supported_sizes(media_source_id)
        is_supported = size in supported_sizes
        logging.info('Is size "%s" supported for %s? %s', size, media_source_id, is_supported)
        return is_supported
    
    def is_type_supported(self, media_source_id: str, media_type: str) -> bool:
        """Check if a specific media type is supported by the device/tray.

        Args:
            media_source_id: Media source to check.
            media_type: Media type to verify.

        Return:
            bool: True if the type is supported, False otherwise.
        """
        supported_types = self.get_supported_types(media_source_id)
        is_supported = media_type in supported_types
        logging.info('Is type "%s" supported for %s? %s', media_type, media_source_id, is_supported)
        return is_supported
    
    def is_media_supported(self, media_source_id: str) -> bool:
        """Check if a specific media source is supported by the device.
        Args:
            media_source_id: Media source to check.
        Return:
            bool: True if the media source is supported, False otherwise.
        """
        if not media_source_id:
            logging.error('Media source ID cannot be empty!')
            return False
            
        configuration = self.get_media_configuration().get('inputs', [])
        media_supported = [media.get('mediaSourceId') for media in configuration]

        if media_source_id not in media_supported:
            logging.error('Media source %s is not supported!', media_source_id)
            return False
        
        logging.info('Media source %s is supported.', media_source_id)
        return True

    def get_source_and_media_sizes(self, source = None) -> Tuple[str, List[str]]:
        """Get the default tray and its supported media sizes.
        
        Returns:
            tuple: (default_tray, media_sizes) where default_tray is the default source
                   and media_sizes is a list of supported media sizes for that tray
        """
        if source is None:
            source = self.get_default_source()
        supported_inputs = self.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((input.get('supportedMediaSizes', []) for input in supported_inputs if input.get('mediaSourceId') == source), [])
        logging.info('Supported Media Sizes (%s): %s', source, media_sizes)
        return source, media_sizes

    def get_media_sizes(self, source = None) -> List[str]:
        """Get the supported media sizes for a specific source.
        
        Returns:
            List[str]: A list of supported media sizes for the specified source.
        """
        if source is None:
            raise ValueError("Source must be specified to get media sizes.")
        supported_inputs = self.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((input.get('supportedMediaSizes', []) for input in supported_inputs if input.get('mediaSourceId') == source), [])
        logging.info('Supported Media Sizes (%s): %s', source, media_sizes)
        return media_sizes        

    # --- DUNE/ARES-specific stubs below ---

    def get_finisher_configuration(self) -> Dict:
        """
        GET cdm/media/v1/finisherConfiguration
        Retrieves the current finisher configuration.
        """
        raise NotImplementedError("get_finisher_configuration() must be implemented in the subclass")

    def put_finisher_configuration(self, payload: Dict) -> None:
        """
        PUT cdm/media/v1/finisherConfiguration
        Replaces the entire finisher configuration.

        Args:
            payload: dict representing the full finisher configuration.
        """
        raise NotImplementedError("put_finisher_configuration() must be implemented in the subclass")

    def update_finisher_configuration(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/finisherConfiguration
        Applies a partial update to the finisher configuration.

        Args:
            payload: dict of fields to update.
        """
        raise NotImplementedError("update_finisher_configuration() must be implemented in the subclass")

    def get_finisher_capabilities(self) -> Dict:
        """
        GET cdm/media/v1/finisherCapabilities
        Retrieves the device’s finisher capabilities.
        """
        raise NotImplementedError("get_finisher_capabilities() must be implemented in the subclass")

    def get_custom_folding_styles(self) -> Dict:
        """
        GET cdm/media/v1/customFoldingStyles
        Retrieves all custom folding styles.
        """
        raise NotImplementedError("get_custom_folding_styles() must be implemented in the subclass")

    def create_custom_folding_style(self, payload: Dict) -> None:
        """
        POST cdm/media/v1/customFoldingStyles
        Creates a new custom folding style.

        Args:
            payload: dict representing the new folding style.
        """
        raise NotImplementedError("create_custom_folding_style() must be implemented in the subclass")

    def get_custom_folding_style(self, custom_folding_style_id: str) -> Dict:
        """
        GET cdm/media/v1/customFoldingStyles/{customFoldingStyleId}
        Retrieves a specific custom folding style by ID.

        Args:
            custom_folding_style_id: ID of the folding style to retrieve.
        """
        raise NotImplementedError("get_custom_folding_style() must be implemented in the subclass")

    def update_custom_folding_style(self, custom_folding_style_id: str, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/customFoldingStyles/{customFoldingStyleId}
        Applies a partial update to a specific custom folding style.

        Args:
            custom_folding_style_id: ID of the folding style to update.
            payload: dict of fields to update.
        """
        raise NotImplementedError("update_custom_folding_style() must be implemented in the subclass")

    def delete_custom_folding_style(self, custom_folding_style_id: str) -> None:
        """
        DELETE cdm/media/v1/customFoldingStyles/{customFoldingStyleId}
        Deletes a specific custom folding style.

        Args:
            custom_folding_style_id: ID of the folding style to delete.
        """
        raise NotImplementedError("delete_custom_folding_style() must be implemented in the subclass")

    def get_device_operations(self) -> Dict:
        """
        GET cdm/media/v1/deviceOperations
        Retrieves the list of available device operations.
        """
        raise NotImplementedError("get_device_operations() must be implemented in the subclass")

    def get_device_operations_for_device(self, device_identifier: str) -> Dict:
        """
        GET cdm/media/v1/deviceOperations/{deviceIdentifier}
        Retrieves the operations for a specific device.

        Args:
            device_identifier: ID of the device.
        """
        raise NotImplementedError("get_device_operations_for_device() must be implemented in the subclass")

    def update_device_operations_for_device(self, device_identifier: str, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/deviceOperations/{deviceIdentifier}
        Triggers or updates an operation for a specific device.

        Args:
            device_identifier: ID of the device.
            payload: dict with operation details.
        """
        raise NotImplementedError("update_device_operations_for_device() must be implemented in the subclass")

    def get_system_operations(self) -> Dict:
        """
        GET cdm/media/v1/systemOperations
        Retrieves the list of system operations.
        """
        raise NotImplementedError("get_system_operations() must be implemented in the subclass")

    def update_system_operations(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/systemOperations
        Triggers or updates a system operation.

        Args:
            payload: dict with operation details.
        """
        raise NotImplementedError("update_system_operations() must be implemented in the subclass")

    def get_cold_reset_media_size(self) -> Dict:
        """
        GET cdm/media/v1/coldResetMediaSize
        Retrieves the cold reset media size setting.
        """
        raise NotImplementedError("get_cold_reset_media_size() must be implemented in the subclass")

    def update_cold_reset_media_size(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/coldResetMediaSize
        Applies a partial update to the cold reset media size setting.

        Args:
            payload: dict of fields to update.
        """
        raise NotImplementedError("update_cold_reset_media_size() must be implemented in the subclass")

    def get_fixed_tray_guides_config(self) -> Dict:
        """
        GET cdm/media/v1/fixedTrayGuidesConfig
        Retrieves the fixed tray guides configuration.
        """
        raise NotImplementedError("get_fixed_tray_guides_config() must be implemented in the subclass")

    def update_fixed_tray_guides_config(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/fixedTrayGuidesConfig
        Applies a partial update to the fixed tray guides configuration.

        Args:
            payload: dict of fields to update.
        """
        raise NotImplementedError("update_fixed_tray_guides_config() must be implemented in the subclass")
    
    def set_device_status(
        self,
        device_id: int,
        state_value: str = "OK",
        status_values: Optional[List[str]] = None
    ) -> None:
        """
        Send a setDeviceStatus command via the Underware simulator for a given tray or bin.

        Args:
            device_id (int): ID of the tray or bin to update.
            state_value (str): State to set (e.g. "OK", "ERROR", "WARNING"). Defaults to "OK".
            status_values (List[str]): List of status values
                (e.g. ["READY"], ["OCCUPIED"]). Defaults to ["READY"].

        Raises:
            RuntimeError: If the simulator command fails (non-'1' return code).
        """
        raise NotImplementedError("set_device_status() must be implemented in the subclass")

    def get_default_source(self) -> str:
        """
        Determine default media source depending on configuration.
        
        Returns:
            str: The default media source identifier.
            
        Raises:
            ValueError: If no suitable default media source is found.
        """
        configuration = self.get_media_configuration()
        available_inputs = configuration.get('inputs', [])
        media_source = [input.get('mediaSourceId') for input in available_inputs]
        
        # Priority order for default source selection
        priority_sources = ['tray-1', 'main', 'main-roll', 'roll-1', 'roll']
        
        for source in priority_sources:
            if source in media_source:
                logging.info('Using default media source: %s', source)
                return source
        
        # If no priority source is found, raise a more specific exception
        raise ValueError(
            f'Cannot determine default media source. Available inputs: {available_inputs}'
        )

    def get_default_size(self, tray):
        """Determine default media size depending on media source."""
        # TODO: This is a workaround to identify the default size, though not a
        # correct way. A UDW/CDM interface should be provided by the firmware to
        # determine default size against the product (may be based on CR size).
        if 'tray' in tray:
            supported_inputs = self.get_media_capabilities().get('supportedInputs', [])
            media_sizes = next((input.get('supportedMediaSizes', []) for input in supported_inputs if input.get('mediaSourceId') == tray), [])
            if "any" in media_sizes:
                # ProA4 Laser products use Any Size as default paper size in Trays App
                default = "any"
            else:
                default = 'na_letter_8.5x11in'

        elif 'alternate' in tray:
            default = 'na_letter_8.5x11in'

        elif 'roll' in tray:
            default = 'custom'

        elif 'main' in tray:
            default = 'na_letter_8.5x11in'

        elif 'top' in tray:
            default = 'custom'

        else:
            raise Exception('Cannot determine default media size!')

        logging.debug('Using default media size: %s for %s', default, tray)
        return default

    def get_default_type(self, tray):
        """Determine default media type depending on media source."""
        default = None

        # TODO: This is a workaround to identify the default type.
        if 'tray' in tray:
            if "any" in self.get_supported_types(tray):
                # ProA4 Laser products use Any Type as default paper type in Trays App
                default = "any"
            else:
                default = 'stationery'

        elif 'alternate' in tray:
            default = 'stationery'

        elif 'roll' in tray:
            default = 'stationery'

        elif 'main' in tray:
            default = 'stationery'

        elif 'top' in tray:
            default = 'custom'

        else:
            raise Exception('Cannot determine default media type!')

        logging.debug('Using default media type: %s for %s', default, tray)
        return default

    def load_media(self, tray: str = 'all') -> None:
        """
        Simulate loading media (OCCUPIED + READY) on the specified tray(s).

        Args:
            tray: 'all' or specific mediaSourceId to target.

        Raises:
            AssertionError: if any tray did not reach 'ready' state.
        """
        raise NotImplementedError("load_media() must be implemented in the subclass")

    def almost_out_of_media(self, tray: str = 'all') -> None:
        """
        Simulate an 'almost out of media' warning on the specified tray(s).

        Args:
            tray: 'all' or specific mediaSourceId to target.
        """
        raise NotImplementedError("almost_out_of_media() must be implemented in the subclass")

    def unload_media(self, tray: str = 'all') -> None:
        """
        Simulate unloading media (OUT_OF_MEDIA) on the specified tray(s),
        and handle sizeType alert confirmations.

        Args:
            tray: 'all' or specific mediaSourceId to target.

        Raises:
            AssertionError: if any tray did not reach 'empty' state.
        """
        raise NotImplementedError("unload_media() must be implemented in the subclass")
    
    def reset_inputs(self) -> None:
        """
        Reset all media inputs to their default state.
        This implementation handles exceptions gracefully so that platform-specific
        behavior doesn't require try/catch in calling code.
        
        All Dune/Ares platform subclasses use this common implementation.
        """
        logging.info("Resetting all media inputs to default state.")
        try:
            for config in self.get_media_configuration().get('inputs', []):
                input = config.get('mediaSourceId')
                try:
                    media_size = self.get_default_size(input)
                    media_type = self.get_default_type(input)
                    logging.info('Resetting %s to default: %s - %s', input, media_size, media_type)
                    self.tray.load(input, media_size, media_type)
                except Exception as e:
                    logging.warning("Failed to reset input %s: %s", input, e)
                    logging.info("Continuing with other inputs")
        except Exception as e:
            logging.warning("Failed to get media configuration for reset: %s", e)
            logging.info("Skipping media input reset")

    def get_alerts(self, category='any'):
        """Get and return media handling alert list."""
        alerts = self._cdm.get(self._cdm.CDM_MEDIAHANDLING_ALERTS)

        alerts = alerts.get('alerts')
        logging.debug('Media handling alerts: %s', alerts)

        alerts = [alert for alert in alerts if alert.get('category') == category or category == 'any']
        return alerts

    def wait_for_alerts(self, category='any'):
        """
        Wait until a specific category of media alert is observed.

        Args:
            category: The category of media alert to wait for.
        """
        logging.info('Waiting for media handling alert of category: %s', category)

        ALERTS_TIME_OUT = 15
        time_elapsed = 0

        while time_elapsed <= ALERTS_TIME_OUT:
            alerts = self.get_alerts(category)
            logging.info('Expected alert category: %s, timeElapsed: %.1fs', category, time_elapsed)
            if alerts:
                logging.info('Expected alert category: %s, alerts raised: %s', category, alerts)
                return alerts
            
            time.sleep(0.5)
            time_elapsed += 0.5

        raise TimeoutError('Timeout waiting media handling alert!')

    def alert_action(self, category, response):
        """
        Check the Flow Category against the one returned by cdm.
        
        Args:
            category: The category of media alert to check.
            response: The response action to take for the alert.
        """
        alerts = self.get_alerts(category)
        response_data = {'selectedAction':  response}
        response_created = False
        for alert in alerts:
            if alert["category"] == 'sizeType' and category == 'sizeType':
                data = alert.get('data')
                for item in data:
                    if(item.get('propertyPointer') == '/currentMediaSource'):
                        media_source = item.get('value', {}).get('seValue') 
                        response_data = {"selectedAction": response, "mediaSourceId": media_source}
                        print("\n response data: " + str(response_data))
                        response_created = True
                        break
                if response_created:
                    break
        alerts = self.get_alerts(category)
        for alert in alerts:
            action_urls = alert.get('actions').get('links')
            action_url = [url.get('href') for url in action_urls][0]

            result = self._cdm.put_raw(action_url, response_data)
            assert result.status_code == 200


    class Tray:
        """
        Base class for tray operations, nested within Media.
        Created using the same IP / UDW / CDM as the parent Media container.
        """

        def __init__(self, media: 'Media') -> None:
            # store the parent instance to inherit cdm/udw
            self._media = media
            self._ip_address = media.ip_address
            self._cdm = media._cdm
            self._udw = media._udw
            self._tcl = TclSocketClient(self._ip_address, 9104)
            self._target_platform = media._target_platform
            logging.info(f"Initializing Tray for platform: {self._target_platform}")

        def install(self, tray: str, **kwargs: Optional[str]) -> None:
            """
            Install a media tray.
            
            Args:
                tray: The media tray to install.
            """
            raise NotImplementedError("install() must be implemented in the subclass")

        def uninstall(self, tray: str, **kwargs: Optional[str]) -> None:
            """
            Uninstall a media tray.

            Args:
                tray: The media tray to uninstall.

            """
            raise NotImplementedError("uninstall() must be implemented in the subclass")

        def load(
            self,
            input: Any,
            media_size: Any,
            media_type: Any,
            media_orientation: Optional[str] = None,
            width: Optional[float] = None,
            length: Optional[float] = None,
            resolution: Optional[int] = None,
            level: Optional[str] = None,
            status_values: Optional[List[str]] = None,
            need_open: Optional[bool] = None,
            **kwargs: Optional[str]
        ) -> None:
            """Update media configuration for a specific tray.
            
            Args:
                default_tray: Default tray identifier
                media_size: Media size to set
                media_type: Media type to set
                width: Custom width for media (optional)
                length: Custom length for media (optional)
                media_orientation: Media orientation to set (optional)
                resolution: Custom resolution for media (optional)
                level: Level of media (optional)
                status_values: List of status values to set (optional)
                neep_open: Whether to open the NEEP (optional)
                **kwargs: Additional parameters for future use (optional)

            Returns:
                None: Updates the media configuration for the specified tray.            
            """
            input = input.value if isinstance(input, MediaInputIds) else input
            media_size = media_size.value if isinstance(media_size, MediaSize) else media_size
            media_type = media_type.value if isinstance(media_type, MediaType) else media_type          
            media_input = self._media.get_media_configuration().get('inputs', [])
            
            for input_config in media_input:
                if input_config.get('mediaSourceId') == input:
                    # Handle custom media size configuration
                    if media_size == 'custom':
                        supported_inputs = self._media.get_media_capabilities().get('supportedInputs', [])
                        capability = next(
                            (cap for cap in supported_inputs if cap.get('mediaSourceId') == input),
                            {}
                        )
                        input_config['currentMediaWidth'] = width if width else capability.get('mediaWidthMaximum')
                        input_config['currentMediaLength'] = length if length else capability.get('mediaLengthMaximum')
                        input_config['currentResolution'] = resolution if resolution else capability.get('resolution')
                    
                    # Update media properties
                    input_config['currentMediaSize'] = media_size
                    input_config['currentMediaType'] = media_type
                    
                    # Update configuration and return early
                    self._media.update_media_configuration({'inputs': [input_config]})
                    if status_values:
                        self._send_device_status_command(input, status_values)
                    return
            
            logging.warning(f"No media input found for tray: {input}")

        def load_all_trays(
            self,
            input: Any,
            media_size: Any,
            media_type: Any,
            media_orientation: Optional[str] = None,
            width: Optional[float] = None,
            length: Optional[float] = None,
            resolution: Optional[int] = None,
            level: Optional[str] = None,
            status_values: Optional[List[str]] = None,
            need_open: Optional[bool] = None,
            **kwargs: Optional[str]
        ) -> None:
            """Configure all trays with the specified media size and type.
            
            Args:
                media_size: Media size to set for all trays
                media_type: Media type to set for all trays
                media_orientation: Media orientation to set for all trays (optional)
                width: Custom width for media (optional)
                length: Custom length for media (optional)
                resolution: Custom resolution for media (optional)
                level: Level of media (optional)
                status_values: List of status values to set (optional)
                need_open: Whether to open the NEEP (optional)
            Returns:
                None: Updates the media configuration for all trays.
            """
            logging.info('Configuring all trays with size %s and type %s', media_size, media_type)
            for tray in self._media.get_media_configuration().get('inputs', []):
                tray_id = tray['mediaSourceId']
                self.load(tray_id, media_size, media_type, media_orientation, width, length, resolution, level, status_values, need_open, **kwargs)

        def get(self, **kwargs: Optional[str]) -> List[str]:
            """Get the current tray configuration.
            Returns:
                List[str]: A set of tray identifiers currently configured.
            """
            logging.info('Fetching current tray configuration')
            media_inputs = self._media.get_media_configuration().get('inputs', [])
            trays = [input["mediaSourceId"] for input in media_inputs if 'tray-' in input["mediaSourceId"]]
            logging.info('Current tray configuration: %s', trays)
            return trays
        
        
        def get_supported_media_sizes(self, trayid, edge, **kwargs):
            """Get the supported media sizes for a specific tray."""
            raise NotImplementedError("get_supported_media_sizes() must be implemented in the subclass")

        def get_supported_media_types(self, trayid, **kwargs):
            """Get the supported media types for a specific tray."""
            raise NotImplementedError("get_supported_media_types() must be implemented in the subclass")

        def capacity_unlimited(self, trayid, **kwargs):
            """Set the tray capacity to unlimited."""
            raise NotImplementedError("capacity_unlimited() must be implemented in the subclass")

        def _send_device_status_command(self, input: str, status_values: List[str]) -> None:
            """Send device status command via TCL.
            
            Args:
                input: The device input identifier
                status_values: List of status values to set
            """
            command = "EngineSimulatorUw executeSimulatorAction MEDIA setDeviceStatus {{ idDevice: " + str(input) + ", stateValue: OK , statusValues:[ " + ",".join(status_values) + " ] }}"
            logging.info(f"Sending tcl: {command}")
            self._tcl.execute(command)

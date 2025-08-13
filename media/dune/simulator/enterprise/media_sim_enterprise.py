import logging
from typing import Optional, List, Any
from dunetuf.media.dune.media_dune import MediaDune
from dunetuf.media.media import Media
from dunetuf.media.enums.media_simulator_enums import MediaSize, MediaType, MediaInputIds

class MediaSimEnterprise(MediaDune):
    """
    Media Simulator Enterprise implementation for the Dune platform.
    Executes CDM calls for alerts, configuration, and capabilities.
    """
    MediaType = MediaType
    MediaSize = MediaSize
    MediaInputIds = MediaInputIds

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the Dune-specific MediaSimEnterprise instance.
        Sets up logging and prepares CDM/UDW interfaces inherited from the base class.
        """
        if getattr(self, "_simenterprise_inited", False):
            return
        self._simenterprise_inited = True
        logging.info("Initializing MediaSimEnterprise")
        super().__init__(*args, **kwargs)

    class Tray(Media.Tray):
        """
        Custom Tray for MediaLowFidelity.
        Here we redefine or extend the load, alert methods, etc.
        """
        def __init__(self, media: 'Media') -> None:
            # store the parent instance to inherit cdm/udw
            super().__init__(media)

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
                resolution: Custom resolution for media (optional)
                level: Custom level for media (optional)
                status_values: List of status values to set (optional)
                neep_open: Whether to open the tray after loading media (optional)
                **kwargs: Additional keyword arguments for future extensions
            """
            input = input.value if isinstance(input, MediaInputIds) else input
            media_size = media_size.value if isinstance(media_size, MediaSize) else media_size
            media_type = media_type.value if isinstance(media_type, MediaType) else media_type          
            media_input = self._media.get_media_configuration().get('inputs', [])

            for input_config in media_input:
                if input_config.get('mediaSourceId') == input:
                    # Handle custom media size configuration
                    if media_size == self._media.MediaSize.Custom:
                        if width is None or length is None:
                            logging.info(f"Changing media size to any custom for input: {input}")
                            media_size = self._media.MediaSize.AnyCustom
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
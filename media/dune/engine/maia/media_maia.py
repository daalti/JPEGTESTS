import logging
from typing import Optional, List, Union
from enum import Enum
from dunetuf.media.dune.media_dune import MediaDune
from dunetuf.media.media import Media
from dunetuf.print.new.mapper.mapper import PrintMapper
from dunetuf.media.enums.media_emulator_enums import MediaSize, MediaType, MediaInputIds

class MediaMaia(MediaDune):
    """
    Media Maia implementation for the Dune platform.
    Executes CDM calls for alerts, configuration, and capabilities.
    """
    MediaType = MediaType
    MediaSize = MediaSize
    MediaInputIds = MediaInputIds

    def __init__(self) -> None:
        """
        Initialize the Dune-specific MediaMaia instance.
        Sets up logging and prepares CDM/UDW interfaces inherited from the base class.
        """
        logging.info("Initializing MediaMaia")
        if getattr(self, "_class_initialized", False):
            return
        self._class_initialized = True
        super().__init__()
    
    def reset_inputs(self) -> None:
        """
        Reset all media inputs to their default state.
        This is a no-op in the base class, but can be overridden by subclasses.
        """
        logging.info("Resetting all media inputs to default state.")
        for config in self.get_media_configuration().get('inputs', []):
            input = config.get('mediaSourceId')
            media_size = self.get_default_size(input)
            media_type = self.get_default_type(input)
            logging.info('Resetting %s to default: %s - %s', input, media_size, media_type)
            Media.Tray.load(self.tray, input, media_size, media_type)

    class Tray(Media.Tray):
        """
        Custom Tray for MediaLowFidelity.
        Here we redefine or extend the load, alert methods, etc.
        """
        def __init__(self, media: 'Media') -> None:
            # store the parent instance to inherit cdm/udw
            super().__init__(media)
            self._mapper = PrintMapper(self._cdm)
            #self._tcl = TclSocketClient(self._ip_address, 9104)

        def load(
            self,
            input: MediaInputIds,
            media_size: MediaSize,
            media_type: MediaType,
            media_orientation: Optional[str] = None,
            width: Optional[float] = None,
            length: Optional[float] = None,
            resolution: Optional[int] = None,
            level: Optional[str] = 'High',
            status_values: Optional[List[str]] = None,
            need_open: Optional[bool] = None, 
            **kwargs: Optional[str]
        ) -> None:
            """
            Load media into the specified tray with the given parameters.
            Args:
                input (str): The media input identifier.
                media_size (str): The size of the media.
                media_type (str): The type of the media.
                media_orientation (Optional[str]): The orientation of the media.
                width (Optional[float]): The width of the media.
                length (Optional[float]): The length of the media.
                resolution (Optional[int]): The resolution of the media.
                level (Optional[str]): The tray level to load the media into.
                status_values (Optional[List[str]]): List of status values to set.
                need_open (Optional[bool]): Whether to open the tray before loading media.
                **kwargs: Additional keyword arguments for future extensions.
            Returns:
                None: This method does not return any value.
            Raises:
                ValueError: If the input is not valid, or if the media size or type is not supported.
            Logs:
                Info: Loading media input with specified parameters.
            """
            input_str = self._get_value(input)
            media_size_str = self._get_value(media_size)
            media_type_str = self._get_value(media_type)

            tray_cdm_name = self._mapper.get_media_input_cdm_name(input_str)
            mediasize_cdm_name = self._mapper.get_mediasize_cdm_name(media_size_str)
            mediatype_cdm_name = self._mapper.get_mediatype_cdm_name(media_type_str)

            configuration = self._media.get_media_configuration()
            printer_inputs = [printer_inputs.get('mediaSourceId') for printer_inputs in configuration]
            if input not in printer_inputs:
                raise ValueError(f"Input '{input_str}' is not a valid media source ID")
            
            if not self._media.is_size_supported(input_str, media_size_str):
                raise ValueError(f"Media size '{media_size_str}' is not supported for input '{input_str}'")
            
            if not self._media.is_type_supported(input_str, media_type_str):
                raise ValueError(f"Media type '{media_type_str}' is not supported for input '{input_str }'")

            self._media.tray.load(tray_cdm_name, mediasize_cdm_name, mediatype_cdm_name)

            logging.info(f"Loading media input '{tray_cdm_name}' with size '{mediasize_cdm_name}' and type '{mediatype_cdm_name}'")

        def _get_value(self, val: Union[Enum, str]) -> str:
            return val.value if isinstance(val, Enum) else val
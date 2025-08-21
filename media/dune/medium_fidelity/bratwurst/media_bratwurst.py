import logging
from typing import Optional, List, Union
from enum import Enum
from dunetuf.media.dune.media_dune import MediaDune
from dunetuf.media.media import Media
from dunetuf.emulation.print.mapper.mediumfidelity.bratwurst.MapperBratwurst import MapperBratwurst
from dunetuf.simulator.bratwurst import Bratwurst
from dunetuf.metadata import get_emulation_ip
from dunetuf.print.print_common_types import TrayLevel
from dunetuf.media.enums.media_emulator_enums import MediaSize, MediaType, MediaInputIds

class MediaBratwurst(MediaDune):
    """
    Media Bratwurst implementation for the Dune platform.
    Executes CDM calls for alerts, configuration, and capabilities.
    """
    MediaType = MediaType
    MediaSize = MediaSize
    MediaInputIds = MediaInputIds

    def __init__(self) -> None:
        """
        Initialize the Dune-specific MediaBratwurst instance.
        Sets up logging and prepares CDM/UDW interfaces inherited from the base class.
        """
        logging.info("Initializing MediaBratwurst")
        super().__init__()
    
    class Tray(Media.Tray):
        """
        Custom Tray for MediaLowFidelity.
        Here we redefine or extend the load, alert methods, etc.
        """
        def __init__(self, media: 'Media') -> None:
            # store the parent instance to inherit cdm/udw
            if getattr(self, "_class_initialized", False):
                return
            self._class_initialized = True
            super().__init__(media)
            engine_simulator_ip = get_emulation_ip()
            if engine_simulator_ip == 'None':
                raise ValueError("Engine simulator IP is required but not provided. Please set -eip to emulator/simulator emulation IP.")
            logging.info('Instantiating PrintEmulation with %s', engine_simulator_ip)
            self._peclient = Bratwurst(engine_simulator_ip)
            self._mapper = MapperBratwurst()

        def install(self, tray: str, **kwargs: Optional[str]) -> None:
            """
            Install a media tray.
            
            Args:
                tray: The media tray to install.
            """
            tray_name = MediaInputIds[tray]
            self._peclient.TrayImplement.Install(tray_name, **kwargs) #type: ignore

        def uninstall(self, tray: str, **kwargs: Optional[str]) -> None:
            """
            Uninstall a media tray.

            Args:
                tray: The media tray to uninstall.

            """
            tray_name = MediaInputIds[tray]
            self._peclient.TrayImplement.Uninstall(tray_name, **kwargs) #type: ignore

        def load(
            self,
            input: MediaInputIds,
            media_size: MediaSize,
            media_type: MediaType,
            media_orientation: Optional[str] = None,
            width: Optional[float] = None,
            length: Optional[float] = None,
            resolution: Optional[int] = None,
            level: Optional[str] = TrayLevel.High.name,
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
                neep_open (Optional[bool]): Whether to open the tray after loading media.
                **kwargs: Additional keyword arguments for future extensions.
            Returns:
                None: This method does not return any value.
            Raises:
                ValueError: If the input is not valid, or if the media size or type is not supported.
            Logs:
                Info: Loading media input with specified parameters.
            """
            input_str = self._get_name(input)
            media_size_str = self._get_name(media_size)
            media_type_str = self._get_name(media_type)

            if need_open:
                logging.info(f"Opening tray {input_str} before loading media")
                self.open(input_str)

            tray_name = self._mapper.MediaInputIds[input_str]
            tray_level = self._mapper.TrayLevel[level or TrayLevel.High.name]
            emulation_media_size = self._mapper.MediaSizes[media_size_str]
            emulation_media_type = self._mapper.MediaTypes[media_type_str]
            emulation_media_orientation = self._mapper.MediaOrientation[media_orientation] if media_orientation is not None else None
            #TODO: TrayImplement is not implemented in Bratwurst
            self._peclient.TrayImplement.Load(emulation_media_size, emulation_media_type, emulation_media_orientation, tray_level, tray_name, **kwargs) #type: ignore

            if need_open:
                logging.info(f"Tray {input_str} closed after loading media")
                self.close(input_str)
                
        def get(self, **kwargs: Optional[str]) -> List[str]:
            """
            Get the list of installed trays and returns the tray ids.
            Args:
                **kwargs: Additional keyword arguments for the TrayImplement method.
            Returns:
                list[str]: A list of tray IDs that are installed.
            Raises:
                AssertionError: If any tray entries are missing in the mapper.
            """
            installed_trays = self._peclient.TrayImplement.InstalledTrays(**kwargs) #type: ignore
            logging.info(f"installed trays {installed_trays}")

            trays = []
            trays_not_in_mapper = []
            for tray in installed_trays:
                logging.info(f"tray = {tray}")
                found_in_mapper = False
                for id, value in self._mapper.MediaInputIds.items():
                    if tray == value:
                        trays.append(id)
                        found_in_mapper = True
                        break

                if not found_in_mapper:
                    trays_not_in_mapper.append(tray)

            assert len(trays_not_in_mapper) == 0, "Tray entries missing in bratwurst name mapper: {trays_not_in_mapper}"

            return trays

        def open(self, trayid: str, **kwargs: Optional[str]) -> None:
            """
            Open the specified tray.
            Args:
            trayid (str): The tray identifier to open.
            **kwargs: Additional keyword arguments for the TrayImplement method.
            Raises:
            KeyError: If the trayid is not found in the mapper.
            Logs:
            Info: Opening tray with specified ID.
            """
            logging.info(f"Opening tray: {trayid}")
            if trayid not in self._mapper.MediaInputIds:
                raise KeyError(f"Tray ID '{trayid}' not found in mapper")

            tray_name = self._mapper.MediaInputIds[trayid]
            self._peclient.TrayImplement.OpenTray(tray_name, **kwargs)  # type: ignore

        def close(self, trayid: str, **kwargs: Optional[str]) -> None:
            """
            Close the specified tray.
            Args:
            trayid (str): The tray identifier to close.
            **kwargs: Additional keyword arguments for the TrayImplement method.
            Raises:
            KeyError: If the trayid is not found in the mapper.
            Logs:
            Info: Closing tray with specified ID.
            """
            logging.info(f"Closing tray: {trayid}")
            if trayid not in self._mapper.MediaInputIds:
                raise KeyError(f"Tray ID '{trayid}' not found in mapper")

            tray_name = self._mapper.MediaInputIds[trayid]
            self._peclient.TrayImplement.CloseTray(tray_name, **kwargs)  # type: ignore

        def get_supported_media_sizes(self, trayid, edge, **kwargs):
            """Get supported media sizes for the tray"""
            edge = edge.lower()
            tray_name = self._mapper.MediaInputIds[trayid]
            supported_media_sizes = []
            sizes = None
            if edge == "short":
                sizes = self._peclient.TrayImplement.SizesShortList(tray_name, **kwargs) # type: ignore
            elif edge == "long":
                sizes = self._peclient.TrayImplement.SizesLongList(tray_name, **kwargs) # type: ignore

            if sizes is not None and isinstance(sizes, str):
                # Form list if 'sizes' is string - only one supported size
                supported_media_sizes.append(sizes)
            else:
                supported_media_sizes = sizes

            media_sizes = []
            if supported_media_sizes is not None:
                for media_size in supported_media_sizes:
                    for key, value in self._mapper.MediaSizes.items():
                        if media_size == value:
                            media_sizes.append(key)
                            break

            logging.info(f"Supported media sizes for {trayid} {edge} edge are {media_sizes}")
            return media_sizes

        def get_supported_media_types(self, trayid, **kwargs):
            """Get supported media types for the tray"""
            tray_name = self._mapper.MediaInputIds[trayid]
            supported_media_types = []
            types = self._peclient.TrayImplement.GetMediaType(tray_name, **kwargs) # type: ignore
            if isinstance(types, str):
                # Form list if 'types' is string - only one supported type
                supported_media_types.append(types)
            else:
                supported_media_types = types

            media_types = []
            for media_type in supported_media_types:
                for key, value in self._mapper.MediaTypes.items():
                    if media_type == value:
                        media_types.append(key)
                        break
            logging.info(f"Supported media types for {trayid} are {media_types}")
            return media_types

        def capacity_unlimited(self, trayid, **kwargs):
            """set tray capacity to unlimited."""
            tray_name = self._mapper.MediaInputIds[trayid]
            return self._peclient.TrayImplement.CapacityUnlimitedSet(tray_name, **kwargs) # type: ignore

        def _get_name(self, val: Union[Enum, str]) -> str:
            return val.name if isinstance(val, Enum) else val
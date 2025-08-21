import logging
import re
from typing import Optional, List, Union
from enum import Enum
from dunetuf.media.dune.media_dune import MediaDune
from dunetuf.media.media import Media
from dunetuf.emulation.print.mapper.highfidelity.canon.MapperCanon import MapperCanon
from dunetuf.emulator.canon.CanonClient import CanonClient, Canon
from dunetuf.metadata import get_emulation_ip
from dunetuf.print.print_common_types import TrayLevel
from dunetuf.media.enums.media_emulator_enums import MediaSize, MediaType, MediaInputIds

class MediaCanon(MediaDune):
    """
    Media Canon implementation for the Dune platform.
    Executes CDM calls for alerts, configuration, and capabilities.
    """
    MediaType = MediaType
    MediaSize = MediaSize
    MediaInputIds = MediaInputIds

    def __init__(self) -> None:
        """
        Initialize the Dune-specific MediaCanon instance.
        Sets up logging and prepares CDM/UDW interfaces inherited from the base class.
        """
        logging.info("Initializing MediaCanon")
        super().__init__()

    class Tray(Media.Tray):
        """
        Custom Tray for MediaLowFidelity.
        Here we redefine or extend the load, alert methods, etc.
        """
        def __init__(self, media: 'Media') -> None:
            # store the parent instance to inherit cdm/udw
            super().__init__(media)
            engine_simulator_ip = get_emulation_ip()
            if engine_simulator_ip == 'None':
                raise ValueError("Engine simulator IP is required but not provided. Please set -eip to emulator/simulator emulation IP.")
            logging.info('Instantiating PrintEmulation with %s', engine_simulator_ip)
            self._peclient = Canon(engine_simulator_ip)
            self._mapper = MapperCanon()

        def install(self, tray: str, **kwargs: Optional[str]) -> None:
            """
            Install a media tray.
            
            Args:
                tray: The media tray to install.
            """
            tray_name = MediaInputIds[tray]
            self._peclient.client.execute(f'tray {tray_name} install')

        def uninstall(self, tray: str, **kwargs: Optional[str]) -> None:
            """
            Uninstall a media tray.

            Args:
                tray: The media tray to uninstall.

            """
            tray_name = MediaInputIds[tray]
            self._peclient.client.execute(f'tray {tray_name} uninstall')

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
                need_open (Optional[bool]): Whether to open the tray before loading media.
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

            if level == 'Empty':
                return self.empty(input_str)
            tray_name = self._mapper.MediaInputIds[input_str]
            tray_level = self._mapper.TrayLevel[level or TrayLevel.High.name]
            emulation_size = self._mapper.MediaSizes[media_size_str]
            emulation_type = self._mapper.MediaTypes[media_type_str]
            emulation_orientation = self._mapper.MediaOrientation[media_orientation] if media_orientation is not None else None
            self._peclient.client.execute(f'tray {tray_name} {tray_level} {emulation_size} {emulation_type} {emulation_orientation}')

            if need_open:
                logging.info(f"Closing tray {input_str} after loading media")
                self.close(input_str)

        
        def empty(self, input: str, **kwargs) -> None:
            """
            Empty the specified media tray.
            
            Args:
            input (str): The media input identifier/tray ID to empty.
            **kwargs: Additional optional parameters (currently unused).
            
            Raises:
            KeyError: If the input identifier is not found in MediaInputIds mapping.
            
            Logs:
            Info: When successfully emptying the tray.
            """
            try:
                tray_name = self._mapper.MediaInputIds[input]
                self._peclient.client.execute(f'tray {tray_name} empty')
                logging.info(f"Successfully emptied tray: {input} ({tray_name})")
            except KeyError:
                logging.error(f"Invalid input identifier: {input}")
                raise ValueError(f"Input '{input}' not found in available media inputs")

        def get(self, **kwargs: Optional[str]) -> List[str]:
            """
            Retrieve the list of installed media trays.
            
            Returns:
            List[str]: A list of tray identifiers for all currently installed trays.
            
            Raises:
            RuntimeError: If unable to retrieve tray status from the client.
            
            Logs:
            Info: The list of installed trays found.
            Warning: If no installed trays are found.
            """
            try:
                tray_status = self._peclient.client.execute('tray status')
                
                # Extract tray information using regex
                tray_matches = re.findall(r'tray\w*_[^)]*\)', tray_status)
                tray_list = []
                
                for tray_match in tray_matches:
                    # Skip uninstalled trays
                    if 'uninstalled' in tray_match.lower():
                        continue
                    
                    # Extract tray name and map back to input ID
                    tray_parts = tray_match.split('_')
                    tray_name = tray_parts[0] if tray_parts else ""
                    # Find the corresponding input ID
                    for input_id, mapped_name in self._mapper.MediaInputIds.items():
                        if mapped_name == tray_name:
                            tray_list.append(input_id)
                            break
                
                if not tray_list:
                    logging.warning("No installed trays found")
                else:
                    logging.info(f"Installed trays: {tray_list}")
                
                return tray_list
            
            except Exception as e:
                logging.error(f"Failed to retrieve tray status: {e}")
                raise RuntimeError(f"Unable to get tray information: {e}")

        def open(self, trayid: str) -> None:
            """
            Open the specified media tray.
            Args:
            trayid (str): The media input identifier/tray ID to open.
            Raises:
            ValueError: If the tray identifier is not found in available media inputs.
            RuntimeError: If unable to execute the open command.
            """
            try:
                tray_name = self._mapper.MediaInputIds[trayid]
                self._peclient.client.execute(f"tray {tray_name} open")
                logging.info(f"Successfully opened tray: {trayid} ({tray_name})")
            except KeyError:
                logging.error(f"Invalid tray identifier: {trayid}")
                raise ValueError(f"Tray '{trayid}' not found in available media inputs")
            except Exception as e:
                logging.error(f"Failed to open tray {trayid}: {e}")
                raise RuntimeError(f"Unable to open tray {trayid}: {e}")

        def close(self, trayid: str) -> None:
            """
            Close the specified media tray.
            Args:
            trayid (str): The media input identifier/tray ID to close.
            **kwargs: Additional optional parameters (currently unused).
            Raises:
            ValueError: If the tray identifier is not found in available media inputs.
            RuntimeError: If unable to execute the close command.
            """
            try:
                tray_name = self._mapper.MediaInputIds[trayid]
                self._peclient.client.execute(f"tray {tray_name} close")
                logging.info(f"Successfully closed tray: {trayid} ({tray_name})")
            except KeyError:
                logging.error(f"Invalid tray identifier: {trayid}")
                raise ValueError(f"Tray '{trayid}' not found in available media inputs")
            except Exception as e:
                logging.error(f"Failed to close tray {trayid}: {e}")
                raise RuntimeError(f"Unable to close tray {trayid}: {e}")
            
        def get_supported_media_sizes(self, trayid, edge, **kwargs):
            """Get supported media sizes for the tray - E.g. tray tray2 show media sizes short"""
            edge = edge.lower() #[long | short]
            tray_name = self._mapper.MediaInputIds[trayid]
            supported_media_sizes = []
            media_sizes = self._peclient.client.execute(f'tray {tray_name} show media sizes {edge}')
            media_sizes = media_sizes.split('\n')[1]
            sizes = media_sizes.replace(',','')
            sizes = sizes.split()

            if isinstance(sizes, str):
                # Form list if 'sizes' is string - only one supported size
                supported_media_sizes.append(sizes)
            else:
                supported_media_sizes = sizes
            # Get common size names corresponding to canon names
            media_sizes = []
            for media_size in supported_media_sizes:
                for key, value in self._mapper.MediaSizes.items():
                    if media_size == value:
                        media_sizes.append(key)
                        break
            logging.info(f"Supported media sizes for {trayid} are {media_sizes}")
            return media_sizes

        def get_supported_media_types(self, trayid, **kwargs):
            """Get supported media types for the tray - E.g.  tray tray2 show media types"""
            tray_name = self._mapper.MediaInputIds[trayid]
            supported_media_types = []
            types = self._peclient.client.execute(f'tray {tray_name} show media types')
            media_types = types.split('\n')[1]
            types = media_types.replace(',', '')
            types = types.split()

            if isinstance(types, str):
                # Form list if 'types' is string - only one supported type
                supported_media_types.append(types)
            else:
                supported_media_types = types
            # Get common media type names corresponding to canon names
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
            #    Set the indicated tray to the limited or unlimited state
            tray_name = self._mapper.MediaInputIds[trayid]
            return self._peclient.client.execute(f'tray {tray_name} unlimited')
            
        def _get_name(self, val: Union[Enum, str]) -> str:
            return val.name if isinstance(val, Enum) else val
# file: dunetuf/media/dune/media_dune.py

import logging
from typing import Any, Dict, Type, cast, Optional, List
from typing_extensions import Self  # type: ignore
from dunetuf.media.media import Media
from dunetuf.media.media_handling import MediaHandling

from dunetuf.configuration import Configuration
from dunetuf.emulation.print.print_emulation_ids import DuneEnginePlatform, DuneEngineInterface, DuneEngineMake


class MediaDune(Media):
    """
    Media implementation for the DUNE platform.
    Inherits all methods from the base Media class and adds DUNE-specific endpoints.
    """

    def __new__(cls: Type[Self], *args: Any, **kwargs: Any) -> Self:
        if cls is MediaDune:
            # Common initialization
            cls._configuration = Configuration(cls._cdm)
            cls._family_name = cls._configuration.familyname
            cls._product_name = cls._configuration.productname
            pe_platform = cls._udw.mainApp.execute("ConnectorDriver PUB_getPrintEnginePlatform") # type: ignore
            cls._print_engine_platform = DuneEnginePlatform(int(pe_platform)).name
            pe_interface = cls._udw.mainApp.execute("ConnectorDriver PUB_getPrintEngineInterface") # type: ignore
            cls._print_engine_interface = DuneEngineInterface(int(pe_interface)).name
            pe_make = cls._udw.mainApp.execute("ConnectorDriver PUB_getEngineMake") # type: ignore
            cls._engine_make = DuneEngineMake(int(pe_make)).name
            logging.info("MediaDune initialized with platform: %s, interface: %s, make: %s",
                         cls._print_engine_platform, cls._print_engine_interface, cls._engine_make)

            if cls._print_engine_platform == DuneEnginePlatform.hwEngine.name:
                pass  # Hardware engine does not require special handling
                if cls._print_engine_interface == DuneEngineInterface.maia.name or cls._print_engine_interface == DuneEngineInterface.bratwurst.name:
                    from dunetuf.media.dune.engine.maia.media_maia import MediaMaia
                    return cast(Self, MediaMaia(*args, **kwargs))                    
                elif cls._print_engine_interface == DuneEngineInterface.homeSmb.name:
                    from dunetuf.media.dune.engine.homesmb.media_homesmb import MediaHomeSmb
                    return cast(Self, MediaHomeSmb(*args, **kwargs))
            elif cls._print_engine_platform == DuneEnginePlatform.mediumFidelitySim.name:
                if cls._print_engine_interface == DuneEngineInterface.bratwurst.name:
                    from dunetuf.media.dune.medium_fidelity.bratwurst.media_bratwurst import MediaBratwurst
                    return cast(Self, MediaBratwurst(*args, **kwargs))
            elif cls._print_engine_platform == DuneEnginePlatform.emulator.name or cls._print_engine_platform == DuneEnginePlatform.highFidelitySim.name:
                if cls._engine_make in [DuneEngineMake.canon.name, DuneEngineMake.canonHomepro.name]:
                    from dunetuf.media.dune.high_fildelity.canon.media_canon import MediaCanon
                    return cast(Self, MediaCanon(*args, **kwargs))
                elif cls._engine_make == DuneEngineMake.hp.name and cls._print_engine_interface == DuneEngineInterface.bratwurst.name: #Hpmfp emulator
                    from dunetuf.media.dune.medium_fidelity.bratwurst.media_bratwurst import MediaBratwurst
                    return cast(Self, MediaBratwurst(*args, **kwargs))
            elif cls._family_name == "enterprise":
                logging.info("Creating MediaSimEnterprise for enterprise simulator")
                from dunetuf.media.dune.simulator.enterprise.media_sim_enterprise import MediaSimEnterprise
                return cast(Self, MediaSimEnterprise(*args, **kwargs))

            return cast(Self, super().__new__(cls, *args, **kwargs))

        return cast(Self, super().__new__(cls, *args, **kwargs))

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if getattr(self, "_media_dune_initialized", False):
            return
        self._media_dune_initialized = True
        if type(self) is MediaDune:
            logging.info("Initializing MediaDune")
        self._media_handling = MediaHandling()
        super().__init__(*args, **kwargs)

    # /cdm/media/v1/finisherConfiguration  - GET / PUT / PATCH
    def get_finisher_configuration(self) -> Dict:
        """
        GET cdm/media/v1/finisherConfiguration
        Retrieves the current finisher configuration.
        """
        logging.info("Fetching finisher configuration")
        return self._cdm.get(self._cdm.MEDIA_FINISHER_CONFIGURATION)

    def put_finisher_configuration(self, payload: Dict) -> None:
        """
        PUT cdm/media/v1/finisherConfiguration
        Replaces the entire finisher configuration.

        Args:
            payload: dict representing the full finisher configuration.
        """
        logging.info("Replacing finisher configuration: %s", payload)
        self._cdm.put(self._cdm.MEDIA_FINISHER_CONFIGURATION, payload)

    def update_finisher_configuration(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/finisherConfiguration
        Applies a partial update to the finisher configuration.

        Args:
            payload: dict of fields to update.
        """
        logging.info("Updating finisher configuration: %s", payload)
        self._cdm.patch(self._cdm.MEDIA_FINISHER_CONFIGURATION, payload)

    # /cdm/media/v1/finisherCapabilities  - GET
    def get_finisher_capabilities(self) -> Dict:
        """
        GET cdm/media/v1/finisherCapabilities
        Retrieves the device’s finisher capabilities.
        """
        logging.info("Fetching finisher capabilities")
        return self._cdm.get(self._cdm.MEDIA_FINISHER_CAPABILITIES)

    # /cdm/media/v1/customFoldingStyles  - GET / POST
    def get_custom_folding_styles(self) -> Dict:
        """
        GET cdm/media/v1/customFoldingStyles
        Retrieves all custom folding styles.
        """
        logging.info("Fetching custom folding styles")
        return self._cdm.get(self._cdm.MEDIA_CUSTOM_FOLDING_STYLES)

    def create_custom_folding_style(self, payload: Dict) -> None:
        """
        POST cdm/media/v1/customFoldingStyles
        Creates a new custom folding style.

        Args:
            payload: dict representing the new folding style.
        """
        logging.info("Creating custom folding style: %s", payload)
        self._cdm.post(self._cdm.MEDIA_CUSTOM_FOLDING_STYLES, payload)

    # /cdm/media/v1/customFoldingStyles/{customFoldingStyleId}  - GET / PATCH / DELETE
    def get_custom_folding_style(self, custom_folding_style_id: str) -> Dict:
        """
        GET cdm/media/v1/customFoldingStyles/{customFoldingStyleId}
        Retrieves a specific custom folding style by ID.

        Args:
            custom_folding_style_id: ID of the folding style to retrieve.
        """
        logging.info("Fetching custom folding style %s", custom_folding_style_id)
        return self._cdm.get(f'{self._cdm.MEDIA_CUSTOM_FOLDING_STYLES}/{custom_folding_style_id}')

    def update_custom_folding_style(self, custom_folding_style_id: str, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/customFoldingStyles/{customFoldingStyleId}
        Applies a partial update to a specific custom folding style.

        Args:
            custom_folding_style_id: ID of the folding style to update.
            payload: dict of fields to update.
        """
        logging.info("Updating custom folding style %s: %s", custom_folding_style_id, payload)
        self._cdm.patch(f'{self._cdm.MEDIA_CUSTOM_FOLDING_STYLES}/{custom_folding_style_id}', payload)

    def delete_custom_folding_style(self, custom_folding_style_id: str) -> None:
        """
        DELETE cdm/media/v1/customFoldingStyles/{customFoldingStyleId}
        Deletes a specific custom folding style.

        Args:
            custom_folding_style_id: ID of the folding style to delete.
        """
        logging.info("Deleting custom folding style %s", custom_folding_style_id)
        self._cdm.delete(f'{self._cdm.MEDIA_CUSTOM_FOLDING_STYLES}/{custom_folding_style_id}')

    # /cdm/media/v1/deviceOperations  - GET
    def get_device_operations(self) -> Dict:
        """
        GET cdm/media/v1/deviceOperations
        Retrieves the list of available device operations.
        """
        logging.info("Fetching device operations list")
        return self._cdm.get(self._cdm.MEDIA_V1_DEVICEOPERATIONS)

    # /cdm/media/v1/deviceOperations/{deviceIdentifier}  - GET / PATCH
    def get_device_operations_for_device(self, device_identifier: str) -> Dict:
        """
        GET cdm/media/v1/deviceOperations/{deviceIdentifier}
        Retrieves the operations for a specific device.

        Args:
            device_identifier: ID of the device.
        """
        logging.info("Fetching operations for device %s", device_identifier)
        return self._cdm.get(f'{self._cdm.MEDIA_V1_DEVICEOPERATIONS}/{device_identifier}')

    def update_device_operations_for_device(self, device_identifier: str, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/deviceOperations/{deviceIdentifier}
        Triggers or updates an operation for a specific device.

        Args:
            device_identifier: ID of the device.
            payload: dict with operation details.
        """
        logging.info("Updating device operations for %s: %s", device_identifier, payload)
        self._cdm.patch(f'{self._cdm.MEDIA_V1_DEVICEOPERATIONS}/{device_identifier}', payload)

    # /cdm/media/v1/systemOperations  - GET / PATCH
    def get_system_operations(self) -> Dict:
        """
        GET cdm/media/v1/systemOperations
        Retrieves the list of system operations.
        """
        logging.info("Fetching system operations")
        return self._cdm.get(self._cdm.MEDIA_V1_SYSTEMOPERATIONS)

    def update_system_operations(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/systemOperations
        Triggers or updates a system operation.

        Args:
            payload: dict with operation details.
        """
        logging.info("Updating system operations: %s", payload)
        self._cdm.patch(self._cdm.MEDIA_V1_SYSTEMOPERATIONS, payload)

    # /cdm/media/v1/coldResetMediaSize  - GET / PATCH
    def get_cold_reset_media_size(self) -> Dict:
        """
        GET cdm/media/v1/coldResetMediaSize
        Retrieves the cold reset media size setting.
        """
        logging.info("Fetching cold reset media size")
        return self._cdm.get(self._cdm.MEDIA_V1_COLDRESET_MEDIASIZE)

    def update_cold_reset_media_size(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/coldResetMediaSize
        Applies a partial update to the cold reset media size setting.

        Args:
            payload: dict of fields to update.
        """
        logging.info("Updating cold reset media size: %s", payload)
        self._cdm.patch(self._cdm.MEDIA_V1_COLDRESET_MEDIASIZE, payload)

    # /cdm/media/v1/fixedTrayGuidesConfig  - GET / PATCH
    def get_fixed_tray_guides_config(self) -> Dict:
        """
        GET cdm/media/v1/fixedTrayGuidesConfig
        Retrieves the fixed tray guides configuration.
        """
        logging.info("Fetching fixed tray guides configuration")
        return self._cdm.get('cdm/media/v1/fixedTrayGuidesConfig')

    def update_fixed_tray_guides_config(self, payload: Dict) -> None:
        """
        PATCH cdm/media/v1/fixedTrayGuidesConfig
        Applies a partial update to the fixed tray guides configuration.

        Args:
            payload: dict of fields to update.
        """
        logging.info("Updating fixed tray guides configuration: %s", payload)
        self._cdm.patch('cdm/media/v1/fixedTrayGuidesConfig', payload)

    def media_set_device_status(self, tray: str, payload_template: str) -> None:
        """
        Send device status update commands via the simulator for specified tray(s).

        Args:
            tray: 'all' or specific mediaSourceId to target.
            payload_template: Template string for device status payload,
                must contain '{device_id}' placeholder for formatting.

        Raises:
            RuntimeError: if simulator command returns a non-success result.
        """
        # Fetch current media-handling configuration
        response_body = self._media_handling.get_configuration()

        # Determine target tray config list
        all_configs = self.get_media_configuration().get('inputs', [])
        targets = all_configs if tray == 'all' else [cfg for cfg in all_configs if cfg.get('mediaSourceId') == tray]

        for cfg in targets:
            device_id = cfg.get('deviceIdentifier')
            # Special case for tray 1 ALMOST_OUT_OF_MEDIA
            if str(device_id) == '1' and 'ALMOST_OUT_OF_MEDIA' in payload_template:
                command = (
                    "EngineSimulatorUw executeSimulatorAction MEDIA setDeviceStatus "
                    "{ idDevice: 1, stateValue: INFORM, statusValues:[ ALMOST_OUT_OF_MEDIA ] }"
                )
            else:
                formatted = payload_template.format(device_id=device_id)
                command = f"EngineSimulatorUw executeSimulatorAction MEDIA setDeviceStatus {formatted}"

            # Execute simulation command
            result = self._udw.mainApp.execute(command) # type: ignore
            if result != '1':
                raise RuntimeError(f"Simulator command failed: {command}")

            # Handle sizeType alerts for OCCUPIED events
            if 'OCCUPIED' in payload_template:
                try:
                    if response_body.get('sizeTypeEnabled') == 'true':
                        self._media_handling.wait_for_alerts('sizeType', 1)
                        self._media_handling.alert_action(category='sizeType', response='ok')
                except Exception:
                    logging.info("No sizeType alert to confirm")

    def load_media(self, tray: str = 'all') -> None:
        """
        Simulate loading media (OCCUPIED + READY) on the specified tray(s).

        Args:
            tray: 'all' or specific mediaSourceId to target.

        Raises:
            AssertionError: if any tray did not reach 'ready' state.
        """
        logging.info('Loading media on %s', tray)
        occupied = "{{{{ idDevice: {device_id}, stateValue: OK, statusValues: [ OCCUPIED ] }}}}"
        self.media_set_device_status(tray, occupied)

        ready = "{{{{ idDevice: {device_id}, stateValue: OK, statusValues: [ READY ] }}}}"
        self.media_set_device_status(tray, ready)

        # Pull the inputs array directly from CDM
        inputs = self.get_media_configuration().get('inputs', [])
        # Filter by tray if requested
        configs = inputs if tray == 'all' else [
            cfg for cfg in inputs
            if cfg.get('mediaSourceId') == tray
        ]

        # Assert every targeted tray is now in “ready” state
        ready_states = [cfg.get('stateReason') == 'ready' for cfg in configs]
        assert all(ready_states), (
            "Loading failed, not all expected trays are in ready state!"
        )


    def almost_out_of_media(self, tray: str = 'all') -> None:
        """
        Simulate an 'almost out of media' warning on the specified tray(s).

        Args:
            tray: 'all' or specific mediaSourceId to target.
        """
        logging.info('Setting almost out of media on %s', tray)
        warning = "{{{{ idDevice: {device_id}, stateValue: WARNING, statusValues: [ ALMOST_OUT_OF_MEDIA ] }}}}"
        self.media_set_device_status(tray, warning)

    def unload_media(self, tray: str = 'all') -> None:
        """
        Simulate unloading media (OUT_OF_MEDIA) on the specified tray(s),
        and handle sizeType alert confirmations.

        Args:
            tray: 'all' or specific mediaSourceId to target.

        Raises:
            AssertionError: if any tray did not reach 'empty' state.
        """
        logging.info('Unloading media from %s', tray)
        error = "{{{{ idDevice: {device_id}, stateValue: ERROR, statusValues: [ OUT_OF_MEDIA ] }}}}"
        self.media_set_device_status(tray, error)

        # Handle any sizeType alerts that pop up
        try:
            self._media_handling.wait_for_alerts('sizeType', 1)
            self._media_handling.alert_action(category='sizeType', response='ok')
        except Exception:
            logging.info("No sizeType alert to confirm")

        # Pull the inputs array directly from CDM
        inputs = self.get_media_configuration().get('inputs', [])
        # Filter by tray if requested
        configs = inputs if tray == 'all' else [
            cfg for cfg in inputs
            if cfg.get('mediaSourceId') == tray
        ]

        # Assert every targeted tray is now in “empty” state
        empty_states = [cfg.get('stateReason') == 'empty' for cfg in configs]
        assert all(empty_states), (
            "Unloading failed, not all expected trays are empty!"
        )

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
        if status_values is None:
            status_values = ["READY"]
        statuses = ", ".join(status_values)
        payload = f"{{{{ idDevice: {device_id}, stateValue: {state_value}, statusValues: [ {statuses} ] }}}}"
        command = f"EngineSimulatorUw executeSimulatorAction MEDIA setDeviceStatus {payload}"
        logging.info("Executing simulator command: %s", command)
        
        result = self._udw.mainApp.execute(command)  # type: ignore
        if result != "1":
            raise RuntimeError(f"Simulator command failed for device {device_id}: returned '{result}'")


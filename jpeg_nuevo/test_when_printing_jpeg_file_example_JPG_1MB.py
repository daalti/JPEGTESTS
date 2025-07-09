import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaType, MediaOrientation
from dunetuf.configuration import Configuration


class TestWhenPrintingJPEGFile:
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()
        cls.outputsaver = OutputSaver()
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.udw = get_underware_instance(cls.ip_address)
        cls.configuration = Configuration(cls.cdm)
        engine_simulator_ip = get_emulation_ip()
        cls.tcl = TclSocketClient(cls.ip_address, 9104)
        if engine_simulator_ip == 'None':
            logging.debug('Instantiating PrintEmulation: no engineSimulatorIP specified, was -eip not set to emulator/simulator emulation IP?')
            engine_simulator_ip = None
        logging.info('Instantiating PrintEmulation with %s', engine_simulator_ip)
        cls.print_emulation = PrintEmulation(cls.cdm, cls.udw, cls.tcl, engine_simulator_ip)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def setup_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Get media configuration
        self.default_configuration = self.media.get_media_configuration()

    def teardown_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Reset media configuration to default
        self.media.update_media_configuration(self.default_configuration)
    
    def _update_media_input_config(self, default_tray, media_size, media_type):
        """Update media configuration for a specific tray.
        
        Args:
            default_tray: Default tray identifier
            media_size: Media size to set
            media_type: Media type to set
        """
        media_input = self.media.get_media_configuration().get('inputs', [])
        
        for input_config in media_input:
            if input_config.get('mediaSourceId') == default_tray:
                # Handle custom media size configuration
                if media_size == 'custom':
                    supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
                    capability = next(
                        (cap for cap in supported_inputs if cap.get('mediaSourceId') == default_tray),
                        {}
                    )
                    input_config['currentMediaWidth'] = capability.get('mediaWidthMaximum')
                    input_config['currentMediaLength'] = capability.get('mediaLengthMaximum')
                    input_config['currentResolution'] = capability.get('resolution')
                
                # Update media properties
                input_config['mediaSize'] = media_size
                input_config['mediaType'] = media_type
                
                # Update configuration and return early
                self.media.update_media_configuration({'inputs': [input_config]})
                return
        
        logging.warning(f"No media input found for tray: {default_tray}")

    def _get_tray_and_media_sizes(self, tray = None):
        """Get the default tray and its supported media sizes.
        
        Returns:
            tuple: (default_tray, media_sizes) where default_tray is the default source
                   and media_sizes is a list of supported media sizes for that tray
        """
        if tray is None:
            tray = self.media.get_default_source()
        supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((input.get('supportedMediaSizes', []) for input in supported_inputs if input.get('mediaSourceId') == tray), [])
        logging.info('Supported Media Sizes (%s): %s', tray, media_sizes)
        return tray, media_sizes
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple Print job of Jpeg file of 1MB from **
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_example_JPG_1MB.jpg=683a8528125ca09d8314435c051331de2b4c981c756721a2d12c103e8603a1d2
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_file_example_JPG_1MB_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_file_example_JPG_1MB
        +guid:c0307457-53e0-485b-ad44-5be21ea3eadb
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_file_example_JPG_1MB_jpg_then_succeeds(self):

        if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
            installed_trays = self.print_emulation.tray.get_installed_trays()
            selected_tray = None

            # Check each tray for supported sizes
            for tray_id in installed_trays:
                system_tray_id = tray_id.lower().replace('tray', 'tray-')
                tray, media_sizes = self._get_tray_and_media_sizes(system_tray_id)
                if 'anycustom' in media_sizes:
                    selected_tray = tray_id
                    self.print_emulation.tray.open(selected_tray)
                    self.print_emulation.tray.load(selected_tray, "Custom", MediaType.Plain.name,
                                            media_orientation="Portrait")
                    self.print_emulation.tray.close(selected_tray)
                    break

            if selected_tray is None:
                raise ValueError("No tray found supporting anycustom size")
        else:
            capabilities = self.media.get_media_capabilities()
            media_width_maximum = capabilities["supportedInputs"][0]["mediaWidthMaximum"]
            media_length_maximum = capabilities["supportedInputs"][0]["mediaLengthMaximum"]
            media_width_minimum = capabilities["supportedInputs"][0]["mediaWidthMinimum"]
            media_length_minimum = capabilities["supportedInputs"][0]["mediaLengthMinimum"]
            default_tray, media_sizes = self._get_tray_and_media_sizes()
            if 'anycustom' in media_sizes:
                self._update_media_input_config(default_tray, 'anycustom', 'stationery')
            elif 'custom' in media_sizes and media_width_maximum >= 527777 and media_length_maximum >= 351944 and  media_width_minimum <= 527777 and media_length_minimum <= 351944:
                self._update_media_input_config(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('683a8528125ca09d8314435c051331de2b4c981c756721a2d12c103e8603a1d2')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg file example JPG 1MB Page - Print job completed successfully")

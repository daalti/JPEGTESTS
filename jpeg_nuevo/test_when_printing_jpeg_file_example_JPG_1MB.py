import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaType, MediaOrientation
from dunetuf.configuration import Configuration
from jpeg_nuevo.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
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
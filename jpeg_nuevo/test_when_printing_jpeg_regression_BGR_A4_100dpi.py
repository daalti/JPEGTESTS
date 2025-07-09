import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.mapper import PrintMapper
from dunetuf.print.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaSize, MediaType
from jpeg_nuevo.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.outputsaver = OutputSaver()
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.udw = get_underware_instance(cls.ip_address)
        cls.print_mapper = PrintMapper(cls.cdm)
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
    +purpose:Simple print job of Jpeg Regression of BGR A4 100dpi Page from *BGR_A4_100dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:420
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:BGR_A4_100dpi.jpg=04e30e1847278cbccc57f4ac8cc64e657922b47be63fd42874311b453c629f7b
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_BGR_A4_100dpi_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_BGR_A4_100dpi
        +guid:6df55a91-c6b3-4998-a7e0-9c57b8388752
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_BGR_A4_100dpi_jpg_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()
        default_tray, media_sizes = self._get_tray_and_media_sizes()

        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')
        elif 'any' in media_sizes:
            tray_test_name = self.print_mapper.get_media_input_test_name(default_tray)
            self.print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)  # type: ignore
            self._update_media_input_config(default_tray, 'any', 'any')
        else:
            self._update_media_input_config(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('04e30e1847278cbccc57f4ac8cc64e657922b47be63fd42874311b453c629f7b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("JPEG Regression BGR A4 100dpi Page - Print job completed successfully")
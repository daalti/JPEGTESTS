import logging
from dunetuf.print.output_saver import OutputSaver
from dunetuf.configuration import Configuration
from dunetuf.metadata import get_ip
from dunetuf.cdm import get_cdm_instance
from jpeg_nuevo.print_base import TestWhenPrinting



class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.outputsaver = OutputSaver()
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.configuration = Configuration(cls.cdm)

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
    +purpose:Simple print job of Jpeg Regression of untagged cmyk swop 100dpi Page from *untagged_cmyk_swop_100dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:untagged_cmyk_swop_100dpi.jpg=4f9f5dd2775a1a4a733a6a21830b4b257bab151d6971ee664e482c67013d7cda
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_untagged_cmyk_swop_100dpi_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_untagged_cmyk_swop_100dpi
        +guid:680082ee-90b7-4c30-aa12-bb211fece546
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_untagged_cmyk_swop_100dpi_jpg_then_succeeds(self):

        if self.configuration.productname == "jupiter":
            self.outputsaver.operation_mode('CRC')
        else:
            self.outputsaver.operation_mode('TIFF')
            self.outputsaver.validate_crc_tiff()

        default_tray, media_sizes = self._get_tray_and_media_sizes()

        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')

        else:
            self._update_media_input_config(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('4f9f5dd2775a1a4a733a6a21830b4b257bab151d6971ee664e482c67013d7cda')
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        if self.configuration.productname == "jupiter":
            expected_crc = ["0x1408b886"]
            self.outputsaver.verify_output_crc(expected_crc)
        else:
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        self.outputsaver.operation_mode('NONE')
        logging.info("JPEG Regression untagged cmyk swop 100dpi Page - Print job completed successfully")

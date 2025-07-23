import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.metadata import get_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.configuration import Configuration
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
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
        tear_down_output_saver(self.outputsaver)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of Jpeg Regression of AdobeRGB A4 100dpi Page from *AdobeRGB_A4_100dpi.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:AdobeRGB_A4_100dpi.jpg=acc8383b0992e875904aa4c196a4f0ef47ba8e0bfdd0914159876e64f79d2700
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_AdobeRGB_A4_100dpi_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_regression_AdobeRGB_A4_100dpi
            +guid:3ca7a128-1930-48b8-8ae0-cc550e241b53
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_AdobeRGB_A4_100dpi_file_then_succeeds(self):

        if self.configuration.productname == "jupiter":
            self.outputsaver.operation_mode('CRC')
        else:
            self.outputsaver.operation_mode('TIFF')
            self.outputsaver.validate_crc_tiff()

        default_tray = self.media.get_default_source()
        self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('acc8383b0992e875904aa4c196a4f0ef47ba8e0bfdd0914159876e64f79d2700')
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        if self.configuration.productname == "jupiter":
            expected_crc = ["0x9350fdc4"]
            self.outputsaver.verify_output_crc(expected_crc)
        else:
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        self.outputsaver.operation_mode('NONE')

        logging.info("JPEG Regression AdobeRGB A4 100dpi Page - Print job completed successfully")
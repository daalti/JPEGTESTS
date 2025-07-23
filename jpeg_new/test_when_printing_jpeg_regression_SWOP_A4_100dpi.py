import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.configuration import Configuration
from dunetuf.metadata import get_ip
from dunetuf.cdm import get_cdm_instance
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
        +purpose:Simple print job of Jpeg Regression of SWOP A4 100dpi Page from *SWOP_A4_100dpi.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:SWOP_A4_100dpi.jpg=42cf76c1cbe4f91f5f557ffd6670c3438ed8611c5956d3aefcdf5274e3c83193
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_SWOP_A4_100dpi_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_regression_SWOP_A4_100dpi
            +guid:96ac14cd-dd13-4a6c-a1f6-f548b91f972f
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_SWOP_A4_100dpi_file_then_succeeds(self):

        if self.configuration.productname == "jupiter":
            self.outputsaver.operation_mode('CRC')
        else:
            self.outputsaver.operation_mode('TIFF')
            self.outputsaver.validate_crc_tiff()

        default_tray = self.media.get_default_source()
        self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('42cf76c1cbe4f91f5f557ffd6670c3438ed8611c5956d3aefcdf5274e3c83193')
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        if self.configuration.productname == "jupiter":
            expected_crc = ["0xec6ce0e1"]
            self.outputsaver.verify_output_crc(expected_crc)
        else:
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        self.outputsaver.operation_mode('NONE')

        logging.info("JPEG Regression SWOP A4 100dpi Page - Print job completed successfully")
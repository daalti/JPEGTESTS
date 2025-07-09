import pytest
import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver


class TestWhenPrintingJPEGFile:
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()
        cls.outputsaver = OutputSaver()

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
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna without resolution info Page from *lenna_without_resolution_info.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:420
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_without_resolution_info.jpg=e1ed76315e7bfc2c48c28b1efb0fbd0a3b28c333583ce6b477cfcc7da495042c
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_lenna_without_resolution_info_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_lenna_without_resolution_info_jpg_then_succeeds
        +guid:c21142b9-59a4-42c4-84c6-0b940d859a36
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_lenna_without_resolution_info_jpg_then_succeeds(self):

        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff(udw)
        default = tray.get_default_source()
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, "anycustom", 'stationery')

        else:
            tray.configure_tray(default, 'custom', 'stationery')

        self.print.raw.start('e1ed76315e7bfc2c48c28b1efb0fbd0a3b28c333583ce6b477cfcc7da495042c',timeout=420)
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("JPEG TestSuite lenna without resolution info Page - Print job completed successfully")

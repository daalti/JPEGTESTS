import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

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
        +purpose: Print job of file tower_a1.rs **
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-2765, LFPSWQAA-3262
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:tower_a1.rs=abfae6b4e8b5597dd712c14e210626b3fc3f13e040610e704cd0cc2d760a92ab
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_tower_a1_file_then_succeeds
        +test:
            +title:test_rs_tower_a1
            +guid:20ff834f-9121-4ceb-aaea-89a7e150fd28
            +dut:
                +type:Emulator, Simulator
                +configuration:DocumentFormat=RasterStreamICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_tower_a1_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('abfae6b4e8b5597dd712c14e210626b3fc3f13e040610e704cd0cc2d760a92ab')
        self.print.wait_for_job_completion(job_id)
        logging.info("tower_a1.rs - Print job completed successfully")

        expected_crc = ["0xf084787c"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("tower_a1.rs - Checksum(s) verified successfully")

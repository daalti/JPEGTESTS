import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

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
        +purpose:Print job file tower_a1_3pages.rs
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-14986
        +timeout:500
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:tower_a1_3pages.rs=ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_multiple_pages_checksum_file_then_succeeds
        +test:
            +title:test_rs_multiple_pages_checksum
            +guid:5f281eb0-a9e9-46d0-afd8-5280534fb2b4
            +dut:
                +type:Emulator, Simulator
                +configuration:DocumentFormat=RasterStreamICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_multiple_pages_checksum_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689')
        self.print.wait_for_job_completion(job_id)
        logging.info("tower_a1_3pages.rs - Print job completed successfully")

        expected_crc = ["0xf084787c", "0xf084787c", "0xf084787c"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("tower_a1_3pages.rs - Checksum(s) verified successfully")

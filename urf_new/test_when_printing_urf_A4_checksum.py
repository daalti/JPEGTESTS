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
        +purpose: Print job file *A4.urf
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:A4.urf=2b0adec1b1c778ae0f84c76a23f21347a055d2b39ed5b2ee09cd731d321dda06
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_A4_checksum_file_then_succeeds
        +test:
            +title:test_urf_A4_checksum
            +guid:7532f55d-ed2d-4492-94df-ab30a8f6cb67
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=Maia & DocumentFormat=URF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_A4_checksum_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('2b0adec1b1c778ae0f84c76a23f21347a055d2b39ed5b2ee09cd731d321dda06')
        self.print.wait_for_job_completion(job_id)
        logging.info("urf basic file A4.urf - Print job completed successfully")

        expected_crc = ["0x9430ae6e"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        outputsaver.verify_output_crc(expected_crc)
        logging.info("urf basic file A4.urf - Checksum(s) verified successfully")

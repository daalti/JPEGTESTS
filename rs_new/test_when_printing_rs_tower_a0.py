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
        +purpose: A0 rasterstream (.rs) file print
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-14986
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:tower_a0.rs=5bf95e48e5ba0f74b5708008029d5c943aa9516995e52c332d3cf625dc5786ba
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_tower_a0_file_then_succeeds
        +test:
            +title:test_rs_tower_a0
            +guid:54b943ab-a1e9-4a1b-acc3-a79ad91f208a
            +dut:
                +type: Simulator, Emulator
                +configuration: PrintEngineType=Maia & DocumentFormat=RasterStreamICF & MediaSizeSupported=A0_Landscape
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_tower_a0_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('5bf95e48e5ba0f74b5708008029d5c943aa9516995e52c332d3cf625dc5786ba')
        self.print.wait_for_job_completion(job_id)

        printjob.wait_verify_job_completion(jobid, timeout=300)
        logging.info("tower_a0.rs - Print job completed successfully")

        expected_crc = ["0x7a714995"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("tower_a0.rs - Checksum(s) verified successfully")

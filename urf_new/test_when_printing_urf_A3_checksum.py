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
        +purpose:Simple print from a rasterstream (.rs) file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:LFPSWQAA-5221
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:A3.urf=1027b94fbc1e93bcc14c2ab0979902a683e1ce876804fc2c2d71b9201ba3e012
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_A3_checksum_file_then_succeeds
        +test:
            +title:test_urf_A3_checksum
            +guid:b35adad5-47cf-4baa-aa7a-5379963eb228
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_A3_checksum_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('1027b94fbc1e93bcc14c2ab0979902a683e1ce876804fc2c2d71b9201ba3e012')
        self.print.wait_for_job_completion(job_id)
        logging.info("urf basic file A3.urf - Print job completed successfully")

        expected_crc = ["0x88567900"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        outputsaver.verify_output_crc(expected_crc)
        logging.info("urf basic file A3.urf - Checksum(s) verified successfully")

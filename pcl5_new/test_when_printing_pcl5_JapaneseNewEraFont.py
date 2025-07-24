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
        +purpose: Test Japanese New Era Font in PCL5
        +test_tier:3
        +is_manual: False
        +reqid: DUNE-107248
        +timeout: 600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files: JapaneseNewEra_PCL_Test.prn=3739e2db13da0d4d81d504e60001efec297331e8adf8c0d74817477e7b837acf
        +test_classification: System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_JapaneseNewEraFont_file_then_succeeds
        +test:
            +title:test_pcl5_JapaneseNewEraFont
            +guid:62e02baf-b25f-4f73-9328-61358dd1a087
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCL5 

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_JapaneseNewEraFont_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        self.print.raw.start("3739e2db13da0d4d81d504e60001efec297331e8adf8c0d74817477e7b837acf")
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

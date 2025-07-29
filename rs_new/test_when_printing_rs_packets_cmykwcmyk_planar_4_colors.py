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
        +purpose: test_rs_packets_cmykwcmyk_planar_4_colors
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-XXXX
        +timeout:700
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:packets_cmykwcmyk_planar_4_colors.rs=b60ac9e2480c6e0a0f7effcd479a5adb5e21ab0d512b14590281f53c573d4842
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_packets_cmykwcmyk_planar_4_colors_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:RasterStream
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_rs_packets_cmykwcmyk_planar_4_colors
            +guid:c7a47f2f-b4b6-42ab-81f8-88c6d4840a94
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=RasterStreamPlanarICF
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_packets_cmykwcmyk_planar_4_colors_file_then_succeeds(self):
        job_id = self.print.raw.start('b60ac9e2480c6e0a0f7effcd479a5adb5e21ab0d512b14590281f53c573d4842')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("RasterStream job finished")

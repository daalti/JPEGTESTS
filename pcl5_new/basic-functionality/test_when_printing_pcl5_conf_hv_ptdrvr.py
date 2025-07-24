import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_verifier import OutputVerifier
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.outputverifier = OutputVerifier(cls.outputsaver)


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
        +purpose:PCL5 high value test using **ptdrvr.cht
        +test_tier: 1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-156300
        +timeout:140
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:ptdrvr.cht=7a9a8d0aa77ee2c0e71ef7e8a2f133592f5897edcc2194e32bc7ced201f49e36
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_conf_hv_ptdrvr_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl5_conf_hv_ptdrvr
            +guid:04f39416-df5d-40ec-be39-547a51dd9581
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5
        
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_conf_hv_ptdrvr_file_then_succeeds(self):
        job_id = self.print.raw.start('7a9a8d0aa77ee2c0e71ef7e8a2f133592f5897edcc2194e32bc7ced201f49e36')
        self.print.wait_for_job_completion(job_id)
        self.outputverifier.save_and_parse_output()

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
        +purpose:Adding new system tests for PCL5 missing coverage
        +test_tier:1
        +is_manual:False
        +test_classification:1
        +reqid:DUNE-197464
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:com10.pcl=66ab177d91aa66c5ca406812fe4e8d68ed66a73b2b1fa171b4b1b3fa01d84612
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_com10_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl5_com10
            +guid:5a2d78c7-076d-46bb-b39f-e7e6c4afaf63
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCL5

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_com10_file_then_succeeds(self):
        if self.media.is_size_supported('na_number-10_4.125x9.5in','tray-1'):
            self.media.tray.configure_tray('tray-1', 'na_number-10_4.125x9.5in', 'any')
        job_id = self.print.raw.start('66ab177d91aa66c5ca406812fe4e8d68ed66a73b2b1fa171b4b1b3fa01d84612')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output() 

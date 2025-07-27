import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.localization.LocalizationHelper import LocalizationHelper


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
        +purpose:Print of a job wider than supported in Jupiter Clamato_42.pcl of 42 inches (square shaped, auto rotate does not allow printing either) vs 36 inches of max and check it can be cancelled when mismatch screen is prompted.
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-3387
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:Clamato_42.pcl=9c7dc590009b3a2175e987621626cde907dbb6112a011eaa1ec07fc089064ffa
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_Clamato_42_file_then_succeeds
        +test:
            +title:test_when_printing_42_inches_job_wider_than_supported_then_size_mismatch_prompts_and_job_is_canceled_by_user
            +guid:1ddf0321-3001-4415-af2b-a7a6c24bda69
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCL3GUI & DeviceClass=LFP
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl3gui_Clamato_42_file_then_succeeds(self):
        
        # Send job to print
        job_id = printjob.start_print('9c7dc590009b3a2175e987621626cde907dbb6112a011eaa1ec07fc089064ffa')
        
        # Cancel job from mismatch prompt
        spice.job_ui.mismatch_alert_cancel_job()
        job.wait_canceled_job(job_id, job_wait_time = 60)

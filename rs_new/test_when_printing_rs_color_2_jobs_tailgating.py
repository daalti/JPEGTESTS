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
        +purpose:Check 2nd job is printing before 1st job with same PM is finished (tailgating)
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-213703
        +timeout:500
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:SmallFile_lowCompression_-_2191787_L_20x_Generic_Viniyl_4p.prt=6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_color_2_jobs_tailgating_file_then_succeeds
        +test:
            +title:test_rs_color_2_jobs_tailgating
            +guid:cae4e90b-db8f-44cf-8350-3e5ef20b01fe
            +dut:
                +type:Emulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & DeviceClass=LFP
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_color_2_jobs_tailgating_file_then_succeeds(self):

        # Go to Job Queue App screen
        spice.homeMenuUI().goto_job_queue_app_floating_dock(spice)

        # Send first job to print
        job_id = self.print.raw.start('6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06')
        self.print.wait_for_job_completion(job_id)

        # Send second job to print
        job_id = self.print.raw.start('6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06')
        self.print.wait_for_job_completion(job_id)

        ## Check 2nd job is printing before 1st job is finished 
        # Wait for 1st job "Printing" state
        job.wait_for_job_state(first_job_id, "PRINTING", timeout=120)

        # Check 2nd job starts to print while 1st job is still printing
        job.wait_for_job_state(second_job_id, "PRINTING", timeout=120)

        # Wait for 1st job "Curing" state
        job.wait_for_job_state(first_job_id, "DRYING", timeout=120)

        # Check 2nd job continues printing while 1st job is curing
        job.wait_for_job_state(second_job_id, "PRINTING", timeout=120)

        # Wait for both jobs to finish
        job.wait_for_job_state(first_job_id, "SUCCESS", timeout=120)
        job.wait_for_job_state(second_job_id, "SUCCESS", timeout=180)

        # Go to homescreen
        spice.goto_homescreen()

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
        +purpose:Check 1st job is cured before start to prit 2nd job with different PM
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-213727
        +timeout:650
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:SmallFile_lowCompression_-_2191787_L_20x_Generic_Viniyl_4p.prt=6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06
        +external_files:packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_color_2_jobs_different_pm_file_then_succeeds
        +test:
            +title:test_rs_color_2_jobs_different_pm
            +guid:8f80323f-1671-4d4a-9116-b84a434ef117
            +dut:
                +type:Emulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & DeviceClass=LFP
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_color_2_jobs_different_pm_file_then_succeeds(self):

        # Go to Job Queue App screen
        spice.homeMenuUI().goto_job_queue_app_floating_dock(spice)

        # Send first job to print
        job_id = self.print.raw.start('6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06')
        self.print.wait_for_job_completion(job_id)

        # Send second job to print
        job_id = self.print.raw.start('85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8')
        self.print.wait_for_job_completion(job_id)

        ## Check 1st job is cured before starting 2nd job
        # Wait for "Curing" state and then "Success" state
        job.wait_for_job_state(first_job_id, "DRYING", timeout=180)
        job.wait_for_job_state(first_job_id, "SUCCESS", timeout=120)

        # Check 2nd job starts to print
        job.wait_for_job_state(second_job_id, "PREPARINGTOPRINT", timeout=120)
        job.wait_for_job_state(second_job_id, "PRINTING", timeout=120)

        # Wait for second job completion
        self.print.wait_for_job_completion(second_job_id, 300)

        # Go to homescreen
        spice.goto_homescreen()

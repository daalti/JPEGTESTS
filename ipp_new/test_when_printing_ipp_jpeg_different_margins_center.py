import logging

from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

class TestWhenPrintingFileFromIPP(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""
        # no-op unless the legacy file had a matching teardown
        pass

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
        self.media.reset_inputs()

        tear_down_output_saver(self.outputsaver)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Ipp test for printing a JPEG file using attribute value different-margig-settings
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-121987
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:10x12-none.jpg=951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_jpeg_different_margins_center_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_jpeg_different_margins_center
            +guid:84652581-9c22-4a85-bd6c-2383ebf7dce8
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_jpeg_different_margins_center_file_then_succeeds(self):
        expected_vertical_alignment = VerticalContentAlignment.CENTER

        update_dat_file = printjob.copy_file_to_output_folder(PRINT_JPEG_DIFFERENT_MARGINS_TEST_FILE_PATH)

        job_id = self.print.ipp.start(ipp_test_file, '951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_vertical_content_alignment(Intents.printintent, expected_vertical_alignment)


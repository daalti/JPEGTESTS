from dunetuf.print.print_common_types import MediaSize, MediaType
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
        +purpose:Jpeg test using **Webpage_UPD_PRint.JPG
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Webpage_UPD_PRint.JPG=a89ef72d5101dabbf55a0722d57141626372518bfd7fa6b3ba53808ba7d1e0f5
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_Webpage_UPD_PRint_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_webpage_upd_print
            +guid:b9e7e3fc-eda7-4549-ae26-2aafbc29e5df
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_Webpage_UPD_PRint_file_then_succeeds(self):

        job_id = self.print.raw.start('a89ef72d5101dabbf55a0722d57141626372518bfd7fa6b3ba53808ba7d1e0f5')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
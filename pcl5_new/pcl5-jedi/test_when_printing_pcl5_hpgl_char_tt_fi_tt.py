
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
        +purpose: pcl5 hpgl using fi_tt.obj
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:720
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:fi_tt.obj=a5943dfde1f19648bfdbd0277df1836fd7316e47d6cf342535fe6c2622a24898
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_hpgl_char_tt_fi_tt_file_then_succeeds
        +test:
            +title: test_pcl5_hpgl_char_tt_fi_tt
            +guid:5cb1c3a0-056b-49de-aec0-ef2be3558175
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_hpgl_char_tt_fi_tt_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('a5943dfde1f19648bfdbd0277df1836fd7316e47d6cf342535fe6c2622a24898')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

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
        +purpose: pcl5 highvalue using 6Page_rasbars3.obj
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:420
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:6Page-rasbars3.obj=681b7bbb208cf68d854754bf6fcd05f0aacd0c3e08c87538faedad8e6180db7d
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_6page_rasbars3_file_then_succeeds
        +test:
            +title: test_pcl5_highvalue_6page_rasbars3
            +guid:198fffa5-5639-4a0f-bef9-d11e2af1fcc7
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5 & MediaSizeSupported=na_legal_8.5x14in & MediaType=Plain

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_highvalue_6page_rasbars3_file_then_succeeds(self):
            default = self.media.get_default_source()
            if tray.is_media_combination_supported(default, 'na_legal_8.5x14in', 'stationery'):
                self.media.tray.configure_tray(default, 'na_legal_8.5x14in','stationery')

                job_id = self.print.raw.start('681b7bbb208cf68d854754bf6fcd05f0aacd0c3e08c87538faedad8e6180db7d')
                self.print.wait_for_job_completion(job_id)
                self.outputsaver.save_output()
            else:
                # if the media combination is not supported, just print a log and let the test pass
                logging.info("PCL5 na_legal_8.5x14in stationery - Media combination not supported")

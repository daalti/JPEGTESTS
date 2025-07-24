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
        +purpose: pcl5 highvalue using 6Page_raslogp3.obj
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:420
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:6Page-raslogp3.obj=068f39cdd3a14c651d275f16a5675692a7f33f6273bf67dce816995b0b6b90cf
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_6page_raslogp3_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_highvalue_6page_raslogp3
            +guid:c0fe095c-c5cb-4b3a-8911-cc56e4d7295b
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5 & MediaSizeSupported=na_legal_8.5x14in & MediaType=Plain

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_highvalue_6page_raslogp3_file_then_succeeds(self):
            default = self.media.get_default_source()
            if tray.is_media_combination_supported(default, 'na_legal_8.5x14in','stationery'):
                self.media.tray.configure_tray(default, 'na_legal_8.5x14in','stationery')

                job_id = self.print.raw.start('068f39cdd3a14c651d275f16a5675692a7f33f6273bf67dce816995b0b6b90cf')
                self.print.wait_for_job_completion(job_id)
                self.outputsaver.save_output()
            else:
                # if the media combination is not supported, just print a log and let the test pass
                logging.info("PCL5 na_legal_8.5x14in stationery - Media combination not supported")

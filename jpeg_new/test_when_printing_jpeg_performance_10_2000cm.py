import logging
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
        +purpose:Simple print job of Jpeg Performance of 10_2000cm Page from *10_2000cm.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:10_2000cm.jpg=c99290a709203b35b2e7c8520e9764b1648ec79354af4bddfa7aa14b52848dad
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_10_2000cm_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_performance_10_2000cm
            +guid:e9b21578-9d84-4c95-a2c8-78b9dd4855f9
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=Letter

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_10_2000cm_file_then_succeeds(self):

        job_id = self.print.raw.start('c99290a709203b35b2e7c8520e9764b1648ec79354af4bddfa7aa14b52848dad')
        self.print.wait_for_job_completion(job_id)
        logging.info("JPEG Performance 10_2000cm Page - Print job completed successfully")
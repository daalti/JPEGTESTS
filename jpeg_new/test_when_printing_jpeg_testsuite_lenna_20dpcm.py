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
        +purpose:Simple print job of Jpeg TestSuite lenna 20dpcm Page from *lenna_20dpcm.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:lenna_20dpcm.jpg=be12e5937c270ec1d6690cc50cd3e42b1123f0d0fe04a6540e8c3ef19374c305
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_lenna_20dpcm_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_lenna_20dpcm
            +guid:f082e356-5050-4250-ad7e-2afc603c21b8
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_lenna_20dpcm_file_then_succeeds(self):

        job_id = self.print.raw.start('be12e5937c270ec1d6690cc50cd3e42b1123f0d0fe04a6540e8c3ef19374c305')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("JPEG TestSuite lenna 20dpcm Page - Print job completed successfully")
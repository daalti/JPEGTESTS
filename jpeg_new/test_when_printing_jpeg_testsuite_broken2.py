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
        +purpose:Simple print job of Jpeg TestSuite broken2 Page from *broken2.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_broken2_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_broken2
            +guid:7cc20528-d186-4208-b22e-326ffd5ab1ce
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_broken2_file_then_succeeds(self):

        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)
        if "anycustom" in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.AnyCustom, self.media.MediaType.Stationery)
        elif "custom" in media_sizes and self.media.get_media_capabilities()["supportedInputs"][0]["mediaLengthMaximum"] >= 150000:
            # the size of print file should in max/min custom size of printer supported, then could set custom size
            self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("JPEG TestSuite broken2 Page - Print job completed successfully")
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
        +purpose:simple print job of jpeg file of photoimages frequently-usedjpeg pb260776
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_Frequently-usedJPEG_PB260776.JPG=85db63fbd7f31121d4936a1a12d8fab3c76129b226b6d0f75764c0c7ba552f1d
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_Frequently_usedJPEG_PB260776_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_frequently_usedjpeg_pb260776
            +guid:4c36ab7a-3a40-4a31-affb-faeeedfd8949
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_Frequently_usedJPEG_PB260776_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=146751,
            length_max=110063,
            width_min=146751,
            length_min=110063)

        job_id = self.print.raw.start('85db63fbd7f31121d4936a1a12d8fab3c76129b226b6d0f75764c0c7ba552f1d')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg file example photoimages Frequently-usedJPEG PB260776 - Print job completed successfully")
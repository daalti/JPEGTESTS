from jpeg_nuevo.print_base import TestWhenPrinting

import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.outputsaver = OutputSaver()

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

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna 20dpcm EXIF NONE Page from *lenna_20dpcm_EXIF_NONE.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_20dpcm_EXIF_NONE.jpg=cb6e516bebfbd46c2e719ebb1bb3c7f4d49cefb80977a40cc167073712f7ba24
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_lenna_20dpcm_EXIF_NONE_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_20dpcm_EXIF_NONE
        +guid:394c3a98-5cbf-411b-a464-572970c2a347
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_lenna_20dpcm_EXIF_NONE_jpg_then_succeeds(self):

        default_tray, media_sizes = self._get_tray_and_media_sizes()
        default_size = self.media.get_default_size(default_tray)

        if default_size in media_sizes:
            logging.info(f"Set paper tray <{default_tray}> to paper size <{default_size}>")
            self._update_media_input_config(default_tray, default_size, 'stationery')

        job_id = self.print.raw.start('cb6e516bebfbd46c2e719ebb1bb3c7f4d49cefb80977a40cc167073712f7ba24')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("JPEG TestSuite lenna 20dpcm EXIF NONE Page - Print job completed successfully")
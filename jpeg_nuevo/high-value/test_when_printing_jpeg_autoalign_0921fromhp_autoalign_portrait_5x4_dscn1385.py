import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from jpeg_nuevo.print_base import TestWhenPrinting


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
    +purpose: simple print job of jpeg file of autoalign 0921fromhp autoalign portrait 5x4 dscn1385
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:autoAlign_0921fromHP_AutoAlign_Portrait_5x4_DSCN1385.JPG=44ffc42c2d40cc0e77340abccd78e6de628f0de5bbea5e7ded8137605a70ed7e
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_autoAlign_0921fromHP_AutoAlign_Portrait_5x4_DSCN1385_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_autoalign_0921fromhp_autoalign_portrait_5x4_dscn1385
        +guid:8dbb4840-78ce-4121-9da2-7b14ea1c9b1f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_autoAlign_0921fromHP_AutoAlign_Portrait_5x4_DSCN1385_JPG_then_succeeds(self):

        default_tray, media_sizes = self._get_tray_and_media_sizes()

        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')
        else:
            self._update_media_input_config(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('44ffc42c2d40cc0e77340abccd78e6de628f0de5bbea5e7ded8137605a70ed7e')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg autoAlign 0921fromHP AutoAlign Portrait 5x4 DSCN1385 file")
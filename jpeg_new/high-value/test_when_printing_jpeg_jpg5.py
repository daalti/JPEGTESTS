import logging
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
        +purpose: simple print job of jpeg file of jpg5
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:jpg5.jpg=9d133dde6eb25f2e326e6b72839242a8727e0cf1b64b882f4935a73d1f3cae14
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_jpg5_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_jpg5
            +guid:1320982a-cffd-4554-9413-b986ff364f6f
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_jpg5_file_then_succeeds(self):

        if self.get_platform() == 'emulator':
            installed_trays = self.media.tray.get()
            selected_tray = None

            for tray_id in installed_trays:
                system_tray_id = tray_id.lower().replace('tray', 'tray-')
                media_sizes = self.media.get_media_sizes(system_tray_id)
                if "anycustom" in media_sizes:
                    selected_tray = tray_id
                    break

            if selected_tray is None:
                raise ValueError("No tray found supporting anycustom in enterprise emulator")

            self.media.tray.load(selected_tray, self.media.MediaSize.Custom, self.media.MediaType.Plain, need_open=True)

        self.load_custom_tray(
            width_max=453333,
            length_max=340000,
            width_min=453333,
            length_min=340000
        )

        job_id = self.print.raw.start('9d133dde6eb25f2e326e6b72839242a8727e0cf1b64b882f4935a73d1f3cae14')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg photoimages resolution tif tif1024x768 file")
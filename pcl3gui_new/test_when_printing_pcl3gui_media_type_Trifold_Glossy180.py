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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Print job which exercises driverware for com.hp-trifold-brochure-glossy-180gsm Media Types  using a US letter normal 1-page PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-6338
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:HP_Tri-fold_Brochure_Paper_Glossy.pcl=b982c46ef54f82835347f7908c57c162a3ca7e13cb10b01e73a92a2217748c7a
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_media_type_Trifold_Glossy180_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_media_type_Trifold_Glossy180
            +guid:c0335e28-cfed-428c-b203-1c1e70445b2c
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_media_type_Trifold_Glossy180_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('na_letter_8.5x11in', default) and self.media.tray.is_type_supported('com.hp-trifold-brochure-glossy-180gsm', default):
            self.media.tray.configure_tray(default, 'na_letter_8.5x11in', 'com.hp-trifold-brochure-glossy-180gsm')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('b982c46ef54f82835347f7908c57c162a3ca7e13cb10b01e73a92a2217748c7a')

        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("PCL3GUI Media Type trifold-brochure-glossy-180gsm US letter normal 1-pagecompleted successfully")

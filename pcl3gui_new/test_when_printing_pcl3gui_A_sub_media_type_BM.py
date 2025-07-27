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
        +purpose:Print job which exercises driverware for Sub Media Types HP brochure-matte using a US letter normal 1-page PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-6338
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Wedding_Vision_A_HPBroch_Matte_N.pcl=9fb185eeb0b0ce592a873f0a2f17ccb7c231a5add0dd930ad0468a7243312031
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_A_sub_media_type_BM_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_sub_media_type_brochure_matte
            +guid:8137e6d5-1b1e-4cdb-9f58-51640e789d14
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_A_sub_media_type_BM_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('na_letter_8.5x11in', default) and self.media.tray.is_type_supported('com.hp-matte-brochure', default):
            self.media.tray.configure_tray(default, 'na_letter_8.5x11in', 'com.hp-matte-brochure')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('9fb185eeb0b0ce592a873f0a2f17ccb7c231a5add0dd930ad0468a7243312031')

        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("PCL3GUI Sub Media Type HP brochure-matte US letter normal 1-pagecompleted successfully")

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
    
        +purpose: Simple print job of a A4 plain 5-Page PCL3GUI file 
        +test_tier:1
        +is_manual:False
        +test_classification: System
        +reqid: DUNE-174492
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:MMVertical 
        +test_framework:TUF 
        +external_files: EET_Plain_N_A4_Simplex_5pgs_.pcl=3c0b496acf86b1b7a054d34b4b81211c9c8cb9b75d00432b44960fe4564a12fc
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_A4_Simplex_5pgs_file_then_succeeds
        +test:
            +title:test_pcl3gui_A4_Simplex_5pgs
            +guid:af19f4b3-898f-459c-96a7-b722c3238f9f
            +dut:
                +type:Engine
                +configuration: DocumentFormat=PCL3GUI
        +overrides:
            +Home:
                +is_manual:False
                +timeout:240
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_A4_Simplex_5pgs_file_then_succeeds(self):
        self.media.tray.reset_trays()

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('3c0b496acf86b1b7a054d34b4b81211c9c8cb9b75d00432b44960fe4564a12fc')

        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()

        logging.info("PCL3GUI A4 Simplex 5-page print completed successfully")

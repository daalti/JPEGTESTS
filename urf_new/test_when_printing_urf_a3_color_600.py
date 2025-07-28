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
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C52178020 Simple print job of urf A3 Color 600 from *A3_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:A3_Color_600.urf=974aee85965b8d8cb63584d8661e1d87c0d57893c6447dc010a49e4b9961a7dd
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_a3_color_600_file_then_succeeds
        +test:
            +title:test_urf_a3_color_600_page
            +guid:ab3daeee-94ff-43ac-af52-838210cf4b9c
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF
        +overrides:
            +Home:
                +is_manual:False
                +timeout:300
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_a3_color_600_file_then_succeeds(self):
        self.outputsaver.operation_mode('TIFF')

        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('iso_a3_297x420mm', default):
            self.media.tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('974aee85965b8d8cb63584d8661e1d87c0d57893c6447dc010a49e4b9961a7dd')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc() 
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')
        self.media.tray.reset_trays()

        logging.info("URF A3 Color 600 page - Print job completed successfully")

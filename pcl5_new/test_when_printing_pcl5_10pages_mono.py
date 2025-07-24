import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents, MediaType, MediaSize, ColorMode


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
        +purpose:Simple print job of Pcl5 letter Page from 10pgs_Letter_Plain.prn file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-223392
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:10pgs_Letter_Plain.prn=81b00eaa2f06be2bdf7b27f025c6b703da3c600b4fdb28a06086f0bb4236af47
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_10pages_mono_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl5_10pages_mono
            +guid:447b72e9-d0d2-4fb4-86c6-57a69e8dec14
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_10pages_mono_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()

        default = self.media.get_default_source()
        if tray.is_media_combination_supported(default, 'na_letter_8.5x11in', 'stationery'):
             self.media.tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
             job_id = self.print.raw.start('81b00eaa2f06be2bdf7b27f025c6b703da3c600b4fdb28a06086f0bb4236af47')
             self.print.wait_for_job_completion(job_id)

             outputverifier.save_and_parse_output()
             outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
             outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
             outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
             self.outputsaver.operation_mode('NONE')

             Current_crc_value = self.outputsaver.get_crc()
             assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        else:
            logging.info('Media size na_letter_8.5x11in is not supported in the default tray')    

        self.media.tray.reset_trays()


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

"""$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-MarginLRTB-5.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MarginLRTB-5.pwg=06c3a98244287f7cb60e448a13839364c570e66a75cf7b8834adc1d705de5eda
    +name:TestWhenPrintingJPEGFile::test_when_using_pwg_ph_only_margin_lrtb_5_file_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_phonly_margin_lrtb_5
        +guid:c63ff7cc-cdde-4e70-9ae9-3d4f67b23bf0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & MediaSizeSupported=na_executive_7.25x10.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$"""
    def test_when_using_pwg_ph_only_margin_lrtb_5_file_then_succeeds(self):
        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)
        if self.media.MediaSize.EXECUTIVE in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.EXECUTIVE, self.media.MediaType.Stationery)
        job_id = self.print.raw.start('06c3a98244287f7cb60e448a13839364c570e66a75cf7b8834adc1d705de5eda')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

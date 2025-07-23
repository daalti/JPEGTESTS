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
    +purpose:Simple print job of pwg a4 600x8 mono one page from *a4-600x8-mono-1p-sim.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a4-600x8-mono-1p-sim.pwg=706dc4ec7cc7102294bd874d627301bbbb8e84c18378528ffd59ba63639f1697
    +name:TestWhenPrintingJPEGFile::test_when_using_pwg_a4_600x8_mono_1_page_sim_file_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_a4_600x8_mono_one_page
        +guid:66ea988b-2d8a-4a0c-bf7c-f35a03f90b1e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pwg_a4_600x8_mono_1_page_sim_file_then_succeeds(self):

        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)
        if self.media.MediaSize.A4 in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.A4, self.media.MediaType.Plain)

        job_id = self.print.raw.start('706dc4ec7cc7102294bd874d627301bbbb8e84c18378528ffd59ba63639f1697')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

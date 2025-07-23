import logging
from dunetuf.print.print_common_types import MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

from dunetuf.print.print_common_types import MediaInputIds, MediaType

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
        +purpose:Jpeg test using **2686.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:2686.jpg=e7a41c713330895d538595fbf74af4f7ac88a25424abb103beb3872d54cc0bfa
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_2686_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_2686
            +guid:509d2f16-419c-4b31-a547-b1eccae1848f
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
    def test_when_using_2686_file_then_succeeds(self):

        if self.get_platform() == 'emulator':
            media_sizes = self.media.get_media_sizes('tray-1')
            if "anycustom" in media_sizes:
                self.media.tray.load(self.media.MediaInputIds.Tray1.name, self.media.MediaSize.Custom, self.media.MediaType.Plain, need_open=True)
        
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('e7a41c713330895d538595fbf74af4f7ac88a25424abb103beb3872d54cc0bfa')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
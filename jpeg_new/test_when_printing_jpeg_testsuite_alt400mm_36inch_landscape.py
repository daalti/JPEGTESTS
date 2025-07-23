import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel
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
        +purpose:Simple print job of Jpeg TestSuite alt400mm 36inch landscape Page from *alt400mm_36inch_landscape.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:alt400mm_36inch_landscape.jpg=8cb2e40ad94a931c43c9c6253ef7f367aa54cabf7b96a09a581c5b621fd00902
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_alt400mm_36inch_landscape_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_alt400mm_36inch_landscape
            +guid:f48c4310-dc97-4b1b-9ae4-cc70d78f3ee2
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
    def test_when_using_alt400mm_36inch_landscape_file_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()
        if self.get_platform() == 'emulator':
            installed_trays = self.media.tray.get()
            for tray_id in installed_trays:
                self.media.tray.load(tray_id, self.media.MediaSize.A4, self.media.MediaType.Plain)

        job_id = self.print.raw.start('8cb2e40ad94a931c43c9c6253ef7f367aa54cabf7b96a09a581c5b621fd00902')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("JPEG TestSuite alt400mm 36inch landscape Page - Print job completed successfully")
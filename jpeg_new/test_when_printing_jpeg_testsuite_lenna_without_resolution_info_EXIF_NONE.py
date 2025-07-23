import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.mapper.mapper import PrintMapper
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaSize, MediaType
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.print_mapper = PrintMapper(cls.cdm)

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
        +purpose:Simple print job of Jpeg TestSuite lenna without resolution info EXIFNONE Page from *lenna_without_resolution_info_EXIF_NONE.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:420
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:lenna_without_resolution_info_EXIF_NONE.jpg=0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_lenna_without_resolution_info_EXIF_NONE_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_lenna_without_resolution_info_EXIF_NONE
            +guid:7c85c118-93fa-45fb-ae18-3cc71224dd5b
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_lenna_without_resolution_info_EXIF_NONE_file_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()
        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)

        if "anycustom" in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.AnyCustom, self.media.MediaType.Stationery)
        elif "any" in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.Any, self.media.MediaType.Any)
        else:
            self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("JPEG TestSuite lenna without resolution info EXIF NONE Page - Print job completed successfully")
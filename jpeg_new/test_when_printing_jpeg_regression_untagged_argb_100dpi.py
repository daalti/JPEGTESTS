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
from dunetuf.configuration import Configuration
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
        cls.udw = get_underware_instance(cls.ip_address)
        cls.configuration = Configuration(cls.cdm)
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
        +purpose:C52178011 Simple print job of Jpeg Regression of untagged argb 100dpi Page from *untagged_argb_100dpi.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:400
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:untagged_argb_100dpi.jpg=d91801b4c08f2ed918a3cbf885a61c8721cace99b0e83a2f82e95660e2275704
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_untagged_argb_100dpi_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_regression_untagged_argb_100dpi
            +guid:dbf7757a-264e-4e71-8863-ba0115a9b456
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
            +ProA4:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_untagged_argb_100dpi_file_then_succeeds(self):

        if self.configuration.productname == "jupiter":
            self.outputsaver.operation_mode('CRC')
        else:
            self.outputsaver.operation_mode('TIFF')
        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            installed_trays = self.media.tray.get()
            for tray_id in installed_trays:
                system_tray_id = tray_id.lower().replace('tray', 'tray-')
                media_sizes = self.media.get_media_sizes(system_tray_id)
                if "anycustom" in media_sizes:
                    self.media.tray.load(system_tray_id, self.media.MediaSize.Custom, self.media.MediaType.Plain, media_orientation="Portrait", need_open=True)
                    break
        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)

        if "any"in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.Any, self.media.MediaType.Any)
        elif "anycustom" in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.AnyCustom, self.media.MediaType.Stationery)
        else:
            self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)
        self.outputsaver.validate_crc_tiff() 
        job_id = self.print.raw.start('d91801b4c08f2ed918a3cbf885a61c8721cace99b0e83a2f82e95660e2275704')
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        if self.configuration.productname == "jupiter":
            expected_crc = ["0x9350fdc4"]    
            self.outputsaver.verify_output_crc(expected_crc)
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc() 
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')

        logging.info("JPEG Regression untagged argb 100dpi Page - Print job completed successfully")
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation


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
        +purpose:Simple print job of urf 8_5x13 color 300 page from *8_5x13_Color_300.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:8_5x13_Color_300.urf=df0ad3eee183375bd2f24ff7e5794783527f7182fb1e502970b93a4c9e140f40
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_8_5x13_color_300_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_8_5x13_color_300_page
            +guid:a52dc262-620b-4f1b-80db-267c8ca22312
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_8_5x13_color_300_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()

        default = self.media.tray.get_default_source()
        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if self.media.tray.is_size_supported('na_foolscap_8.5x13in', default):
            if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
                tray1 = MediaInputIds.Tray1.name
                self.media.tray.open(tray1)
                self.media.tray.load(tray1, MediaSize.EightPointFiveByThirteen.name, MediaType.Plain.name)
                self.media.tray.close(tray1)
            else:
                self.media.tray.configure_tray(default, 'na_foolscap_8.5x13in', 'stationery')
        elif self.media.tray.is_size_supported('custom', default) and media_width_maximum >= 85000 and media_length_maximum >= 130000 and  media_width_minimum <= 85000 and media_length_minimum <= 130000:
            self.media.tray.configure_tray(default, 'custom', 'stationery')


        job_id = self.print.raw.start('df0ad3eee183375bd2f24ff7e5794783527f7182fb1e502970b93a4c9e140f40')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.media.tray.reset_trays()

        logging.info("URF 8_5x13 Color 300 page - Print job completed successfully")

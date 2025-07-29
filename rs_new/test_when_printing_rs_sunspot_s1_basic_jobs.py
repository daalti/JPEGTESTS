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
        +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a basic job without white
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-114994
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:color_basic_CMYKLites.rs=8bc2bb983f2403da91bf59239bffd046943b06b7f872353d9d0a8b416bb95c87
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_color_basic_cmyklites_job_print_file_then_succeeds
        +test:
            +title:test_rs_color_basic_cmyklites_job_print
            +guid:4d2e31bb-fa6e-42db-aac7-4b9acbf2fed8
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=RasterStreamPlanarICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_color_basic_cmyklites_job_print_file_then_succeeds(self):

        # Avoid the error from the supplies handling component for print a job color with white ph
        print(tcl.execute("SuppliesHandlingManagerUw setByPassMode"))

        # CRC will be calculated using the payload of the RasterData
        self.outputsaver.operation_mode('CRC')

        self.print.raw.start("8bc2bb983f2403da91bf59239bffd046943b06b7f872353d9d0a8b416bb95c87", timeout=120)
        logging.info("color_basic_CMYKLites.rs - Print job completed successfully")

        expected_crc = ["0x59414912"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("color_basic_CMYKLites.rs - Checksum(s) verified successfully")

        # Enable checks at supplies handling component
        print(tcl.execute("SuppliesHandlingManagerUw setCheckMode"))



    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a white job in mode spot
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-114994
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:white_basic_SPOT_v2_OK.rs=aa50b55926fe642d96ca80041ef124d320c8ce9ff0797b24fcae828fe43e20a4
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_white_basic_spot_job_print_file_then_succeeds
        +test:
            +title:test_rs_white_basic_spot_job_print
            +guid:3b4f68f2-cf59-4236-b10d-c8c5d4efa634
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_white_basic_spot_job_print_file_then_succeeds(self):

        # CRC will be calculated using the payload of the RasterData
        self.outputsaver.operation_mode('CRC')

        # Configure the simulator with adhesive transparent media
        self.media.tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")

        self.print.raw.start("aa50b55926fe642d96ca80041ef124d320c8ce9ff0797b24fcae828fe43e20a4", timeout=120)
        logging.info("white_basic_SPOT_v2_OK.rs - Print job completed successfully")

        expected_crc = ["0x2a648a1f"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("white_basic_SPOT_v2_OK.rs - Checksum(s) verified successfully")



    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a white job in mode underflood and whiteshrink disabled
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-114994
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:white_basic_no_spot_UF_wshrink_disabled.rs=b901b7b736492ff53ee3a4269e836d89df4e22d8cd07c9b14ecde87c3a8a3094
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_white_basic_underflood_disabled_whiteshrink_job_print_file_then_succeeds
        +test:
            +title:test_rs_white_basic_underflood_disabled_whiteshrink_job_print
            +guid:3a2e0179-55d1-4496-83c6-0caa3add0d67
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_white_basic_underflood_disabled_whiteshrink_job_print_file_then_succeeds(self):

        # CRC will be calculated using the payload of the RasterData
        self.outputsaver.operation_mode('CRC')

        # Configure the simulator with adhesive transparent media
        self.media.tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")

        self.print.raw.start("b901b7b736492ff53ee3a4269e836d89df4e22d8cd07c9b14ecde87c3a8a3094", timeout=120)
        logging.info("white_basic_no_spot_UF_wshrink_disabled.rs - Print job completed successfully")

        expected_crc = ["0x2a648a1f"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("white_basic_no_spot_UF_wshrink_disabled.rs - Checksum(s) verified successfully")



    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a white job in mode underflood and whiteshrink enabled
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-114994
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:white_basic_no_spot_UF_wshrink_enabled.rs=f49dc7a6b330c9f10a2ae964c35c80c8a80e6b7860917954593eb854d52d2b45
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_white_basic_underflood_enabled_whiteshrink_job_print_file_then_succeeds
        +test:
            +title:test_rs_white_basic_underflood_enabled_whiteshrink_job_print
            +guid:834dfcde-ae30-4f21-9b79-1d62d356ffc3
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_white_basic_underflood_enabled_whiteshrink_job_print_file_then_succeeds(self):

        # CRC will be calculated using the payload of the RasterData
        self.outputsaver.operation_mode('CRC')

        self.print.raw.start("f49dc7a6b330c9f10a2ae964c35c80c8a80e6b7860917954593eb854d52d2b45", timeout=120)
        logging.info("white_basic_no_spot_UF_wshrink_enabled.rs - Print job completed successfully")

        expected_crc = ["0xe54c6249"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("white_basic_no_spot_UF_wshrink_enabled.rs - Checksum(s) verified successfully")



    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a white job in mode sandwich
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-114994
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:white_japan_SANDWICH_sw3l.rs=65728c71f41a75e5184681ebf962957baaef56d4fb5c5126639654cc136d09a4
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_white_sandwich_sw3l_job_print_file_then_succeeds
        +test:
            +title:test_rs_white_sandwich_sw3l_job_print
            +guid:b85cf4a4-02f5-42d8-9fe4-38b3f51cddd0
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_white_sandwich_sw3l_job_print_file_then_succeeds(self):

        # CRC will be calculated using the payload of the RasterData
        self.outputsaver.operation_mode('CRC')

        # Configure the simulator with adhesive transparent media
        self.media.tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")

        self.print.raw.start("65728c71f41a75e5184681ebf962957baaef56d4fb5c5126639654cc136d09a4", timeout=120)
        logging.info("white_japan_SANDWICH_sw3l.rs - Print job completed successfully")

        expected_crc = ["0x32c51ce0"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("white_japan_SANDWICH_sw3l.rs - Checksum(s) verified successfully")

"""
"""
"""
"""

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
        +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a sandwich job.
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-6621
        +timeout:1000
        +asset:PDL_New
        +test_framework:TUF
        +delivery_team:QualityGuild
        +feature_team:ProductQA
        +external_files:JapanSandwich-SW3L-W10060p110-CMYKWCMYK-600.prt=ffe6b8879c296c095b90f1bed48672cd349097204b14fc1f3fcd9e7d36a3ce16
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_JapanSandwich_SW3L_W10060p110_CMYKWCMYK_600_file_then_succeeds
        +test:
            +title:test_rs_JapanSandwich_SW3L_W10060p110_CMYKWCMYK_600
            +guid:eb1e9266-c595-47be-8bbb-b4d0a8b200a5
            +dut:
                +type:Simulator, Emulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_JapanSandwich_SW3L_W10060p110_CMYKWCMYK_600_file_then_succeeds(self):

        try:
            self.media.tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")
        except:
            tclMaia.execute("setMediaLoaded ROLL 64 150106")

        # CRC will be calculated using the payload of the RasterData
        self.outputsaver.operation_mode('CRC')

        self.print.raw.start("ffe6b8879c296c095b90f1bed48672cd349097204b14fc1f3fcd9e7d36a3ce16", timeout=1000)
        logging.info("JapanSandwich-SW3L-W10060p110-CMYKWCMYK-600.prt - Print job completed successfully")

        expected_crc = ["0xb76d8835"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("JapanSandwich-SW3L-W10060p110-CMYKWCMYK-600.prt - Checksum(s) verified successfully")

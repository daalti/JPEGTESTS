import logging
from dunetuf.print.output_saver import OutputSaver
from jpeg_nuevo.print_base import TestWhenPrinting

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.outputsaver = OutputSaver()

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
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file *sRGB_A4_600dpi.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_sRGB_A4_600dpi_jpg_then_succeeds
    +test:
        +title:test_jpg_sRGB_A4_600dpi_checksum
        +guid:06f3c688-6112-4fa8-b408-dec92505b062
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=JPEG
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_sRGB_A4_600dpi_jpg_then_succeeds(self):


        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b')
        self.print.wait_for_job_completion(job_id)
        logging.info("basic file sRGB_A4_600dpi.jpg - Print job completed successfully")

        expected_crc = ["0x35d1f2ef"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)        logging.info("basic file sRGB_A4_600dpi.jpg - Checksum(s) verified successfully")

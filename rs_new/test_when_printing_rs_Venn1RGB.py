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
        +purpose: Print job of file Venn1RGB.rs **
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-2765
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ProductQA
        +test_framework:TUF
        +external_files:Venn1RGB.rs=e4b093935481c7ec9e428194a9c7fa475558e18104bb66dfdd4736b81906f3a5
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_Venn1RGB_file_then_succeeds
        +test:
            +title:test_rs_Venn1RGB
            +guid:a0326124-3b25-43c5-ace8-24a2f7f276fe
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_Venn1RGB_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('e4b093935481c7ec9e428194a9c7fa475558e18104bb66dfdd4736b81906f3a5')
        self.print.wait_for_job_completion(job_id)
        logging.info("RS Venn1RGB - Print job completed successfully")

        expected_crc = ["0xc4cbd5fe"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("RS Venn1RGB - Checksum(s) verified successfully")

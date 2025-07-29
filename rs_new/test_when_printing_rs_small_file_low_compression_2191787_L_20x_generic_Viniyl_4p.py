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
        +purpose: test_rs_small_file_low_compression_2191787_L_20x_generic_Viniyl_4p
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-5338
        +timeout:300
        +asset:PDL_New
        +test_framework:TUF
        +delivery_team:QualityGuild
        +feature_team:ProductQA
        +external_files:SmallFile_lowCompression_-_2191787_L_20x_Generic_Viniyl_4p.prt=6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_small_file_low_compression_2191787_L_20x_generic_Viniyl_4p_file_then_succeeds
        +test:
            +title:test_rs_small_file_low_compression_2191787_L_20x_generic_Viniyl_4p
            +guid:a2b24c16-a86e-43c0-a4f1-7cb8ecb0079d
            +dut:
                +type:Simulator, Emulator
                +configuration: DocumentFormat=RasterStreamPlanarICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_small_file_low_compression_2191787_L_20x_generic_Viniyl_4p_file_then_succeeds(self):

        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('6783c5b8d5e202588f1785f3a057dd3a7cfc2129874723bd56c1d65644842d06')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        expected_crc = ["0x20ff185f"]

        #Verify that obtained checksums are the expected ones
        self.outputsaver.verify_output_crc(expected_crc)

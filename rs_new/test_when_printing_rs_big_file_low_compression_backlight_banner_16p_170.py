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
        +purpose: test_rs_big_file_low_compression_backlight_banner_16p_170
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-5338
        +timeout:550
        +asset:PDL_New
        +test_framework:TUF
        +delivery_team:QualityGuild
        +feature_team:ProductQA
        +external_files:BigFile_lowCompression_-_generic_backlight_banner_16p_170.prt=e27854b4d4819ec20694c85a6396bc4e15aafd121587e46e6ee4495860727ae9
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_big_file_low_compression_backlight_banner_16p_170_file_then_succeeds
        +test:
            +title:test_rs_big_file_low_compression_backlight_banner_16p_170
            +guid:3e22a5a4-f0ad-407f-9457-c90d949d350a
            +dut:
                +type:Simulator, Emulator
                +configuration: DocumentFormat=RasterStreamPlanarICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_big_file_low_compression_backlight_banner_16p_170_file_then_succeeds(self):

        try:
            self.media.tray.load_simulator_media(tcl, "PVC_BANNER_BACKLIT", "101100")
        except:
            tclMaia.execute("setMediaLoaded ROLL 64 101100")

        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('e27854b4d4819ec20694c85a6396bc4e15aafd121587e46e6ee4495860727ae9')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        expected_crc = ["0xd2752d17"]

        #Verify that obtained checksums are the expected ones
        self.outputsaver.verify_output_crc(expected_crc)

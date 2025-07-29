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
        +purpose:Print job file Cannabi_Gold_Sticker_SMALL_MOSAICO.tif--8p_6c_36ng.rst
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-4072
        +timeout:800
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:Cannabi_Gold_Sticker_SMALL_MOSAICO.tif--8p_6c_36ng.rst=fda544f509127aed115c2f9291f057e16b793b52c79a43d9352fa94079f9f6c9
        +test_classification:system
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_cannabi_gold_checksum_file_then_succeeds
        +test:
            +title:test_rs_cannabi_gold_checksum
            +guid:e865b593-c788-44db-a529-7d6d2abbe41c
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=MaiaLatex & DocumentFormat=RasterStreamPlanarICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_cannabi_gold_checksum_file_then_succeeds(self):

        # Avoid the error from the supplies handling component when printing a color job with white ph
        print(tcl.execute("SuppliesHandlingManagerUw setByPassMode"))

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('fda544f509127aed115c2f9291f057e16b793b52c79a43d9352fa94079f9f6c9')
        self.print.wait_for_job_completion(job_id)
        logging.info("rs Cannabi_Gold_Sticker_SMALL_MOSAICO.tif--8p_6c_36ng.rst - Print job completed successfully")

        expected_crc = ["0xb193b7ed"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("rs Cannabi_Gold_Sticker_SMALL_MOSAICO.tif--8p_6c_36ng.rst - Checksum(s) verified successfully")

        # Enable checks at supplies handling component
        print(tcl.execute("SuppliesHandlingManagerUw setCheckMode"))

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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Print job file ST212-03-CAD-PlantaPCI-6copies-A1L-FAST-rev5_-2_600.prn and verify
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-61462
        +timeout:800
        +asset:PDL_New
        +test_framework:TUF
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +external_files:ST212-03-CAD-PlantaPCI-6copies-A1L-FAST-rev5_-2_600.prn=28464adb04de938485bcc320bafc6286e330e0670aba47c35574b871922036ec
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3Gui_ST212_03_CAD_PlantaPCI_6copies_A1L_FAST_rev5_2_600_file_then_succeeds
        +test:
            +title:test_pcl3Gui_ST212_03_CAD_PlantaPCI_6copies_A1L_FAST_rev5_2_600
            +guid:cc143ddb-e5e4-446e-ab04-54ffe19f4558
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCL3GUI&EngineFirmwareFamily=Maia
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3Gui_ST212_03_CAD_PlantaPCI_6copies_A1L_FAST_rev5_2_600_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('28464adb04de938485bcc320bafc6286e330e0670aba47c35574b871922036ec')

        self.print.wait_for_job_completion(job_id)

        logging.info("ST212-03-CAD-PlantaPCI-6copies-A1L-FAST-rev5_-2_600.prn - Print job completed successfully")

        expected_crc = ["0x6d2beb27", "0x6d2beb27", "0x6d2beb27", "0x6d2beb27", "0x6d2beb27", "0x6d2beb27"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("ST212-03-CAD-PlantaPCI-6copies-A1L-FAST-rev5_-2_600.prn - Print job completed successfully")

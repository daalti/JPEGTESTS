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
        +purpose:Simple print job on roll PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:LFPSWQAA-4560
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:printOnroll.pcl=1e2d69d97d836018adf7be895a70abcdd0750b7af5041e185ded88b3e0bcfc4e
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_print_on_roll_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_print_on_roll
            +guid:6a18305d-2036-49bb-9ac4-09465d20688e
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI&DeviceClass=MFP & MediaInputInstalled=MainRoll
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_print_on_roll_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('1e2d69d97d836018adf7be895a70abcdd0750b7af5041e185ded88b3e0bcfc4e')
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        
        # CRC check
        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')

        logging.info("PCL3GUI print on roll successfully")

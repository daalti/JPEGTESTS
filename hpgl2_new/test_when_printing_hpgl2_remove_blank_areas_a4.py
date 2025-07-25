import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents


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
        +purpose: Print HPGL2 job with remove blank areas option and verify CRC
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-191746
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:RemoveBlankAreas_A4.prn=61dc742badda5ee1c47295e49430cb7ca91632b96fbb812a72de3eb024fbccb6
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_hpgl2_remove_blank_areas_a4_file_then_succeeds
        +test:
            +title:test_hpgl2_remove_blank_areas_a4
            +guid:a520752e-8792-42f0-9dbd-03b611205ff3
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=HPGL2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_hpgl2_remove_blank_areas_a4_file_then_succeeds(self):

        logging.info('Running test_hpgl2_remove_blank_areas_a4')

        outputverifier.outputsaver.operation_mode('CRC')
        job_id = self.print.raw.start('61dc742badda5ee1c47295e49430cb7ca91632b96fbb812a72de3eb024fbccb6')
        self.print.wait_for_job_completion(job_id)
        logging.info("RemoveBlankAreas_A4.prn - Print job completed successfully")

        ### VERIFY
        if outputverifier.outputsaver.configuration.productname == "jupiter":
            expected_crc = ["0x4ac00c32"]
        else:
            expected_crc = ["0x8f39bf53"]

        # Read and verify that obtained checksums are the expected ones
        outputverifier.save_and_parse_output()
        outputverifier.outputsaver.verify_output_crc(expected_crc)
        logging.info("RemoveBlankAreas_A4.prn - Checksum(s) verified successfully")

        # Verify margins
        outputverifier.verify_top_margin(Intents.printintent, 119)
        outputverifier.verify_bottom_margin(Intents.printintent, 119)
        outputverifier.verify_left_margin(Intents.printintent, 119)
        outputverifier.verify_right_margin(Intents.printintent, 119)

        # Verify page size
        outputverifier.verify_page_width(Intents.printintent, 2800)
        outputverifier.verify_page_height(Intents.printintent, 2865)

        logging.info("RemoveBlankAreas_A4.prn - Dimensions verified successfully")

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
        +purpose: Print HPGL2 job with margin layout set as clipinside but without margins defined to simulate Print from USB/9100
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-191956
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:test_margins_clipinside_300_dpi.hpg=f329a69721defb75754c6e0117717f31d0e8f8340ec75dcedbb74715fd9a8d8b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_hpgl2_9100_usb_margins_clipinside_300_dpi_file_then_succeeds
        +test:
            +title:test_hpgl2_9100_usb_margins_clipinside_300_dpi
            +guid:ffbccaad-29ea-40aa-98dd-60363eb6ae7b
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=HPGL2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_hpgl2_9100_usb_margins_clipinside_300_dpi_file_then_succeeds(self):
        logging.info('Running test_hpgl2_9100_usb_margins_clipinside_300_dpi')
        outputverifier.outputsaver.operation_mode('CRC')
        job_id = self.print.raw.start('f329a69721defb75754c6e0117717f31d0e8f8340ec75dcedbb74715fd9a8d8b')
        self.print.wait_for_job_completion(job_id)
        logging.info("test_margins_clipinside_300_dpi.hpg - Print job completed successfully")

        ### VERIFY
        if outputverifier.outputsaver.configuration.productname == "jupiter":
            expected_crc = ["0x54cade3"]
            expected_margin = 35
        else:
            expected_crc = ["0x6981c237"]
            expected_margin = 59

        # Read and verify that obtained checksums are the expected ones
        outputverifier.save_and_parse_output()
        outputverifier.outputsaver.verify_output_crc(expected_crc)
        logging.info("test_margins_clipinside_300_dpi.hpg - Checksum(s) verified successfully")

        # Verify margins
        outputverifier.verify_top_margin(Intents.printintent, expected_margin)
        outputverifier.verify_bottom_margin(Intents.printintent, expected_margin)
        outputverifier.verify_left_margin(Intents.printintent, expected_margin)
        outputverifier.verify_right_margin(Intents.printintent, expected_margin)

        # Verify page size
        outputverifier.verify_page_width(Intents.printintent, 2481)
        outputverifier.verify_page_height(Intents.printintent, 3508)

        logging.info("test_margins_clipinside_300_dpi.hpg - Dimensions verified successfully")

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Print HPGL2 job with margin layout set as oversize but without margins defined to simulate Print from USB/9100
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-191956
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:test_margins_oversize_300_dpi.hpg=8bc905f582da6e73004884b81da26ebfa29f44b81c5d148aeb03498180c1a074
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_hpgl2_9100_usb_margins_oversize_300_dpi_file_then_succeeds
        +test:
            +title:test_hpgl2_9100_usb_margins_oversize_300_dpi
            +guid:433ba8f4-be96-429e-925d-813b07de3c05
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=HPGL2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_hpgl2_9100_usb_margins_oversize_300_dpi_file_then_succeeds(self):
        logging.info('Running test_hpgl2_9100_usb_margins_oversize_300_dpi')
        outputverifier.outputsaver.operation_mode('CRC')
        job_id = self.print.raw.start('8bc905f582da6e73004884b81da26ebfa29f44b81c5d148aeb03498180c1a074')
        self.print.wait_for_job_completion(job_id)
        logging.info("test_margins_oversize_300_dpi.hpg - Print job completed successfully")

        ### VERIFY
        if outputverifier.outputsaver.configuration.productname == "jupiter":
            expected_crc = ["0x517ffff8"]
            expected_margin = 35
        else:
            expected_crc = ["0x6981c237"]
            expected_margin = 59

        # Read and verify that obtained checksums are the expected ones
        outputverifier.save_and_parse_output()
        outputverifier.outputsaver.verify_output_crc(expected_crc)
        logging.info("test_margins_oversize_300_dpi.hpg - Checksum(s) verified successfully")

        # Verify margins
        outputverifier.verify_top_margin(Intents.printintent, expected_margin)
        outputverifier.verify_bottom_margin(Intents.printintent, expected_margin)
        outputverifier.verify_left_margin(Intents.printintent, expected_margin)
        outputverifier.verify_right_margin(Intents.printintent, expected_margin)

        # Verify page size
        outputverifier.verify_page_width(Intents.printintent, 2481 + expected_margin * 2)
        outputverifier.verify_page_height(Intents.printintent, 3508 + expected_margin * 2)

        logging.info("test_margins_oversize_300_dpi.hpg - Dimensions verified successfully")

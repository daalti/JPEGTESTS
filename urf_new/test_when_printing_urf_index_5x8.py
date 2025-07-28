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
        +purpose:C52178027 Simple print job of Urf Index 5x8 from *na_index_5x8.urf file
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:na_index_5x8.urf=55bb9ae41931e38bcf18c6fa23e9f0c51d4bb89dc51ce6bab34c1af1c80cb811
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_index_5x8_file_then_succeeds
        +test:
            +title:test_urf_index_5x8_page
            +guid:3cd48b39-5ec6-49c0-8cd9-4338d8d38ce7
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-5x8_5x8in
        +overrides:
            +Home:
                +is_manual:False
                +timeout:300
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_index_5x8_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('na_index-5x8_5x8in', default):
            self.media.tray.configure_tray(default, 'na_index-5x8_5x8in', 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('55bb9ae41931e38bcf18c6fa23e9f0c51d4bb89dc51ce6bab34c1af1c80cb811')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

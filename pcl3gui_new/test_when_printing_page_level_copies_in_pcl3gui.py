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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:PageCopies PJL support for SmartStream jobs
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-130648
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:page1_5copies_page1_1copy.pcl=c3b41ca0c4f8b2610b4a2432517a39afc86fa6b870ddb9c6d2ca5d7277f65e83
        +name:TestWhenPrintingJPEGFile::test_when_using_page_level_copies_in_pcl3gui_file_then_succeeds
        +test:
            +title:test_page_level_copies_in_pcl3gui
            +guid:ac6b1182-360d-4fee-af3e-6cd4a5dc5273
            +dut:
                +type:Simulator
                +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI & Print=NumberOfCopies
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_page_level_copies_in_pcl3gui_file_then_succeeds(self):
        self.outputsaver.operation_mode('CRC')
        #The test file changed because previous test file expected unsupported media type on Jupiter & a prompt used to cause timeout
        #Modified the previous file by updating the media type to bond(Id: 1)
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('c3b41ca0c4f8b2610b4a2432517a39afc86fa6b870ddb9c6d2ca5d7277f65e83')
        self.print.wait_for_job_completion(job_id)

        expected_crc = ['0x2d0a4932', '0xb8e7ab58', '0xb8e7ab58', '0xb8e7ab58', '0xb8e7ab58', '0xb8e7ab58']

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)

        self.outputsaver.operation_mode('NONE')

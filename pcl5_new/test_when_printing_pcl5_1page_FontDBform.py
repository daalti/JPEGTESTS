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
        +purpose: unitoffice.prn is a customer escalation file where some text are bold font  and other are printing in regular font
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-211735
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:unit1office.prn=a6cdcd7b0413452bb3ddb814008c26c845a8dce630a23fc9c411ee091add7beb
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_1page_FontDBform_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_1page_FontDBform
            +guid:81ff8aa9-dfac-4b9a-b567-aff529fbb22e
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_1page_FontDBform_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        default = self.media.get_default_source()
        if self.media.is_size_supported('iso_ra4_215x305mm', default):
            self.media.tray.configure_tray(default, 'iso_ra4_215x305mm', 'stationery')
        job_id = self.print.raw.start('a6cdcd7b0413452bb3ddb814008c26c845a8dce630a23fc9c411ee091add7beb')
        self.print.wait_for_job_completion(job_id)
        outputverifier.save_and_parse_output()
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

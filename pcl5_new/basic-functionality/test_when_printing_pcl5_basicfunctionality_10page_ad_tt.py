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
        +purpose: pcl5 basicfunctionality using 10Page_ad_tt.obj
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:240
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:10Page-ad_tt.obj=b7d255091ccaa3c71d2fc24d68974baa4f5ec67fdad28322f98190348df48f80
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_basicfunctionality_10page_ad_tt_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_basicfunctionality_10page_ad_tt
            +guid:a98a95e7-d311-4339-9561-79f3fd216853
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5
        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_basicfunctionality_10page_ad_tt_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('b7d255091ccaa3c71d2fc24d68974baa4f5ec67fdad28322f98190348df48f80')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

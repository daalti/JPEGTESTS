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
        +purpose:Raw text data via PCL5 **Raw_text.txt
        +test_tier: 1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-202711
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Raw_text.txt=32012442531e0b9ebc4578d2af60c2a97958fe4d38df9d4c53506ea902290cac
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_basicfunctionality_raw_text_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl5_basicfunctionality_raw_text
            +guid:ffd45728-3f6e-4c8d-aa07-f576c29ea8c6
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_basicfunctionality_raw_text_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        if self.outputsaver.is_pdl_supported('PCL'):
            job_id = self.print.raw.start('32012442531e0b9ebc4578d2af60c2a97958fe4d38df9d4c53506ea902290cac')
            self.print.wait_for_job_completion(job_id)
            self.outputsaver.save_output()
            logging.info("Get crc value for the current print job")
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        else:
            job_id = self.print.raw.start('32012442531e0b9ebc4578d2af60c2a97958fe4d38df9d4c53506ea902290cac')
            self.print.wait_for_job_completion(job_id)

import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()

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
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Print large jpeg job
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-228793
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:large_image.jpg=40c7bdccc3b536ed31a43208fa935333481533bd65f37fe7dec9a6cf24dc9078
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_large_image_jpg_then_succeeds
        +test:
            +title:test_jpeg_largefile
            +guid:0375c24e-0b72-4d9f-a88d-b9d7700a5246
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & DigitalStorageType=HardDisk & EngineFirmwareFamily=Canon


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_large_image_jpg_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('40c7bdccc3b536ed31a43208fa935333481533bd65f37fe7dec9a6cf24dc9078')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
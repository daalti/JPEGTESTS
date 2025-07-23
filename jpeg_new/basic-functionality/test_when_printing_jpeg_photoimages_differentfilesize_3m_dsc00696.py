import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
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
        +purpose:simple print job of jpeg file of photoimages differentfilesize 3m dsc00696
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_differentfilesize_3M_DSC00696.JPG=9ba3d34b6493769d9d1b40252c3ed9e360de6f4e3e0c93029f616516698637c4
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_differentfilesize_3M_DSC00696_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_differentfilesize_3m_dsc00696
            +guid:15b9c8c3-80a1-4281-894f-ad6e78aea13d
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_differentfilesize_3M_DSC00696_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=453333,
            length_max=340000,
            width_min=453333,
            length_min=340000,  
        )

        job_id = self.print.raw.start('9ba3d34b6493769d9d1b40252c3ed9e360de6f4e3e0c93029f616516698637c4')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg file example photoimages differentfilesize 3M DSC00696 - Print job completed successfully")
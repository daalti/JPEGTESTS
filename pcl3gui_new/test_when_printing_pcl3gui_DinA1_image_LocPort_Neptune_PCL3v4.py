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
        +purpose:Simple print job of pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-18107
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:DinA1_image_LocPort_Neptune_PCL3v4.prn=d12c32dc8c21ab67365790c727bfc924722f4a7e590e7a1c44a7ea9ada089610
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_DinA1_image_LocPort_Neptune_PCL3v4_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4
            +guid:94199c6a-f469-435a-b7f3-4cea78a07d3d
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI & MediaSizeSupported=iso_a1_594x841mm
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl3gui_DinA1_image_LocPort_Neptune_PCL3v4_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('d12c32dc8c21ab67365790c727bfc924722f4a7e590e7a1c44a7ea9ada089610')
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()

        logging.info("Pcl3Gui DinA1_image_LocPort_Neptune_PCL3v4- Print job completed successfully")

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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job on sheet PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:LFPSWQAA-4580
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:printOnsheet.pcl=c7d2cfb9f1753ec458941cc0a18f704c641773ad161adef0d93a5e1d7be5af19
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_print_on_sheet_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_print_on_sheet
            +guid:54c3d444-ab58-4d79-bc0f-447a2aa4ef77
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI&DeviceClass=MFP
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_print_on_sheet_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('iso_a4_210x297mm', default):
            self.media.tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('c7d2cfb9f1753ec458941cc0a18f704c641773ad161adef0d93a5e1d7be5af19')

        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()

        logging.info("PCL3GUI print on sheet successfully")

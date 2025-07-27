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
        +purpose:Simple print job of pcl3Gui_Delenit_A4_P_N
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-18107
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:Delenit_A4_P_N.PCL=46f5bd9eb75c54f928c1b3d79da43ead733944bfd31d604cc9698388a5e0deb8
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_Delenit_A4_P_N_file_then_succeeds
        +test:
            +title:test_pcl3Gui_Delenit_A4_P_N
            +guid:b9e0f853-911e-4392-a01e-9c3493ee8930
            +dut:
                +type:Simulator, Emulator
                +configuration: DocumentFormat=PCL3GUI
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_Delenit_A4_P_N_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('iso_a4_210x297mm', default):
            self.media.tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('46f5bd9eb75c54f928c1b3d79da43ead733944bfd31d604cc9698388a5e0deb8')

        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("Pcl3Gui Delenit_A4_P_N- Print job completed successfully")

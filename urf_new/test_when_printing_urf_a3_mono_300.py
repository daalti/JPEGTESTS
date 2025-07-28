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
        +purpose:URF test using **A3_Mono_300.urf
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-18912
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3_Mono_300.urf=d8dd81c376e6dfced1cafe9845e6f210ef2c8dc298e7af94c8ff94d37c0df427
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_a3_mono_300_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_a3_mono_300
            +guid:7543a96d-52bf-452c-a02d-415c49f3a482
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_a3_mono_300_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('iso_a3_297x420mm', default):
            self.media.tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')

        job_id = self.print.raw.start('d8dd81c376e6dfced1cafe9845e6f210ef2c8dc298e7af94c8ff94d37c0df427')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()

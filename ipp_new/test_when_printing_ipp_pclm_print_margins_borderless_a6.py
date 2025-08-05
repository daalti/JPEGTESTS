import logging

from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

class TestWhenPrintingFileFromIPP(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""
        # no-op unless the legacy file had a matching teardown
        pass

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
        self.media.reset_inputs()

        tear_down_output_saver(self.outputsaver)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C52177656 IPP test for printing a PCLm file with Borderlesss-A6
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:300
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_A6_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=e12ccc2bac8ab6370c0ef988bd23bb56c6dccf8415bc6cda3dc34666d57f5f97
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_margins_borderless_a6_file_then_succeeds
        +test:
            +title:test_ipp_pclm_print_margins_borderless_a6
                    +guid:77cb7f1c-a5de-42f3-b03f-fb1277b34f63
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=iso_a6_105x148mm & MediaType=HPAdvancedPhotoPapers & BorderLessPrinting=True
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_print_margins_borderless_a6_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, 'e12ccc2bac8ab6370c0ef988bd23bb56c6dccf8415bc6cda3dc34666d57f5f97')
        self.print.wait_for_job_completion(job_id)

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
        +purpose:C52177655 IPP test for printing a PCLm file with Borderless-4x6 in
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:300
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_4x6_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7fe66016415859546a91e2a9aef6577b27e33f5960710f30378330dfa0852b72
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_margins_borderless_4x6_file_then_succeeds
        +test:
            +title:test_ipp_pclm_print_margins_borderless_4x6
                    +guid:3c23346f-b74c-4d64-ba32-19b13e0a2c52
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & MediaType=HPAdvancedPhotoPapers & BorderLessPrinting=True
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_print_margins_borderless_4x6_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, '7fe66016415859546a91e2a9aef6577b27e33f5960710f30378330dfa0852b72')
        self.print.wait_for_job_completion(job_id)

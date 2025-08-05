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
        +purpose:C52177646 IPP test for printing a PCLm file with Bordered-Legal
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:300
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_legal_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=8a68cbd1e070d1208a935ae4ba62b25dd10963ba5927fee2500b595a77fc04c9
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_margins_bordered_legal_file_then_succeeds
        +test:
            +title:test_ipp_pclm_print_margins_bordered_legal
                    +guid:5348aebd-df72-43b1-a305-2a437ed9e2b7
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_legal_8.5x14in & MediaType=Plain & MediaInputInstalled=Tray1
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_print_margins_bordered_legal_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, '8a68cbd1e070d1208a935ae4ba62b25dd10963ba5927fee2500b595a77fc04c9')
        self.print.wait_for_job_completion(job_id)

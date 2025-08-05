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

        +purpose:Ipp test for printing a URF file using attribute value media_size_Envelope_DL
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-185216
        +timeout:120
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:DL.urf=0c6fda1e26ac577fab41f56f05bd7f1ecdfb17e0d8c7029f729895bcff461213
            +name:TestWhenPrintingIPPFile::test_when_using_ipp_urf_EnvDL_border_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_urf_EnvDL_border
                +guid:5f217abc-0882-4a31-9662-64307dc06ba4
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=iso_dl_110x220mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_urf_EnvDL_border_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, '0c6fda1e26ac577fab41f56f05bd7f1ecdfb17e0d8c7029f729895bcff461213')
        self.print.wait_for_job_completion(job_id)

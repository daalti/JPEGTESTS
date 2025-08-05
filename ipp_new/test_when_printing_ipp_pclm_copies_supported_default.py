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
        +purpose:C30485288 IPP test for printing a PCLm file with Copies supported default
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_copies_supported_default_file_then_succeeds
        +test:
            +title:test_ipp_pclm_copies_supported_and_default
            +guid:f1e9ebdc-dbfa-4548-b423-184f56ff7c0b
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
        +overrides:
            +Home:
                +is_manual:False
                +timeout:300
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_copies_supported_default_file_then_succeeds(self):
        logging.info("No print job trigger, CRC is null. No need to check CRC for this case.")
        pirnt_file = self.print.get_file("b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8")
        test_file_path = "/code/tests/print/pdl/ipp/attributes/copies_supported_default.test"
        returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_file_path, pirnt_file)
        logging.info(f"Ipp print output content is: <{decoded_output}>")
        assert returncode == 0, f'Unexpected IPP response: {returncode}'
        assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
        assert decoded_output[1] == '', "There is error output for Ipp Print."

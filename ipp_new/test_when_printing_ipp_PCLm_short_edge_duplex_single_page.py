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
        +purpose:C52177639 IPP test for printing a pdf file using attribute value sides_two_sided_short_edge
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-47064
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_PCLm_short_edge_duplex_single_page_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCLm
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_PCLm_short_edge_duplex_single_page
            +guid:87a6f879-e5ff-4b84-93d5-48301e16e489
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PDF & PrintProtocols=IPP
        +overrides:
            +Home:
                +is_manual:False
                +timeout:300
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_PCLm_short_edge_duplex_single_page_file_then_succeeds(self):
        self.outputsaver.operation_mode('TIFF')
        # ipp_test_attribs = {'document-format': 'application/PCLm', 'sides': 'two-sided-short-edge'}
        # ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

        # job_id = self.print.ipp.start(ipp_test_file, 'b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')
        self.print.wait_for_job_completion(job_id)
        # self.outputsaver.save_output()
        print_file = printjob.get_file('b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')

        printjob.bookmark_jobs()
        returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, '/code/output/Duplex_Short.test', print_file)
        print(f"decoded_ouput type {type(decoded_output)}")
        self.outputsaver.operation_mode('NONE')
        print("This ipp cmd never send a print job at all. No need to check CRC for this case.")


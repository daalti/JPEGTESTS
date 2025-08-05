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
        +purpose:C52177632 IPP test for printing GreyscaleSource- greyscale image prints as color-composite grey
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_GRAY__JPG_Source.pdf=321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_color_mode_greyscale_image_prints_as_color_composite_grey_file_then_succeeds
        +test:
            +title:test_ipp_pclm_color_mode_greyscale_image_prints_as_color_composite_grey
            +guid:4193908a-843d-4ac2-b579-3d4c7e41dd79
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & PrintColorMode=Color
        +overrides:
            +Home:
                +is_manual:False
                +timeout:300
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_color_mode_greyscale_image_prints_as_color_composite_grey_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        
        ipp_test_file = '/code/tests/print/pdl/ipp/attributes/ColorOutputMode.test'
        job_id = self.print.ipp.start(ipp_test_file, '321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0')
        self.print.wait_for_job_completion(job_id)
        
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

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
        +purpose:C52177644 IPP test for printing a PCLm file with Bordered-4x6 in
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
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_margins_bordered_4x6_file_then_succeeds
        +test:
            +title:test_ipp_pclm_print_margins_bordered_4x6
            +guid:6dcda66a-7f32-474e-a39f-b5a943d514b7
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & MediaType=HPAdvancedPhotoPapers
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_print_margins_bordered_4x6_file_then_succeeds(self):
        gpa_test_file = "/code/tests/print/pdl/ipp/attributes/gpa.test"
        media_top_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-top-margin-supported')
        media_bottom_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-bottom-margin-supported')
        media_edge_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-left-margin-supported')
        logging.info(f"device top margin value is: {media_top_margin}, bottom margin value is: {media_bottom_margin}, edge margin value is: {media_edge_margin}")
        
        logging.info("Load 4x6 photo glossy paper. Set media size and type from the EWS.")
        ews.media.load_paper_source_trays()
        ews.media.click_edit_default_tray_button(default_tray)
        ews.media.set_media_size("4x6in")
        ews.media.set_media_type("hp_advanced_photo")
        ews.media.set_tray_edit_data()
        ews.media.make_sure_apply_success()
        
        self.outputsaver.validate_crc_tiff()
        
        test_file_path = '/code/tests/print/pdl/ipp/attributes/4x6_Photo.test'
        ipp_extra_command = f"-d topmargin={media_top_margin} -d edgemargin={media_edge_margin} -d botmargin={media_bottom_margin}"
        job_id = self.print.ipp.start(test_file_path, '7fe66016415859546a91e2a9aef6577b27e33f5960710f30378330dfa0852b72')
        self.print.wait_for_job_completion(job_id)
        
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

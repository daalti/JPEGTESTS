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
        +purpose:C52177650 IPP test for printing a PCLm file with Bordered-A4
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_A4_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=2b931e5448da2b6fbce96b836971a0f9008a4d24e0158f4a6c08aec3d288c189
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_margins_bordered_a4_file_then_succeeds
        +test:
            +title:test_ipp_pclm_print_margins_bordered_a4
            +guid:d955ce2a-f610-44e9-a71c-77dade064436
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & MediaType=Plain & MediaInputInstalled=Tray1
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_print_margins_bordered_a4_file_then_succeeds(self):
        gpa_test_file = "/code/tests/print/pdl/ipp/attributes/gpa.test"
        media_top_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-top-margin-supported')
        media_bottom_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-bottom-margin-supported')
        media_edge_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-left-margin-supported')
        logging.info(f"device top margin value is: {media_top_margin}, bottom margin value is: {media_bottom_margin}, edge margin value is: {media_edge_margin}")
        
        logging.info("Load A4, plain paper. Set media size and type from the EWS.")
        ews.media.load_paper_source_trays()
        ews.media.click_edit_default_tray_button(default_tray)
        ews.media.set_media_size("a4_210x297_mm")
        ews.media.set_media_type("plain")
        ews.media.set_tray_edit_data()
        ews.media.make_sure_apply_success()
        
        self.outputsaver.validate_crc_tiff()
        
        test_file_path ='/code/tests/print/pdl/ipp/attributes/A4.test'
        ipp_extra_command = f"-d topmargin={media_top_margin} -d edgemargin={media_edge_margin} -d botmargin={media_bottom_margin}"
        job_id = self.print.ipp.start(test_file_path, '2b931e5448da2b6fbce96b836971a0f9008a4d24e0158f4a6c08aec3d288c189')
        self.print.wait_for_job_completion(job_id)
        
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

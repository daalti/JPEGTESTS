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
        +purpose:URF test using **om_legal_216x340mm_Mono.urf
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-18912
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:om_legal_216x340mm_Mono.urf=ead74db99f97df029f12d4f902fb1dcbdea11df70092d8d2b488c113fb9effab
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_om_legal_216x340mm_mono_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_om_legal_216x340mm_mono
            +guid:2d767592-839d-48cd-95c2-ae65668ac16f
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=na_oficio_8.5x13.4in
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_om_legal_216x340mm_mono_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('na_oficio_8.5x13.4in', default):
            self.media.tray.configure_tray(default, 'na_oficio_8.5x13.4in', 'stationery')
        elif self.media.tray.is_size_supported('custom', default) and self.media.tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"] >= 85033:
            # the size of print file should in max/min custom size of printer supported, then could set custom size
            self.media.tray.configure_tray(default, 'custom', 'stationery')
        elif self.media.tray.is_size_supported('na_letter_8.5x11in', default):
            self.media.tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
        
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('ead74db99f97df029f12d4f902fb1dcbdea11df70092d8d2b488c113fb9effab')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.clear_output()
        self.media.tray.reset_trays()

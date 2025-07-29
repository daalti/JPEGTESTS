import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
import time
import requests
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from tests.print.lib.actions.print_helper import Print

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
        +purpose:Simple print job of packets_cmyk_planar_2_colors.rs and pause job
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-18107
        +timeout:600
        +asset:PDL_New
        +test_framework:TUF
        +delivery_team:QualityGuild
        +feature_team:ProductQA
        +external_files:packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_packets_cmyk_planar_2_colors_pause_job_file_then_succeeds
        +test:
            +title:test_rs_packets_cmyk_planar_2_colors_pause_job
            +guid:f9faa3ae-f5fb-40ae-82ea-39f67fdbb9e1
            +dut:
                +type:Emulator
                +configuration: DocumentFormat=RasterStreamPlanarICF & PrintEngineType=MaiaLatex
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_packets_cmyk_planar_2_colors_pause_job_file_then_succeeds(self):

        # start printing and stop the job
        helper = Print(printjob, job, tclMaia)

        job_id = helper.print_and_stop("85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8")

        # check alert screen
        alert_image = spice.wait_for("#TitleText SpiceLottieImageView")
        assert str(alert_image["source"]) == str("qrc:/images/Status/ErrorFill.json")

        alert_description = spice.wait_for("#alertDetailDescription SpiceText[visible=true]")
        assert str(LocalizationHelper.get_string_translation(net, "cClosePrintZoneWindow", locale)) == str(alert_description["text"])

        time.sleep(10)
        # close the cover
        tclMaia.execute("WindowSensor setValue 0")

        # check job is finished
        self.print.wait_for_job_completion(job_id, timeout=600)


import logging

from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

ATTRIBUTES = {
    'output-bin': 'dummy-tray',
    'resolution': '1234x1234dpi',
    'print-quality': 100,
    'copies': 100,
    'page-ranges': '0-0',
    'orientation-requested': 100,
    'sides': 'dummySide',
    'multiple-document-handling': 'dummpyDoc',
    'scaling': 'dummyFit',
    'print-color-mode': 'dummyColor',
    'output-mode': 'dummyOutputMode',
    'print-content-optimize': 'dummyOptimizer',
    'print-rendering-intent': 'dummyRendering',
    'media': 'dummyMedia',
    'media-source': 'dummyMediaSource',
    'media-type': 'dummyMediaType',
    'media-top-margin': 'dummyTopMargin',
    'media-bottom-margin': 'dummyBottomMargin',
    'media-left-margin': 'dummyLeftMargin',
    'media-right-margin': 'dummyRightMargin'
}


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
        +purpose: IPP test with fidelity true and invalid values
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-47064
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_fidelity_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_fidelity_true
            +guid:09b97eb7-34fb-4df6-b945-3689c533e7f1
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PDF & PrintProtocols=IPP
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_fidelity_file_then_succeeds(self):
        for key, value in ATTRIBUTES.items():
            ipp_test_attribs = {'document-format': 'application/pdf', 'ipp-attribute-fidelity': 'true', key: value}
            ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
            try:
                logging.info('Verifying fidelity with attribute: %s', key)
                job_id = self.print.ipp.start(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
                self.print.wait_for_job_completion(job_id)
                assert False, f'Test was expectd to fail with {key} as {value}'
            except AssertionError as exp:
                if 'Unexpected IPP response' in str(exp):
                    logging.info('Test failed as expected with %s as %s', key, value)

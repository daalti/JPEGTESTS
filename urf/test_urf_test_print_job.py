import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Test Print Job Page from *TestPrintJob.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:TestPrintJob.urf=387ec5cd473f58b64c6179f35beb3ef556ba229f495ce89921c0d128c0dac888
    +name:test_urf_test_print_job_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_test_print_job_page
        +guid:ce1e7bef-404f-41cf-ba6d-1d5d57187797
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_test_print_job_page(setup_teardown, printjob, outputsaver, tray, print_emulation, configuration):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(trayid="all",media_size=MediaSize.Letter.name,media_type=MediaType.Plain.name,orientation=MediaOrientation.Default.name,level=TrayLevel.Full.name)
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('387ec5cd473f58b64c6179f35beb3ef556ba229f495ce89921c0d128c0dac888')
    outputsaver.save_output()
    tray.reset_trays()
    logging.info("URF Test Print Job Page - Print job completed successfully")

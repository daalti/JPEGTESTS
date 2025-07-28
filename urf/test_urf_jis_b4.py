import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf JIS B4 from *JIS_B4.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:JIS_B4.urf=bcc2323674895e324ec89e1517fdb41386076f4040b3c4c9566ed49a47b06e90
    +name:test_urf_jis_b4_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_jis_b4_page
        +guid:424388e4-edbb-4410-b171-2e878158758a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_jis_b4_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('jis_b4_257x364mm', default):
        tray.configure_tray(default, 'jis_b4_257x364mm', 'stationery')

    printjob.print_verify('bcc2323674895e324ec89e1517fdb41386076f4040b3c4c9566ed49a47b06e90')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF JIS B4 Page - Print job completed successfully")

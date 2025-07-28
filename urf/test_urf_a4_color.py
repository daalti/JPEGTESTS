import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf A4 Color from *A4_Color.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_Color.urf=a95b47aa819ddce1710f1c153c5fb29cafc8635c38384e8d9db727524f93a30b
    +name:test_urf_a4_color_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a4_color_page
        +guid:a61b847f-fd08-4d01-84b6-0ef54e6c4de1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a4_color_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('a95b47aa819ddce1710f1c153c5fb29cafc8635c38384e8d9db727524f93a30b')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF A4 Color page - Print job completed successfully")

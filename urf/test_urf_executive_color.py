import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Executive Color from *Executive_Color.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Executive_Color.urf=2488929b9327c6751847274ae39a814dda79c6e2adf2a8582082ce8121216078
    +name:test_urf_executive_color_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_executive_color_page
        +guid:c15fe293-b9bb-4711-b6c6-909057072555
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_executive_7.25x10.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_executive_color_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_executive_7.25x10.5in', default):
        tray.configure_tray(default, 'na_executive_7.25x10.5in', 'stationery')

    printjob.print_verify('2488929b9327c6751847274ae39a814dda79c6e2adf2a8582082ce8121216078')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Executive Color page - Print job completed successfully")

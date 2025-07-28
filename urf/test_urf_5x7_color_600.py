import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 5x7 color 600 page from *5x7_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5x7_Color_600.urf=71131a0deaaa360492a204f4633b602ef1bcb1a742acfbaa50636c77938b2d08
    +name:test_urf_5x7_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_5x7_color_600_page
        +guid:fa1128454-7b53-4384-b9ca-d4d56ee70606
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_5x7_5x7in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_5x7_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index_5x7_5x7in', default):
        tray.configure_tray(default, 'na_index_5x7_5x7in', 'stationery')
    elif tray.is_size_supported('na_5x7_5x7in', default):
        tray.configure_tray(default, 'na_5x7_5x7in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('71131a0deaaa360492a204f4633b602ef1bcb1a742acfbaa50636c77938b2d08', timeout=180)
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 5x7 color 600 page - Print job completed successfully")

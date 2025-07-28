import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Monarch Color 300 Page from *Monarch_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Monarch_Color_300.urf=dd8218349b89937d925ade1962fb55d82d9a9cb89a11da93fd0eac478ee1f317
    +name:test_urf_monarch_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_monarch_color_300_page
        +guid:efc44953-70df-4fd1-b082-00d4b106b9eb
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_monarch_3.875x7.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_monarch_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_monarch_3.875x7.5in', default):
        tray.configure_tray(default, 'na_monarch_3.875x7.5in', 'stationery')

    printjob.print_verify('dd8218349b89937d925ade1962fb55d82d9a9cb89a11da93fd0eac478ee1f317')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Monarch Color 300 Page - Print job completed successfully")

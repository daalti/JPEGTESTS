import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Invoice Color 300 urf from *Invoice_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Invoice_Color_300.urf=64ea208a7024556d2249abd69b81382f05b4ab67733bbe7ed5535fdcee7f0066
    +name:test_urf_invoice_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_invoice_color_300_page
        +guid:3ef9ff99-5bae-467c-a3cc-b23faafb9738
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_invoice_5.5x8.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_invoice_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_invoice_5.5x8.5in', default):
        tray.configure_tray(default, 'na_invoice_5.5x8.5in', 'stationery')

    printjob.print_verify('64ea208a7024556d2249abd69b81382f05b4ab67733bbe7ed5535fdcee7f0066')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Invoice Color 300 Page - Print job completed successfully")

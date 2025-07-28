import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Invoice Color 600 urf from *Invoice_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Invoice_Color_600.urf=f13c121faba7454de342962d29433672eea48ff5b123d3980833d8fd2174cf8f
    +name:test_urf_invoice_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_invoice_color_600_page
        +guid:0b0940d5-6045-4159-878d-80c4577e754d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_invoice_5.5x8.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_invoice_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_invoice_5.5x8.5in', default):
        tray.configure_tray(default, 'na_invoice_5.5x8.5in', 'stationery')

    printjob.print_verify('f13c121faba7454de342962d29433672eea48ff5b123d3980833d8fd2174cf8f')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Invoice Color 600 Page - Print job completed successfully")

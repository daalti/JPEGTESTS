import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf na invoice 5.5x8.5 Page from *na_invoice_5.5x8.5.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:na_invoice_5.5x8.5.urf=f13c121faba7454de342962d29433672eea48ff5b123d3980833d8fd2174cf8f
    +name:test_urf_na_invoice_5_5x8_5_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_na_invoice_5_5x8_5_page
        +guid:d3f4bd58-5753-4c5d-8159-b04e3545c8d2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_invoice_5.5x8.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_na_invoice_5_5x8_5_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_invoice_5.5x8.5in', default):
        tray.configure_tray(default, 'na_invoice_5.5x8.5in', 'stationery')

    printjob.print_verify('f13c121faba7454de342962d29433672eea48ff5b123d3980833d8fd2174cf8f')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF na invoice 5.5x8.5 Page - Print job completed successfully")

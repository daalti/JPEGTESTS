import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Invoice_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Invoice_Mono_600.urf=299495268a5fae6883e8a1b32ef036ec9914915cc07244b62a662803d4e5a688
    +name:test_urf_invoice_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_invoice_mono_600
        +guid:f69e9972-25da-4b61-99a9-aae40a93ecb4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_invoice_5.5x8.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_invoice_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_invoice_5.5x8.5in', default):
        tray.configure_tray(default, 'na_invoice_5.5x8.5in', 'stationery')

    printjob.print_verify('299495268a5fae6883e8a1b32ef036ec9914915cc07244b62a662803d4e5a688')
    outputsaver.save_output()
    tray.reset_trays()

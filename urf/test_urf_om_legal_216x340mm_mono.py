import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **om_legal_216x340mm_Mono.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:om_legal_216x340mm_Mono.urf=ead74db99f97df029f12d4f902fb1dcbdea11df70092d8d2b488c113fb9effab
    +name:test_urf_om_legal_216x340mm_mono
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_om_legal_216x340mm_mono
        +guid:421e2297-e25b-4552-94c3-a04591defdc5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_oficio_8.5x13.4in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_om_legal_216x340mm_mono(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_oficio_8.5x13.4in', default):
        tray.configure_tray(default, 'na_oficio_8.5x13.4in', 'stationery')
    elif tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"] >= 85033:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, 'custom', 'stationery')
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    
    printjob.print_verify('ead74db99f97df029f12d4f902fb1dcbdea11df70092d8d2b488c113fb9effab')
    outputsaver.save_output()
    outputsaver.clear_output()
    tray.reset_trays()

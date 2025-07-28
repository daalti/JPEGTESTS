import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **16k_184x260_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:16k_184x260_Mono_600.urf=76ec4e1cc899b6c2035e194574cd4e2e158f8f829dd951cee3dc2841a58a0827
    +name:test_urf_16k_184x260_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_16k_184x260_mono_600
        +guid:21c1a9de-0126-4086-9e98-5e6e05e80cf7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=om_16k_184x260mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_16k_184x260_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_16k_184x260mm', default):
        tray.configure_tray(default, 'om_16k_184x260mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('76ec4e1cc899b6c2035e194574cd4e2e158f8f829dd951cee3dc2841a58a0827')
    outputsaver.save_output()
    tray.reset_trays()

import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Monarch_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Monarch_Mono_600.urf=b6aa5db4834d3cbbbf9652edd743a5e6b2e8c955fd4f942c3cdc24bb894029bd
    +name:test_urf_monarch_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_monarch_mono_600
        +guid:b81f7653-6ff5-46f0-82d3-f4dae620b372
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_monarch_3.875x7.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_monarch_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_monarch_3.875x7.5in', default):
        tray.configure_tray(default, 'na_monarch_3.875x7.5in', 'stationery')

    printjob.print_verify('b6aa5db4834d3cbbbf9652edd743a5e6b2e8c955fd4f942c3cdc24bb894029bd')
    outputsaver.save_output()
    tray.reset_trays()

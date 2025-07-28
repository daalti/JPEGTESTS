import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Hagaki_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Hagaki_Mono_600.urf=c96b964550b96212397c185dceefd3aa03e5919f43dd33d12fd24fbf7d557df1
    +name:test_urf_hagaki_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_hagaki_mono_600
        +guid:45ea6d45-fd83-4bc2-b3a6-3a3de739cb09
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jpn_hagaki_100x148mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_hagaki_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('jpn_hagaki_100x148mm', default):
        tray.configure_tray(default, 'jpn_hagaki_100x148mm', 'stationery')

    printjob.print_verify('c96b964550b96212397c185dceefd3aa03e5919f43dd33d12fd24fbf7d557df1')
    outputsaver.save_output()
    tray.reset_trays()

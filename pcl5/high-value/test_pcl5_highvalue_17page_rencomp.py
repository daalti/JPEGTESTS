import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 17Page_rencomp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:17Page-rencomp.obj=e93fe7934af63b34b1369c72ee61e27949a97cb296fa9d59e960584b964b9c45
    +test_classification:System
    +name: test_pcl5_highvalue_17page_rencomp
    +test:
        +title: test_pcl5_highvalue_17page_rencomp
        +guid:5c7a2423-1db3-4eac-868f-0f94c71815cb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_17page_rencomp(setup_teardown, printjob, outputsaver, print_emulation):
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            if MediaSize.Letter.name in supported_sizes and MediaType.Plain.name in supported_types:
                print_emulation.tray.load(tray_id, MediaSize.Letter.name, MediaType.Plain.name)
  
    printjob.print_verify('e93fe7934af63b34b1369c72ee61e27949a97cb296fa9d59e960584b964b9c45',timeout=300)
    outputsaver.save_output()

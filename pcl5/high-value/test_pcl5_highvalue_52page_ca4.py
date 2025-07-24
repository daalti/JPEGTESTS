import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 52Page_ca4.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:52Page-ca4.obj=0d12f2769c97c4f69d2f36d777744968fac06a802bf8831bc094767fdb0fea6a
    +test_classification:System
    +name: test_pcl5_highvalue_52page_ca4
    +test:
        +title: test_pcl5_highvalue_52page_ca4
        +guid:3582d220-896f-4f86-a13f-2f692f96db1f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:900
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_52page_ca4(setup_teardown, printjob, outputsaver,tray, print_emulation, configuration):
    default = tray.get_default_source()
    #if print_emulation.print_engine_platform == 'emulator':
    #   print_emulation.tray.setup_tray(trayid="all",media_size=MediaSize.RA4.name,media_type=MediaType.Plain.name,orientation=MediaOrientation.Default.name,level=TrayLevel.Full.name)
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        installed_trays = print_emulation.tray.get_installed_trays()
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            if MediaSize.RA4.name in supported_sizes and MediaType.Plain.name in supported_types:
                print_emulation.tray.capacity_unlimited(tray_id)
                print_emulation.tray.load(tray_id, MediaSize.RA4.name, MediaType.Plain.name, media_orientation=MediaOrientation.Portrait.name)
    elif tray.is_size_supported('iso_ra4_215x305mm', default):
          tray.configure_tray(default, 'iso_ra4_215x305mm', 'stationery')
    elif tray.is_size_supported('iso_a4_210x297mm', default):
         tray.configure_tray(default, 'iso_a4_210x297mm','stationery')
    printjob.print_verify('0d12f2769c97c4f69d2f36d777744968fac06a802bf8831bc094767fdb0fea6a', timeout=900)
    outputsaver.save_output()

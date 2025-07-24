import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 66Page_cexec.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:66Page-cexec.obj=1813aef5904a3536308dd913ebe77a7880851c2ab90aa7a56de747e0e3cab63b
    +test_classification:System
    +name: test_pcl5_highvalue_66page_cexec
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_66page_cexec
        +guid:a9482cf7-42c9-488f-945a-2709f1664ed6
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

def test_pcl5_highvalue_66page_cexec(setup_teardown, printjob, outputsaver,tray, print_emulation, configuration):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        installed_trays = print_emulation.tray.get_installed_trays()
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            if  MediaSize.Executive.name  in supported_sizes and MediaType.Plain.name in supported_types:
                print_emulation.tray.capacity_unlimited(tray_id)
                print_emulation.tray.load(tray_id, MediaSize.Executive.name, MediaType.Plain.name)
                logging.info(f"Emulator: Loaded {tray_id} with Executive and Plain")
    
    elif tray.is_size_supported('na_executive_7.25x10.5in', default):
        tray.configure_tray(default, 'na_executive_7.25x10.5in','stationery')
    printjob.print_verify('1813aef5904a3536308dd913ebe77a7880851c2ab90aa7a56de747e0e3cab63b', timeout=900)
    outputsaver.save_output()

import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 2Page_fullp300.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:2Page-fullp300.obj=10d382ba3e17406afec85c76bd74fdaea565782f0ab1114d7c4049c1408ea661
    +test_classification:System
    +name: test_pcl5_basicfunctionality_2page_fullp300
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_2page_fullp300
        +guid:5dfc3d41-6a5b-4124-92c1-551a927c9932
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
def test_pcl5_basicfunctionality_2page_fullp300(setup_teardown, printjob, outputsaver, tray, udw, print_emulation, configuration):
    default = tray.get_default_source()
    outputsaver.validate_crc_tiff(udw)

    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        tray1 = MediaInputIds.Tray1.name
        if tray.is_size_supported('na_legal_8.5x14in', 'tray-1'):
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, MediaSize.Legal.name, MediaType.Plain.name)
            print_emulation.tray.close(tray1)
    else:
        if tray.is_size_supported('na_legal_8.5x14in', default):
            tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')

    printjob.print_verify('10d382ba3e17406afec85c76bd74fdaea565782f0ab1114d7c4049c1408ea661', timeout=180)
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

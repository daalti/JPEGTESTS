import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669604 pcl5 highvalue using 2Page_mcroexec.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2Page-mcroexec.obj=88771a72bf97e33f909901abb64a258bc4c159a19a4f73cf2fdd3847ea123c75
    +test_classification:System
    +name: test_pcl5_highvalue_2page_mcroexec
    +test:
        +title: test_pcl5_highvalue_2page_mcroexec
        +guid:ccf467e3-9e5a-4434-a547-b751e5212d39
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
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_2page_mcroexec(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('88771a72bf97e33f909901abb64a258bc4c159a19a4f73cf2fdd3847ea123c75', timeout=600)
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

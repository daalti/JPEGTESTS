import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job of a rasterstream file tower_a3.rs
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-2765, LFPSWQAA-3262, DUNE-14986
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:tower_a3.rs=b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617
    +test_classification:System
    +name:test_rs_tower_a3
    +test:
        +title:test_rs_tower_a3
        +guid:0aa1888d-ebd8-4a60-a455-df411b9d495d
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_tower_a3(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617', timeout=300)
    logging.info("tower_a3.rs - Print job completed successfully")

    expected_crc = ["0x69551a32"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("tower_a3.rs - Checksum(s) verified successfully")
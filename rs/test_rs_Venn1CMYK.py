import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job of file Venn1CMYK.rs **
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-2765
    +timeout:200
    +asset:LFP
    +delivery_team:LFP
    +feature_team:ProductQA
    +test_framework:TUF
    +external_files:Venn1CMYK.rs=2460d37ca59f6d731cd69e69f62e3f50846a1c7b80859d8172780a4f40064693
    +test_classification:System
    +name:test_rs_Venn1CMYK
    +test:
        +title:test_rs_Venn1CMYK
        +guid:edd6326f-d53f-40f6-b61c-2fcc18831863
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_rs_Venn1CMYK(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify('2460d37ca59f6d731cd69e69f62e3f50846a1c7b80859d8172780a4f40064693', timeout=180)
    logging.info("RS Venn1CMYK - Print job completed successfully")
    
    expected_crc = ["0xe78eb50d"]
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("RS Venn1CMYK - Checksum(s) verified successfully")

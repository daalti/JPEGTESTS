import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job of file Venn1RGB.rs **
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-2765
    +timeout:120
    +asset:LFP
    +delivery_team:LFP
    +feature_team:ProductQA
    +test_framework:TUF
    +external_files:Venn1RGB.rs=e4b093935481c7ec9e428194a9c7fa475558e18104bb66dfdd4736b81906f3a5
    +test_classification:System
    +name:test_rs_Venn1RGB
    +test:
        +title:test_rs_Venn1RGB
        +guid:d070ea73-9ce8-4725-866f-ca40208ca553
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_rs_Venn1RGB(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')
    
    printjob.print_verify('e4b093935481c7ec9e428194a9c7fa475558e18104bb66dfdd4736b81906f3a5')
    logging.info("RS Venn1RGB - Print job completed successfully")
    
    expected_crc = ["0xc4cbd5fe"]
    
    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("RS Venn1RGB - Checksum(s) verified successfully")

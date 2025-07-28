import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print from a rasterstream (.rs) file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:LFPSWQAA-5221
    +timeout:200
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:A3.urf=1027b94fbc1e93bcc14c2ab0979902a683e1ce876804fc2c2d71b9201ba3e012
    +name:test_urf_A3_checksum
    +test:
        +title:test_urf_A3_checksum
        +guid:52cf84fa-d4f5-11ec-ba0d-b36b387973bc
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_A3_checksum(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('1027b94fbc1e93bcc14c2ab0979902a683e1ce876804fc2c2d71b9201ba3e012', timeout=300)
    logging.info("urf basic file A3.urf - Print job completed successfully")

    expected_crc = ["0x88567900"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("urf basic file A3.urf - Checksum(s) verified successfully")

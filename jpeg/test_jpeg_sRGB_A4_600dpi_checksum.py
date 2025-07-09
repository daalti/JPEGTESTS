import pytest
import logging
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file *sRGB_A4_600dpi.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
    +test_classification:System
    +name:test_jpg_sRGB_A4_600dpi_checksum
    +test:
        +title:test_jpg_sRGB_A4_600dpi_checksum
        +guid:077612ce-4f01-4647-a42b-e3c00c8c4560
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=JPEG
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpg_sRGB_A4_600dpi_checksum(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b', timeout=300)
    logging.info("basic file sRGB_A4_600dpi.jpg - Print job completed successfully")

    expected_crc = ["0x35d1f2ef"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("basic file sRGB_A4_600dpi.jpg - Checksum(s) verified successfully")

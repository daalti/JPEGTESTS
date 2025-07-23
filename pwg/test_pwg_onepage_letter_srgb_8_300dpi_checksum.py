import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file *onepage-letter-srgb-8-300dpi.pwg
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-2761
    +timeout:500
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:onepage-letter-srgb-8-300dpi.pwg=f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e
    +test_classification:system
    +name:test_pwg_onepage_letter_srgb_8_300dpi_checksum
    +test:
        +title:test_pwg_onepage_letter_srgb_8_300dpi_checksum
        +guid:554f6eb8-b394-4e46-8850-2e4ae2f819a5
        +dut:
            +type:Simulator, Emulator
            +configuration:EngineFirmwareFamily=Maia & DocumentFormat=PWGRaster
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_onepage_letter_srgb_8_300dpi_checksum(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e', timeout=300)
    logging.info("onepage_letter_srgb_8_300dpi.pwg - Print job completed successfully")

    expected_crc = ["0x6ae1aba7"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("onepage_letter_srgb_8_300dpi.pwg - Checksum(s) verified successfully")

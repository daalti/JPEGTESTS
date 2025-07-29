import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a sandwich job.
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-6621
    +timeout:1000
    +asset:LFP
    +test_framework:TUF
    +delivery_team:LFP
    +feature_team:ProductQA
    +external_files:JapanSandwich-SW3L-W10060p110-CMYKWCMYK-600.prt=ffe6b8879c296c095b90f1bed48672cd349097204b14fc1f3fcd9e7d36a3ce16
    +test_classification:System
    +name:test_rs_JapanSandwich_SW3L_W10060p110_CMYKWCMYK_600
    +test:
        +title:test_rs_JapanSandwich_SW3L_W10060p110_CMYKWCMYK_600
        +guid:d0e1d6b9-3b83-486c-83e1-3e04b2e456ba
        +dut:
            +type:Simulator, Emulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_JapanSandwich_SW3L_W10060p110_CMYKWCMYK_600(setup_teardown, printjob, outputsaver, tray, tcl, tclMaia):

    try:
        tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")
    except:
        tclMaia.execute("setMediaLoaded ROLL 64 150106")
    
    # CRC will be calculated using the payload of the RasterData
    outputsaver.operation_mode('CRC')

    printjob.print_verify("ffe6b8879c296c095b90f1bed48672cd349097204b14fc1f3fcd9e7d36a3ce16", timeout=1000)
    logging.info("JapanSandwich-SW3L-W10060p110-CMYKWCMYK-600.prt - Print job completed successfully")
    
    expected_crc = ["0xb76d8835"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.verify_output_crc(expected_crc)
    logging.info("JapanSandwich-SW3L-W10060p110-CMYKWCMYK-600.prt - Checksum(s) verified successfully")

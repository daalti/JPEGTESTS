import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: A0 rasterstream (.rs) file print
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-14986
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:tower_a0.rs=5bf95e48e5ba0f74b5708008029d5c943aa9516995e52c332d3cf625dc5786ba
    +name:test_rs_tower_a0
    +test:
        +title:test_rs_tower_a0
        +guid:bd700378-f52e-4295-bcb4-47a8dc2a2460
        +dut:
            +type: Simulator, Emulator
            +configuration: PrintEngineType=Maia & DocumentFormat=RasterStreamICF & MediaSizeSupported=A0_Landscape
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_tower_a0(setup_teardown, printjob, outputsaver):
    
    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    jobid = printjob.start_print('5bf95e48e5ba0f74b5708008029d5c943aa9516995e52c332d3cf625dc5786ba')
    
    printjob.wait_verify_job_completion(jobid, timeout=300)
    logging.info("tower_a0.rs - Print job completed successfully")

    expected_crc = ["0x7a714995"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("tower_a0.rs - Checksum(s) verified successfully")
